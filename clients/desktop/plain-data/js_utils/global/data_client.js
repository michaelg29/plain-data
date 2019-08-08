/*
    data client class
*/

const rsa = require('../enc/rsa');
const aes = require('../enc/aes');
var net = require('net');
const window = require('electron').BrowserWindow;

// client socket object
var client;

// metadata variables
var validated;
var validationStage;
var rsa_key;
var aes_key;
var msg_ = "";
var msg = [];
var response;
var msg_check;
var responseAction = validateServer;
var currentReqId = "";

/*
    send message to server
*/
function sendMsg(msg) {
    client.write(msg + "finished");
    response = {};
}

/*
    encrypt and send message to server with aes
*/
function encAndSend(msg) {
    currentReqId = msg['reqId'] = genReqId();

    aes.encrypt(aes_key, JSON.stringify(msg), sendMsg);
}

/*
    received message callback
*/
function msgReceived(msg) {
    if (validated) {
        aes.decrypt(aes_key, msg, processMsg);
        return;
    }

    processMsg(msg);
}

/*
    secondary message processing
*/
function processMsg(msg) {
    let json_parse = validated ? JSON.parse(msg) : msg;

    var idMatch = json_parse['reqId'] === currentReqId;
    currentReqId = "";

    if (idMatch || !validated) {
        responseAction(json_parse);
        window.getFocusedWindow().webContents.send('loading-animation:stop');
    } else {
        console.log("communications error");
    }
}

/*
    set function for tertiary processing if no current action on queue
*/
function setResponseAction(action) {
    if (currentReqId === "") {
        responseAction = action;
        window.getFocusedWindow().webContents.send('loading-animation:start');
        return true;
    }

    return false;
}

/*
    generate a request id as a random string
*/
function genReqId() {
    return aes.generateKey(24);
}

/*
    server validation process
*/
function validateServer(msg) {
    try {
        switch (validationStage) {
            case 0:
                // receive public key
                response = JSON.parse(msg);
                rsa_key = [ response['e'], response['N'] ];
                console.log("received public key");

                // generate aes key
                aes_key = aes.generateKey(16);

                // send key
                rsa.rsa_encrypt(rsa_key[0], rsa_key[1], aes_key, sendKey);
                
                break;
            case 1:
                // receive decrypted message
                console.log("received decrypted message");
                if (msg === msg_check) {
                    validated = true;
                    console.log("server validated");
                    global.online = true;
                    window.getFocusedWindow().webContents.send('update:config', 'connection');
                } else {
                    client.destroy();
                    console.log("server failed validation");
                }

                break;
        }
    } catch (err) {
        console.log(err);
        client.destroy();
    }
}

// send aes key to server
function sendKey(encrypted) {
    msg_check = aes.generateKey(24);

    // encrypt aes key and send
    response = {
        "shared_key": encrypted,
    };

    aes.encrypt(aes_key, msg_check, sendValidationMsg);
}

// send aes encrypted message to server
function sendValidationMsg(msg) {
    response["enc_msg"] = msg; 

    sendMsg(JSON.stringify(response));
    console.log("sent validation message");

    validationStage++;
}

/*
    initialize client connection and start validation
*/
function start() {
    client = new net.Socket();
    // connect
    client.connect(5500, '127.0.0.1', function() {
        msg_check = aes.generateKey(24);

        console.log('Connected');
        
        // send hello message
        response = {
            "name": "Michael",
            "platform": "win32"
        };

        sendMsg(JSON.stringify(response));
        console.log("sent hello message");

        validated = false;
        validationStage = 0;
    });

    /*
        initial message processing
        eg. decryption, sizing, etc.
    */
    client.on('data', function(recv) {
        if (validated) {
            var last8 = [];
            for (var i = recv.length - 8; i < recv.length; i++)
                last8.push(recv[i]);

            if (aes.decode(last8) === "finished") {
                for (var i = 0; i < recv.length - 8; i++)
                    msg.push(recv[i]);
                msgReceived(msg);
                msg = [];
            } else {
                for (var i = 0; i < recv.length; i++)
                    msg.push(recv[i]);
            }
        } else {
            let data = aes.decode(recv);
            if (data.search("finished") === data.length - 8) {
                msg_ += data.substring(0, data.length - 8);
                msgReceived(msg_);
                msg_ = "";
            } else {
                msg_ += data;
            }
        }
    });

    // on client close
    client.on('close', function() {
        console.log('disconnected');
        global.online = false;
        if (window.getFocusedWindow())
            window.getFocusedWindow().webContents.send('update:config', 'connection');
    });
}

/*
    cleanup client
*/
function cleanup() {
    client.destroy();
}

// exports
module.exports = {
    sendMsg,
    encAndSend,
    start,
    cleanup,
    setResponseAction,
    genReqId,
};