var online = false;

var loggedIn = false;

var client = require('./data_client');

var user = {
    "username": "",
    "name": "",
    "uid": ""
};

module.exports = {
    online,
    user,
    loggedIn,
}