import sys
sys.path.append(r"C:\src\business-library\python")

import mundusinvicte.security.aes as aes

mode = sys.argv[1]

if mode == "ENCRYPT":
    print(aes.encrypt(sys.argv[2], sys.argv[3]))
elif mode == "DECRYPT":
    print(aes.decrypt(sys.argv[2], sys.argv[3]))
else:
    print("invalid mode")

sys.stdout.flush()