const electron = require('electron');
const jQuery = require('jquery');
const { ipcRenderer, remote } = electron;

const titlebar = require('custom-electron-titlebar');

if (process.platform !== "darwin") {
    new titlebar.Titlebar({
        backgroundColor: titlebar.Color.fromHex('#37474f'),
        icon: './../assets/cgi-bin/icon.png',
        shadow: true
    });
}

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

// on ready
ipcRenderer.send('window:ready');

module.exports = {
    goto_pg,
}