function rsa_encrypt(e, N, msg, finished) {
    var python = require('child_process').exec('py js_utils/enc/rsa.py ' + e + ' ' + N + " \"" + msg + "\"", function (error, stdout, stderr) {
        finished(stdout);
    });
}

module.exports = {
    rsa_encrypt: rsa_encrypt,
}