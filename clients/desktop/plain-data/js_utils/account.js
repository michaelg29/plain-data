const config = require('./global/config');
const client = require('electron').remote.getGlobal('client');

const renderer = require('./../js_content/renderer');

function login(username, password) {
    let req = {
        "type": "account",
        "action": "login",
        "values": {
            "u": username,
            "p": password
        }
    }

    console.log("login");
    client.setResponseAction(loginResponse);
    client.encAndSend(req);
}

function loginResponse(msg) {
    console.log('login res',msg)

    if (msg['result'] === 'login-success') {
        console.log("success");
        renderer.goto_pg('dashboard');
    } else {
        console.log('failed login');
        renderer.ipcRenderer('login:failed');
    }
}

module.exports = {
    login
};