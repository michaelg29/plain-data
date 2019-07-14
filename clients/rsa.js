/*
    javascript algorithm to deal with rsa asymmetric key encryption/decryption
*/

function randrange(low, high) {
    return low + (high - low) * Math.random();
}

function powerMod(a, b, n) {
    // TODO: not working as expected (not equal to python pow(a, b, n))

    /*
        return a ^ b % n
        implemented from: http://umaranis.com/2018/07/12/calculate-modular-exponentiation-powermod-in-javascript-ap-n/
    */

    if (n === 1) return 0;
    var result = 1;
    a %= n;
    while (b > 0) {
        if (b % 2 === 1)  //odd number
            result = (result * a) % n;
        b = b >> 1; //divide by 2
        a = (a * a) % n;
    }
    return result;
}

function rabinMiller(n) {
    /*
        return True if n is prime
    */

    var s = n - 1;
    var t = 0;

    while (s % 2 === 0) { // count how many times we have to halve n
        s = Math.floor(s / 2)
        t++;
    }

    for (var trial = 0; trial < 128; trial++) { // try to prove not prime 128 times
        var a = 2 + (n - 3) * Math.random();
        var v = powerMod(a, s, n);
        if (v !== 1) { // test doesn't apply if v == 1
            var i = 0;
            while (v !== n - 1) {
                if (i === t - 1)
                    return false;
                else {
                    i++;
                    v = Math.pow(v, 2) % n;
                }
            }
        }
    }

    return true;
}

function isPrime(n) {
    /*
        return True if n is prime
        resorts to rabinMiller algorithm if uncertain
    */

    if (n < 2) return false; // 0, 1, -ve numbers not prime

    // low prime numbers (< 1000) in order to save time
    var lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997];

    lowPrimes.forEach(element => {
        if (n === element) return true; // if n is a low prime
        if (n % element === 0) return false; // if low primes divide into n
    });

    return rabinMiller(n); // else do rabin miller
}

function gcd(p, q) {
    /*
        euclidean algorithm to determine greatest common divisor of p and q
    */

    while (q !== 0) {
        var temp = q;
        q = p % q;
        p = temp;
    }

    return p;
}

function egcd(a, b) {
    /*
        euclids extended greatest common divisor algorithm
        ax + by = gcd(a, b)
        returns list, result, of size 3:
            result[0] = gcd(a, b)
            result[1] = x
            result[2] = y
    */

    var s = 0;
    var old_s = 1;
    var t = 1;
    var old_t = 0;
    var r = b;
    var old_r = a;

    var quotient;

    while (r !== 0) {
        quotient = Math.floor(old_r / r);
        
        var temp = old_r;
		old_r = r;
		r = temp - quotient * r;

		temp = old_s;
		old_s = s;
		s = temp - quotient * s;

		temp = old_t;
		old_t = t;
		t = temp - quotient * t;
    }

    return [old_r, old_s, old_t];
}

function isCoPrime(p, q) {
    /*
        return True if p and q are coPrime
        if gcd(p, q) == 1
    */

    return gcd(p, q) === 1;
}

function generateLargePrime(keysize=1024) {
    /*
        return a random large prime number of keysize bits in size
    */

    while (true) {
        num = randrange(Math.pow(2, keysize - 1), Math.pow(2, keysize));
        if (isPrime(num)) return num;
    }
}

function modularInverse(a, m) {
    /*
        return modular multiplicative inverse of a and m
        return -1 if dne
    */

    // gcd using euclid's algorithm
    _egcd = egcd(a, m)
    gcd = _egcd[0];
    x = _egcd[1];
    y = _egcd[2];

    if (x < 0)
        x += m

    return x
}

function generateKeys(keysize=1024) {
    /*
        generates encryption and decryption keys of size keysize bits
    */

    var e = d = N = 0;

    // get prime numbers
    var p = generateLargePrime(keysize);
    var q = generateLargePrime(keysize);
    var p = 29;
    var q = 31;

    var N = p * q;
    var phiN = (p - 1) * (q - 1); // number of co-prime numbers 1 <= x <= N

    // choose e (encryption key)
    // e is coprime with phiN
    while (true) {
        e = randrange(Math.pow(2, keysize - 1), Math.pow(2, keysize));
        if (isCoPrime(e, phiN));
            break
    }

    // choose d (decryption key) - modular inverse of e in range m
    d = modularInverse(e, phiN);

    return [ e, d, N ];
}

function encrypt(key, msg) {
    return encrypt(key[0], key[1], msg);
}

function encrypt(e, n, msg) {
    /*
        encrypts msg using encryption key e
    */

    var cypher = "";

    for (var i = 0; i < msg.length; i++) {
        console.log(msg.charCodeAt(i) + " -- " + e + " -- " + N)
        cypher += String(powerMod(msg.charCodeAt(i), e, N)) + " ";
    }

    return cypher
}

function decrypt(key, msg) {
    return decrypt(key[0], key[1], msg);
}

function decrypt(d, n, cypher) {
    console.log("============================")
    /*
        decrypts cypher using decryption key d
    */

    var parts = cypher.split(" ")
    var msg = ""
    parts.forEach(part => {
        if (part) {
            console.log(parseInt(part) + " -- " + d + " -- " + N)
            msg += String.fromCharCode(powerMod(parseInt(part), d, N));
    }});

    return msg
}

// var key = generateKeys(16);
// var e = key[0];
// var d = key[1];
// var N = key[2];

var e = 41863;
var d = 552306247;
var N = 1802204791;

var msg = "Hello, world!";

var cypher = encrypt(e, N, msg);
var txt = decrypt(d, N, cypher);

console.log("e: " + e)
console.log("d: " + d)
console.log("N: " + N)
console.log("msg: " + msg);
console.log("cypher: " + cypher);
console.log("txt: " + txt);