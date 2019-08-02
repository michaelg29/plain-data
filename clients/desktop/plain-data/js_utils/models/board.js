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

}

function comment(atts) {
    let req = {
        "type": "board",
        "action": "comment",
        "values": atts
    }

    client.setResponseAction(commentResponse);
    client.encAndSend(req);
}

function commentResponse(msg) {

}

module.exports = {
    create,
    search,
    comment
}