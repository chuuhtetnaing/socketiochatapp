document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#register').onclick = register;

    let user_deletion = document.querySelector('#delete_user');
    let user_registeration = document.querySelector('#user_register');

    if (user_deletion) {
            user_deletion.onclick = () => {
            delete_user();
            delete_channel();
        }    
    }
    
    if (user_registeration) {
            user_registeration.onsubmit = () => {
            let getname = document.querySelector('#getname').value;
            localStorage.setItem('user', getname);
        }    
    }

});

function delete_user(){
    localStorage.removeItem('user');
}

function delete_channel(){
    localStorage.removeItem('current_channel');
}