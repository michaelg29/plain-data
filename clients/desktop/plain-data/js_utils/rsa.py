import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.rsa as rsa

e = int(sys.argv[1])
N = int(sys.argv[2])
msg = sys.argv[3]

print(rsa.encrypt(e, N, msg))

sys.stdout.flush()