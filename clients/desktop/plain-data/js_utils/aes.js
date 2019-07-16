const crypto = require('crypto');

function generateKey(size) {
    var key = "";
    var code = "\"";

    // generate size characters by converting random ints [33, 126] into characters
    for (var i = 0; i < size; i++) {
        while (code === "'" || code === '"')
            code = String.fromCharCode(Math.floor(33 + (126 - 33) * Math.random()));

        key += code;
        code = "'";
    }

    return key;
}

function generateVector() {
    return crypto.randomBytes(16);
}

function encrypt(key, text, alg, iv, encoding) {
    var cipher = crypto.createCipheriv(alg, key, iv);

    encoding = encoding || "binary";

    var result = cipher.update(text, "utf8", encoding);
    result += cipher.final(encoding);

    return result;
}

function decrypt(key, text, alg, iv, encoding) {
    var decipher = crypto.createDecipheriv(alg, key, iv);

    encoding = encoding || "binary";

    var result = decipher.update(text, encoding);
    result += decipher.final();

    return result;
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
    generateVector: generateVector,
    encrypt: encrypt,
    decrypt: decrypt,
    hex2String: hex2String,
};