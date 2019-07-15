function rsa_encrypt(e, N, msg) {
    var python = require('child_process').spawn('python', ['./rsa.py', String(e), String(N), "\"" + msg + "\""]);
    python.stdout.on('data',function(data){
        console.log("data: ",data.toString('utf8'));
    });
}

module.exports = {
    rsa_encrypt: rsa_encrypt,
}