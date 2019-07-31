const aesjs = require('aes-js');

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

// function encrypt(key, text, finished) {
//     var python = require('child_process').exec('python js_utils/enc/aes.py ENCRYPT "' + key + '" "' + text + '"', function (error, stdout, stderr) {
//         console.log("Key:",key)
//         console.log("text:",text)
//         console.log("enc:",typeof(stdout),stdout.substring(2, stdout.length - 3))
//         decrypt(key, stdout.substring(2, stdout.length - 3), () => {})
//         finished(stdout.substring(2, stdout.length - 3));
//     });
// }

// function decrypt(key, text, finished) {
//     var python = require('child_process').exec('python js_utils/enc/aes.py DECRYPT "' + key + '" "' + text + '"', function (error, stdout, stderr) {
//         console.log('dec:',typeof(stdout), stdout);
//         finished(stdout.substring(2, stdout.length - 3));
//     });
// }

function encrypt(key, text, finished) {
    var aesCtr = new aesjs.ModeOfOperation.ctr(encode(key));
    var textBytes = aesjs.utils.utf8.toBytes(text);

    var encryptedBytes = aesCtr.encrypt(textBytes);

    finished(encryptedBytes);
}

function decrypt(key, encryptedBytes, finished) {
    var aesCtr = new aesjs.ModeOfOperation.ctr(encode(key));
    var decryptedBytes = aesCtr.decrypt(encryptedBytes);

    var decryptedText = aesjs.utils.utf8.fromBytes(decryptedBytes);

    finished(decryptedText);
}

function decode(bytes) {
    return aesjs.utils.utf8.fromBytes(bytes);
}

function encode(text) {
    return aesjs.utils.utf8.toBytes(text);
}

module.exports = {
    generateKey,
    encrypt,
    decrypt,
    decode,
    encode
};