const client = require('./global/data_client');

function login(username, password) {
    let req = {
        "type": "Account",
        "action": "login",
        "values": {
            "username": username,
            "password": password
        }
    }

    client.sendMsg(JSON.stringify(req));
}

module.exports = {
    login
};