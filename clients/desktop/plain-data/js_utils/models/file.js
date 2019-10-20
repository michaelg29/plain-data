/*
    file class
*/

const remote = require('electron').remote;
const client = remote.getGlobal('client');
const fs = require('fs');

const renderer = require('../../js_content/renderer');

/*
    upload file function with attributes
*/
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

        values['date'] = `${mm}/${dd}/${yyyy}`;
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

            let req = {
                "type": "file",
                "action": "upload",
                "values": values
            };
        
            var reqId = client.setResponseAction(uploadResponse);
            client.encAndSend(reqId, req);
        });
    } catch (error) {
        console.log(error);
    }
}

/*
    parse server response for file upload request
*/
function uploadResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'File uploaded', 'You have successfully uploaded the file!');
    } else {
        renderer.sendData('upload:failed', msg['reasons']);
    }
}

/*
    file search function with parameters
*/
function search(atts) {
    let req = {
        "type": "file",
        "action": "search",
        "values": atts
    }

    var reqId = client.setResponseAction(searchResponse);
    client.encAndSend(reqId, req);
}

/*
    parse server response for file search request
*/
function searchResponse(msg) {
    if (msg['response']) {
        renderer.triggerWithData('search:results', msg['list']);
    } else {
        renderer.triggerWithData('search:failed', msg['reasons']);
    }
}

/*
    file download function with specified id
*/
function download(id, downloadToDrive = false) {
    let req = {
        "type": "file",
        "action": "download",
        "values": {
            "fid": id
        }
    }

    if (downloadToDrive) {
        var reqId = client.setResponseAction(downloadToDriveResponse);
        client.encAndSend(reqId, req);
    } else {
        var reqId = client.setResponseAction(downloadContentResponse);
        client.encAndSend(reqId, req);
    }

    client.encAndSend(req);
}

/*
    parse server response for file download request if only opening file from temproary location
*/
function downloadContentResponse(msg) {
    if (msg['response']) {
        var filepath = __dirname + '\\tmp\\' + msg['values']['filepath'];

        writeFile(msg['values']['content'], filepath);

        msg['values']['content'] = null;
        msg['values']['src'] = `file://${filepath}`;

        var child = require('child_process').exec(`${filepath}`);
    } else {
        renderer.alert_message('error', 'Failure', 'File could not be downloaded.');
    }
}

/*
    parse server response for file download request if downloading file to hard drive
*/
function downloadToDriveResponse(msg) {
    if (msg['response']) {
        var filepath = electron.remote.app.getPath('home') + '/downloads/' + msg['values']['filepath'];

        writeFile(msg['values']['content'], filepath);

        renderer.alert_message('info', 'Success', 'File downloaded to downloads folder!');
    } else {
        renderer.alert_message('error', 'Failure', 'File could not be downloaded.');
    }
}

/*
    general write file function
*/
function writeFile(content, filepath) {
    var content_b = Buffer.from(content, 'utf8');
    fs.writeFile(filepath, content_b, function(err) {
        if (err) {
            console.log(err);
            renderer.alert_message('error', 'Failure', 'File could not be downloaded.');
        }
    });
}

// exports
module.exports = {
    upload,
    search,
    download
}