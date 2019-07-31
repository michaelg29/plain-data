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