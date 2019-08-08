/*
    account class
*/

const remote = require('electron').remote;
const client = remote.getGlobal('client');

const renderer = require('../../js_content/renderer');

// temproary user data storage
let user_ = {};

/*
    login with username and password
*/
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

/*
    parse response from server for login request
*/
function loginResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Logged in', 'You have successfully logged in!');
        user_['ID'] = msg['values']['i'];

        remote.getGlobal('user').atts = user_;

        remote.getGlobal('loggedIn').val = true;
        renderer.updateConfig('account');
    } else {
        renderer.sendData('login:failed', msg['reasons']);
    }
}

/*
    create account with user data
*/
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

/*
    parse response from server for create account request
*/
function createAccountResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Created account', 'You have successfully created an account!');
        user_['ID'] = msg['values']['i'];
        remote.getGlobal('user').atts = user_;
        
        remote.getGlobal('loggedIn').val = true;
        renderer.updateConfig('account');
    } else {
        renderer.sendData('create:failed', msg['reasons']);
    }
}

/*
    forgot password function for user with id and email
*/
function forgot(id, email) {

}

/*
    parse response from server for forgot password request
*/
function forgotResponse(msg) {

}

/*
    save user data function with user data
*/
function save(user) {

}

/*
    parse response from server for save user data request
*/
function saveResponse(user) {

}

/*
    logout of application
*/
function logout() {
    global.user = {};
}

// exports
module.exports = {
    login,
    createAccount,
    forgot,
    save,
    logout
};