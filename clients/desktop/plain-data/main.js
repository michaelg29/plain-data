const electron = require('electron');
const client = require('./js_utils/data_client')

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