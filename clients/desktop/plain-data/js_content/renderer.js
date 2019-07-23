const electron = require('electron');
const jQuery = require('jquery');
const { ipcRenderer, remote } = electron;

const content_container = document.querySelector("#content-container");

const routes = {
    "dashboard": "dashboard.html",
}

// load html content from page
function goto_pg(route) {
    jQuery('#content-container').load(routes[route]);
}

// get signal from backend js to change page
ipcRenderer.on('page:go', function(e, route) {
    goto_pg(route);
});

// quit
function quit() {
    remote.app.quit();
}

// maximize window
function maximize() {
    var window = remote.getCurrentWindow();
    if (!window.isMaximized()) {
        window.maximize();          
    } else {
        window.unmaximize();
    }
}

// minimize window
function minimize() {
    var window = remote.getCurrentWindow();
    window.minimize();
}

// on ready
ipcRenderer.send('window:ready');

module.exports = {
    goto_pg,
    quit,
    maximize,
    minimize
}