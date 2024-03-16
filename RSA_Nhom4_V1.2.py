from math import sqrt
import random
from random import randint as rand

# UCLN
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    
# tra ve gia tri cua d
def mod_inverse(e, phi):
    for x in range(1, phi):
        if (e * x) % phi == 1:
            return x
    return -1


# Kiem tra mot so co la SNT hay khong
def isprime(n):
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True

#========================================================= Generate Key Pair ===================================

# Cho 2 so ngau nhien
p = rand(1, 1000)
q = rand(1, 1000)

# tao cap khoa public - private
def generate_keypair(p, q, keysize):
    # keysize la so bit length cua n nen no phai trong pham vi (Min_n, Max_n+1).
    # x << y  =  x * (2^y)
    # Lam cho p & q co bit- length tuong tu nhau -> tao ra gia tri n kho phan tich thanh p & q

    Min_n = 1 << (keysize - 1) 
    Max_n = (1 << keysize) - 1
    primes = [2]
    # chon 2 SNT trong pham vi (start, stop) & do chenh lech toi da la 2 bit.
    start = 1 << (keysize // 2 - 1)
    stop = 1 << (keysize // 2 + 1)
    
    if start >= stop:
        return []

    for i in range(3, stop + 1, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)
    #list primes
    while (primes and primes[0] < start):
        del primes[0] # delete obj

    # chon p & q
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_values = [q for q in primes if Min_n <= p * q <= Max_n]
        if q_values:
            q = random.choice(q_values)
            break
    print("The value of two prime numbers is: ",p,"and", q)

    # Tinh n & phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    #Tao public key - (e, n) sao cho: 1 < e < phi(n)
    e = random.randrange(1, phi)
    ucln = gcd(e, phi)

    while True:
        # chon e sao cho ucln( e, phi(n)) = 1: SNT cung nhau
        e = random.randrange(1, phi)
        ucln = gcd(e, phi)
        
        # tao private key theo cong thuc: d = e^-1(mod(phi))
        d = mod_inverse(e, phi)
        if ucln == 1 and e != d:
            break

    return ((e, n), (d, n)) # (e, n): public key, (d,n): private key

# =============================================== Encrypt ===================================================
# ma hoa : msg_ciphertext = c ^ e mod n
def encrypt(msg_plaintext, public_key):
    #unpack key value pair
    e, n = public_key
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return msg_ciphertext

#================================================ Decrypt ==================================================
# giai ma: msg_plaintext = c ^ d mod n
def decrypt(msg_ciphertext, private_key):
    d, n = private_key
    msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
    return (''.join(msg_plaintext))

#================================================ main =====================================================

def main():
    bit_length = int(input("Enter bit-length: "))
    print("Generating public/private keypair...\n")
    public, private = generate_keypair(p, q, 2**bit_length) 
    print("Public Key: ", public)
    print("Private Key: ", private)
    #nhap thong diep can ma hoa
    msg = input("\nWrite msg: ")
    print([ord(c) for c in msg]) 
    #ma hoa thong diep voi khoa cong khai
    encrypted_msg = encrypt(msg, public)
    print("\nEncrypted msg: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    #giai ma voi khoa bi mat
    print("\nDecrypted msg: ")
    print(decrypt(encrypted_msg, private))
    

if __name__ == "__main__":
   main()