const electron = require('electron');

// process.env.NODE_ENV = 'production';

// script utils
const client = require('./js_utils/data_client');

const menubar = require('./js_content/menubar');

const { app, BrowserWindow, ipcMain, Menu } = electron;

let mainWindow;

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
        frame: false,
        show: false
    });

    // load html into window
    mainWindow.loadURL(__dirname + '/content/index.html');

    mainWindow.once('ready-to-show', function() {
        return mainWindow.show(); 
    });

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