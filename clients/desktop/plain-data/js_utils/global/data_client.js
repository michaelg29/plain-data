const rsa = require('../enc/rsa');
const aes = require('../enc/aes');
var net = require('net');

var client;

var validated;
var validationStage;
var rsa_key;
var aes_key;
var msg_ = "";
var response;
var msg_check;
var responseAction = validateServer;
var responded = true;

function sendMsg(msg) {
    client.write(msg + "finished");
    response = {};
}

function encAndSend(msg) {
    aes.encrypt(aes_key, msg, sendMsg);
}

function msgReceived(msg) {
    if (serverValidated) {
        aes.decrypt(aes_key, msg, processMsg);
        return;
    }

    processMsg(msg);
}

function processMsg(msg) {
    responseAction(msg);
    responded = true;
}

function setResponseAction(action) {
    if (responded) {
        responseAction = action;
        responded = false;
        return true;
    }

    return false;
}

function validateServer(msg) {
    try {
        switch (validationStage) {
            case 0:
                // receive public key
                response = JSON.parse(msg);
                rsa_key = [ response['e'], response['N'] ];

                // generate aes key
                aes_key = aes.generateKey(16);

                // send key
                rsa.rsa_encrypt(rsa_key[0], rsa_key[1], aes_key, sendKey);
                
                break;
            case 1:
                // receive decrypted message
                if (msg === msg_check) {
                    validated = true;
                    console.log("server validated");
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

function sendKey(encrypted) {
    msg_check = aes.generateKey(24);

    // encrypt aes key and send
    response = {
        "shared_key": encrypted,
    };

    aes.encrypt(aes_key, msg_check, sendValidationMsg);
}

function sendValidationMsg(msg) {
    response["enc_msg"] = String(msg).substring(2, msg.length - 2);

    sendMsg(JSON.stringify(response));

    validationStage++;
}

function start() {
    client = new net.Socket();
    client.connect(5500, '127.0.0.1', function() {
        msg_check = aes.generateKey(24);

        console.log('Connected');
        
        // send hello message
        response = {
            "name": "Michael",
            "platform": "win32"
        };

        sendMsg(JSON.stringify(response));

        validated = false;
        validationStage = 0;
    });

    client.on('data', function(recv) {
        let data = aes.hex2String(recv);
        if (data.search("finished") === data.length - 8) {
            msg_ += data.substring(0, data.length - 8);
            processMsg(msg_);
            msg_ = "";
        } else {
            msg_ += data;
        }
    });

    client.on('close', function() {
        console.log('disconnected');
    });
}

function cleanup() {
    
}

module.exports = {
    sendMsg,
    encAndSend,
    start,
    cleanup,
    setResponseAction,
};