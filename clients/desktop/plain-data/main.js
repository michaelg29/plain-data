const electron = require('electron');
const url = require('url');
const path = require('path');

const client = require('./js_utils/data_client')

const { app, BrowserWindow, ipcMain } = electron;

let mainWindow;

var online = false;

// wait for app to be ready
app.on('ready', function() {
    // create window
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    // load html into window
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'content/index.html'),
        protocol: 'file:',
        slashes: true,
    }));

    // quit app when closed
    mainWindow.on('closed', function() {
        app.quit();
    });

    sendMsg('page:go','dashboard');
});

// catch window ready
ipcMain.on('window:ready', function(e) {
    //client.start();
});

// before exiting
app.on('before-quit', function() {
    //client.cleanup();
})

// on quit
app.on('quit', function() {
    
});

sendAlert = function(code) {
    if (mainWindow) {
        mainWindow.webContents.send(code);
    }
};

sendMsg = function(code, data) {
    if (mainWindow) {
        console.log("sent");
        mainWindow.webContents.send(code, data);
    }
};

module.exports = {
    sendAlert: this.sendAlert,
    sendMsg: this.sendMsg,
};