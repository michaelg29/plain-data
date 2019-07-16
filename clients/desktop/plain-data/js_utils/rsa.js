function rsa_encrypt(e, N, msg, finished) {
    ret = "";
    var python = require('child_process').exec('py js_utils/rsa.py ' + e + ' ' + N + " \"" + msg + "\"", function (error, stdout, stderr) {
        finished(stdout);
    });
    console.log("executed");
}

module.exports = {
    rsa_encrypt: rsa_encrypt,
}