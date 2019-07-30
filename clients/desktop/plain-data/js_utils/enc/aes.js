const crypto = require('crypto');

function generateKey(size) {
    var key = "";
    var code = '"';

    // generate size characters by converting random ints [33, 126] into characters
    for (var i = 0; i < size; i++) {
        while (code === "'" || code === '"')
            code = String.fromCharCode(Math.floor(33 + (126 - 33) * Math.random()));

        key += code;
        code = "'";
    }

    return key;
}

function encrypt(key, text, finished) {
    var python = require('child_process').exec('python js_utils/enc/aes.py ENCRYPT "' + key + '" "' + text + '"', function (error, stdout, stderr) {
        finished(done);
    });
}

function decrypt(key, text, finished) {
    var python = require('child_process').exec('python js_utils/enc/aes.py DECRYPT "' + key + '" "' + text + '"', function (error, stdout, stderr) {
        finished(stdout);
    });
}

function hex2String(array) {
    var result = "";
    for (var i = 0; i < array.length; i++) {
        result += String.fromCharCode(parseInt(array[i]));
    }
    return result;
}

module.exports = {
    generateKey: generateKey,
    encrypt: encrypt,
    decrypt: decrypt,
    hex2String: hex2String,
};