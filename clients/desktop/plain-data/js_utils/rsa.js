var rsa = require("node-bignumber");

function rsa_encrypt(e, N, msg) {
    var pub = new rsa.Key();
    pub.setPublic(key_N, key_e);

    return pub.encrypt(msg);
}

module.exports = {
    rsa_encrypt: rsa_encrypt,
}