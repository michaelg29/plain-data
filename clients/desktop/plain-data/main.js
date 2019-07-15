const electron = require('electron');
const rsa = require('./js_utils/rsa.js');

const { app, BrowserWindow } = electron;

let mainWindow;

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
    mainWindow.loadURL("index.html");

    // quit app when closed
    mainWindow.on('closed', function() {
        app.quit();
    });
});