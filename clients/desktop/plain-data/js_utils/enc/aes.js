/*
    aes symmetric key encryption class
*/

const aesjs = require('aes-js');

/*
    generate key of specified byte size
*/
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

/*
    encrypt text with key then call finished function
*/
function encrypt(key, text, finished) {
    var aesCtr = new aesjs.ModeOfOperation.ctr(encode(key));
    var textBytes = aesjs.utils.utf8.toBytes(text);

    var encryptedBytes = aesCtr.encrypt(textBytes);

    finished(encryptedBytes);
}

/*
    decrypt cypher with key then call finished function
*/
function decrypt(key, encryptedBytes, finished) {
    var aesCtr = new aesjs.ModeOfOperation.ctr(encode(key));
    var decryptedBytes = aesCtr.decrypt(encryptedBytes);

    var decryptedText = aesjs.utils.utf8.fromBytes(decryptedBytes);

    finished(decryptedText);
}

/*
    decode bytes with utf8 encoding
*/
function decode(bytes) {
    return aesjs.utils.utf8.fromBytes(bytes);
}

/*
    encode string with utf8 encoding
*/
function encode(text) {
    return aesjs.utils.utf8.toBytes(text);
}

// exports
module.exports = {
    generateKey,
    encrypt,
    decrypt,
    decode,
    encode
};