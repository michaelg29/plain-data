const electron = require('electron');
const path = require('path');

const { app, BrowserWindow, ipcMain, Menu } = electron;
app.setName("Plain Data");

// process.env.NODE_ENV = 'production';

// script utils
const client = require('./js_utils/data_client');

// script content
const menubar = require('./js_content/menubar');

// window variable
let mainWindow;

// app variables
var online = false;
const DEFAULT_PAGE = "dashboard";

// wait for app to be ready
app.on('ready', function() {
    // create window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        },
        icon: __dirname + '/assets/cgi-bin/icon.png',
        frame: process.platform === "darwin",
        title: "Plain Data"
    });

    // load html into window
    mainWindow.loadURL(path.join('file://', __dirname, 'content/index.html'));

    // quit app when closed
    mainWindow.on('closed', () => app.quit());

    mainWindow.webContents.openDevTools();
});

// catch window ready
ipcMain.on('window:ready', function(e) {
    sendMsg('page:go', DEFAULT_PAGE);

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
        mainWindow.webContents.send(code, data);
    }
};

module.exports = {
    sendAlert: this.sendAlert,
    sendMsg: this.sendMsg,
};