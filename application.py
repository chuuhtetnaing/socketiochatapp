import os
import requests
import time

from flask import Flask, session, jsonify, redirect, url_for, render_template, request
from flask_session import Session
from flask_socketio import SocketIO, emit

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'application'

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

channel_list = list()
message_dict = dict()

@app.route("/")
def index():
	if( (session.get('current_channel')) and session.get('current_channel') in channel_list):
		return redirect(url_for("channel", channelname=session['current_channel']))
	return render_template("index.html")

@app.route("/user_registration", methods=["POST"])
def user_register():
    username = request.form.get("username")
    session['user'] = username
    return redirect(url_for("index"))

@app.route("/channel")
def channels():
	if( (session.get('current_channel')) and session.get('current_channel') in channel_list):
		return redirect(url_for("channel", channelname=session['current_channel']))
	return render_template("channels.html", channels=channel_list)

@app.route("/user_deletion")
def user_delete():
    session.pop("user")
    return redirect(url_for("index"))


@app.route("/channel_create", methods=["POST"])
def channel_create():
	channelname = request.form.get("channelname")
	channel_list.append(channelname)
	message_dict[channelname] = list()
	return redirect(url_for("channels"))

@app.route("/channel/<channelname>")
def channel(channelname):
	error = False
	session['current_channel'] = channelname
	if channelname not in channel_list:
		error = True
	return render_template("channel.html", channelname=channelname, messages = message_dict[channelname], error=error)

@socketio.on("send message")
def messages(data):
	message = data["message"]
	username = data["username"]
	local_time = time.asctime(time.localtime(time.time()))
	message_dict[data["channelname"]].append((message, username, local_time))
	emit("deliver message", {"message": message, "username": username, "time": local_time}, broadcast=True)

@app.route("/channel_quit")
def channel_quit():
	session.pop('current_channel')
	return redirect(url_for('channels'))