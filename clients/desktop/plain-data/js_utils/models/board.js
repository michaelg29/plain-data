const remote = require('electron').remote;
const client = remote.getGlobal('client');

const renderer = require('../../js_content/renderer');

function create(atts) {
    let req = {
        "type": "board",
        "action": "create",
        "values": atts
    }

    client.setResponseAction(createResponse);
    client.encAndSend(req);
}

function createResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Board created', 'You have successfully created the board!');
    } else {
        renderer.triggerWithData('create:failed', msg['reasons']);
    }
}

function search(atts) {
    let req = {
        "type": "board",
        "action": "search",
        "values": atts
    }

    client.setResponseAction(searchResponse);
    client.encAndSend(req);
}

function searchResponse(msg) {
    if (msg['response']) {
        renderer.triggerWithData('board:search:results', msg['list']);
    } else {
        renderer.triggerWithData('search:failed', msg['reasons']);
    }
}

function comment(bid, subject, content) {
    let req = {
        "type": "board",
        "action": "comment",
        "values": {
            "id": bid,
            "subject": subject,
            "content": content,
            "uid": remote.getGlobal('user').atts['ID'],
            "name": remote.getGlobal('user').atts['Username']
        }
    }

    client.setResponseAction(commentResponse);
    client.encAndSend(req);
}

function commentResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
    } else {
        renderer.triggerWithData('comment:failed', msg['reasons']);
    }
}

function retrieve(id) {
    let req = {
        "type": "board",
        "action": "retrieve",
        "values": {
            "id": id
        }
    }

    client.setResponseAction(retrieveResponse);
    client.encAndSend(req);
}

function retrieveResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('board');
        renderer.triggerWithData('board:loaded', msg['values']);
    } else {
        renderer.triggerWithData('comment:failed', msg['reasons']);
    }
}

module.exports = {
    create,
    search,
    comment,
    retrieve
}