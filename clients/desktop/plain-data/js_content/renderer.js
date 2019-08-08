/*
    renderer process
*/

const electron = require('electron');
const { ipcRenderer, remote } = electron;
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
    "forgot_pwd": "account/forgot.html",

    "file_upload": "files/upload.html",
    "file_search": "files/search.html",

    "board": "board/board.html",
    "board_search": "board/search.html",
    "board_create": "board/create.html",
}

/*
    load html content from page to content container
*/
function goto_pg(route) {
    jQuery('#content-container').load(routes[route]);
    updateLinks();
}

/*
    get signal from backend js to change page
*/
ipcRenderer.on('page:go', function(e, route) {
    goto_pg(route);
});

// ============================= ALERT ==============================

/*
    show alert as dialog
*/
function alert_message(type, title, message) {
    dialog.showMessageBox({
        type: type, // none|info|error|question|warning
        buttons: [ 'OK' ],
        title: title,
        message: message,
    });
}

/*
    send alert to backend
*/
function sendAlert(alert) {
    ipcRenderer.send(alert);
}

/*
    send data to backend
*/
function sendData(message, data) {
    ipcRenderer.send(message, data);
}

/*
    set response to a certain event
*/
function setResponse(trigger, response) {
    ipcRenderer.on(trigger, response);
}

/*
    trigger an event in frontend
*/
function trigger(event) {
    remote.BrowserWindow.getFocusedWindow().webContents.send(event);
}

/*
    trigger event with data
*/
function triggerWithData(event, data) {
    try {
        remote.BrowserWindow.getFocusedWindow().webContents.send(event, data);
    } catch (error) {
        console.log(error);
    }
}

// ============================== CONFIG VALUES ==========================

/*
    update all existing configurations
*/
function updateAllConfigs() {
    updateConfig("connection");
    updateConfig("account");
}

/*
    updates configuration value in gui
*/
function updateConfig(property) {
    switch (property) {
        case "connection":
            document.querySelector("#footer-property-connection").innerHTML = "Connection Status: " + (electron.remote.getGlobal('online') ? "Online" : "Offline");
            break;

        case "account":
            document.querySelector("#footer-property-account").innerHTML = "Account Status: " + (electron.remote.getGlobal('loggedIn').val ? "Logged In" : "Not Logged In");
            break;
    };
}

/*
    callback to configuration update message
*/
ipcRenderer.on('update:config', (e, config) => updateConfig(config));

/*
    callback to update all configurations message
*/
ipcRenderer.on('update:configs_all', () => updateAllConfigs());

// ============================== RUNTIME ========================

// set window ready
ipcRenderer.send('window:ready');

/*
    parse links to files and boards in gui
*/
function updateLinks() {
    let links = document.getElementsByTagName('a');
    
    for (var i = 0; i < links.length; i++) {
        item = links[i];
        let src = item.getAttribute('tar');
    
        if (src && src.indexOf('/') !== -1) {
            let type = src.substring(0, src.indexOf('/'));
            let id = src.substring(src.indexOf('/') + 1);
    
            switch (type) {
                case "file":
                    item.setAttribute('onclick', `renderer.retrieveFile(${id}, ${item.hasAttribute('download')})`);
                case "board":
                    break;
            }
        }
    }
}

/*
    retrieve file from server
*/
function retrieveFile(id, download = false) {
    const file = require('./../js_utils/models/file');
    file.download(id, download);
}

/*
    retrieve board from server
*/
function retrieveBoard(id, newWindow = true) {

}

// exports
module.exports = {
    goto_pg,
    updateConfig,
    updateAllConfigs,
    alert_message,
    sendAlert,
    sendData,
    setResponse,
    trigger,
    triggerWithData,
    retrieveFile,
    retrieveBoard,
    updateLinks
}