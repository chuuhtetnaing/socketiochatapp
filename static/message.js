document.addEventListener('DOMContentLoaded', () => {

	    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#send').onclick = () => {
        	let message = document.querySelector("#message").value;
        	let channelname = document.querySelector("#channelname").innerHTML;
        	let username = document.querySelector("#username").innerHTML;
	        socket.emit('send message', {'message': message, 'channelname': channelname, 'username': username});
        };


    });

    socket.on('deliver message', data => {
    	const li = document.createElement('li');
    	li.innerHTML = `${data.message}<br>By <b>${data.username}</b> At <i>${data.time}</i>`;
    	document.querySelector('#messages').append(li);
    	document.querySelector("#message").value = "";
    });

});