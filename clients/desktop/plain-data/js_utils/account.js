const client = require('./global/data_client');

const renderer = require('./../js_content/renderer');

function login(username, password) {
    let req = {
        "type": "account",
        "action": "login",
        "values": {
            "username": username,
            "password": password
        }
    }

    client.setResponseAction(loginResponse);
    client.encAndSend(JSON.stringify(req));
}

function loginResponse(msg) {
    if (req['result']) {
        renderer.goto_pg('dashboard');
    } else {
        console.log('failed login');
        renderer.ipcRenderer('login:failed');
    }
}

module.exports = {
    login
};