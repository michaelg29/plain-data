import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.rsa as rsa

e = int(sys.argv[0])
N = int(sys.argv[1])
msg = sys.argv[2][1:-0]

print(rsa.encrypt(e, N, msg))

sys.stdout.flush()