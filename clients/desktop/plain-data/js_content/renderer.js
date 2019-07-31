const electron = require('electron');
const { ipcRenderer } = electron;
const dialog = electron.remote.dialog;

const jQuery = require('jquery');

// ========================== MENUBAR ======================
const titlebar = require('custom-electron-titlebar');

if (process.platform !== "darwin") {
    new titlebar.Titlebar({
        backgroundColor: titlebar.Color.fromHex('#37474f'),
        icon: './../assets/cgi-bin/icon.png',
        shadow: true
    });
}

// ======================== CONTENT CONTAINER ================================

const routes = {
    "dashboard": "dashboard.html",
    "login": "account/login.html",
    "create_account": "account/create.html",
    "forgot_pwd": "account/forgot.html"
}

// load html content from page
function goto_pg(route) {
    jQuery('#content-container').load(routes[route]);
}

// get signal from backend js to change page
ipcRenderer.on('page:go', function(e, route) {
    goto_pg(route);
});

// ============================= ALERT ==============================
function alert_message(type, title, message) {
    dialog.showMessageBox({
        type: type, // none|info|error|question|warning
        buttons: [ 'OK' ],
        title: title,
        message: message,
    });
}

function sendAlert(alert) {
    ipcRenderer.send(alert);
}

function sendData(message, data) {
    ipcRenderer.send(message, data);
}

function setResponse(trigger, response) {
    ipcRenderer.on(trigger, response);
}

// ============================== CONFIG VALUES ==========================
const config = require('../js_utils/global/config');

function updateAllConfigs() {
    updateConfig("connection");
    updateConfig("account");
}

function updateConfig(property) {
    switch (property) {
        case "connection":
            document.querySelector("#footer-property-connection").innerHTML = "Connection Status: " + (config.online ? "Online" : "Offline");
            break;

        case "account":
                document.querySelector("#footer-property-account").innerHTML = "Account Status: " + (config.loggedIn ? "Logged In" : "Not Logged In");
            break;
    };
}

// ============================== RUNTIME ========================

// on ready
ipcRenderer.send('window:ready');

module.exports = {
    goto_pg,
    updateConfig,
    updateAllConfigs,
    alert_message,
    sendAlert,
    sendData,
    setResponse
}