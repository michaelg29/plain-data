const electron = require('electron');

const client = require('./js_utils/data_client')

const { app, BrowserWindow, ipcMain } = electron;

let mainWindow;

var online = false;

const DEFAULT_PAGE = "dashboard";

// wait for app to be ready
app.on('ready', function() {
    // create window
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        },
        icon: __dirname + '/assets/cgi-bin/icon.png',
    });

    // load html into window
    mainWindow.loadURL(__dirname + '/content/index.html');

    // quit app when closed
    mainWindow.on('closed', function() {
        app.quit();
    });
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