const remote = require('electron').remote;
const client = remote.getGlobal('client');
const fs = require('fs');

const renderer = require('../../js_content/renderer');

function upload(atts) {
    let values = {
        "user": remote.getGlobal('user').atts['ID'],
        "author": atts['author'],
        "title": atts['title'],
        "filename": atts['filename'],
        "filetype": atts['filetype'],
        "category": atts['category'],
        "tags": atts['tags']
    };

    // date
    if (atts['date']) {
        values['date'] = atts['date'];
    } else {
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();

        values['date'] = mm + '/' + dd + '/' + yyyy;
    }

    // bytes vs text
    let b_types = [ 'pdf', 'docx', 'pptx', 'csv', 'png', 'jpg', 'mp4' ];
    let t_types = [ 'txt', 'cpp', 'py', 'js', 'html', 'c', 'cs', 'java', 'xml', 'json', 'bat' ];

    if (b_types.indexOf(atts['filetype']) !== -1)
        values['bytes'] = true;
    else
        values['bytes'] = false;

    // read file
    try {
        fs.readFile(atts['filepath'], function(err, data) {
            values['content'] = data;
            values['filesize'] = data.length;

            sendFileToServer(values);
        });
    } catch (error) {
        console.log(error);
    }
}

function sendFileToServer(values) {
    let req = {
        "type": "file",
        "action": "upload",
        "values": values
    };

    client.setResponseAction(uploadResponse);
    client.encAndSend(req);
}

function uploadResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'File uploaded', 'You have successfully uploaded the file!');
    } else {
        renderer.sendData('upload:failed', msg['reasons']);
    }
}

module.exports = {
    upload
}