/*
    rsa asymmetric key encryption class
*/

/*
    encrypt message with e, N then call finished function
    uses python function
*/
function rsa_encrypt(e, N, msg, finished) {
    var python = require('child_process').exec('py js_utils/enc/rsa.py ' + e + ' ' + N + " \"" + msg + "\"", function (error, stdout, stderr) {
        finished(stdout);
    });
}

// exports
module.exports = {
    rsa_encrypt
}