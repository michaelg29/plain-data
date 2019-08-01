const config = require('../global/config');
const client = require('electron').remote.getGlobal('client');

const renderer = require('../../js_content/renderer');

let user_ = {};

function login(username, password) {
    let req = {
        "type": "account",
        "action": "login",
        "values": {
            "u": username,
            "p": password
        }
    }

    user_['Username'] = username;

    client.setResponseAction(loginResponse);
    client.encAndSend(req);
}

function loginResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Logged in', 'You have successfully logged in!');
        global.user = user_;
    } else {
        renderer.sendData('login:failed', msg['reasons']);
    }
}

function createAccount(user) {
    let req = {
        "type": "account",
        "action": "create",
        "values": user
    }

    user_['LastName'] = user['l'];
    user_['FirstName'] = user['f'];
    user_['Username'] = user['u'];
    user_['Email'] = user['e'];

    client.setResponseAction(createAccountResponse);
    client.encAndSend(req);
}

function createAccountResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Created account', 'You have successfully created an account!');
        global.user = user_;
    } else {
        renderer.sendData('create:failed', msg['reasons']);
    }
}

function forgot(id, email) {

}

function forgotResponse(msg) {

}

function save(user) {

}

function saveResponse(user) {

}

function logout() {
    global.user = {};
}

module.exports = {
    login,
    createAccount,
    forgot,
    save,
    logout
};