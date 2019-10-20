/*
    board class
*/

const remote = require('electron').remote;
const client = remote.getGlobal('client');

const renderer = require('../../js_content/renderer');

/*
    create board function with metadata
*/
function create(atts) {
    let req = {
        "type": "board",
        "action": "create",
        "values": atts
    }

    var reqId = client.setResponseAction(createResponse);
    client.encAndSend(reqId, req);
}

/*
    parse server response for create board request
*/
function createResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
        renderer.alert_message('info', 'Board created', 'You have successfully created the board!');
    } else {
        renderer.triggerWithData('create:failed', msg['reasons']);
    }
}

/*
    board search function with parameters
*/
function search(atts) {
    let req = {
        "type": "board",
        "action": "search",
        "values": atts
    }

    var reqId = client.setResponseAction(searchResponse);
    client.encAndSend(reqId, req);
}

/*
    parse server response for board search request
*/
function searchResponse(msg) {
    if (msg['response']) {
        renderer.triggerWithData('board:search:results', msg['list']);
    } else {
        renderer.triggerWithData('search:failed', msg['reasons']);
    }
}

/*
    comment function with board id, subject of comment, and comment content
*/
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

    var reqId = client.setResponseAction(commentResponse);
    client.encAndSend(reqId, req);
}

/*
    parse server response for board comment request
*/
function commentResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('dashboard');
    } else {
        renderer.triggerWithData('comment:failed', msg['reasons']);
    }
}

/*
    retrieve board from server with specified id
*/
function retrieve(id) {
    let req = {
        "type": "board",
        "action": "retrieve",
        "values": {
            "id": id
        }
    }

    var reqId = client.setResponseAction(retrieveResponse);
    client.encAndSend(reqId, req);
}

/*
    parse server response for board retrieval request
*/
function retrieveResponse(msg) {
    if (msg['response']) {
        renderer.goto_pg('board');
        renderer.triggerWithData('board:loaded', msg['values']);
    } else {
        renderer.triggerWithData('comment:failed', msg['reasons']);
    }
}

// exports
module.exports = {
    create,
    search,
    comment,
    retrieve
}