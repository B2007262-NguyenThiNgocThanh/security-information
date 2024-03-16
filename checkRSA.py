from math import sqrt
import random
from random import randint as rand

# UCLN use euclidean algorithm, Use iteration to make it faster for larger integers
# def gcd(a, b):
#     while b != 0:
#         a, b = b, a % b
#     return a

def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

# kiem tra mot so la SNT hay khong
def is_prime(num):
    if num == 2:
        return True
    elif num < 2 or num % 2 == 0:
        return False
    else:
        for i in range(2, int(sqrt(num)) + 1, 2): 
            if num % i == 0:
                return False
    return True

# Tao cap khoa : public key - private key
def generate_keypair(p, q):
    # kt SNT
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.') #exception xu ly ngoai le
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #tinh val Euler function 
    phi_n = (p-1) * (q-1)

    #chon 1 so nguyen e sao cho (e, n) la SNT cung nhau
    e = random.randrange(1, phi_n)
    g = gcd(e, phi_n) #kt tra SNT(e,n)
    while g != 1:
        e = random.randrange(1, phi_n)
        g = gcd(e, phi_n)

    # Dung thuat toan euclid mo rong de tao -> private key
    d = multiplicative_inverse(e, phi_n)
    
    
    # Kq tra ve: Public key - (e, n) and private key - (d, n)
    return ((e, n), (d, n))


def encrypt(package, plaintext):
    #Unpack the key into it's components
    e, n = package
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    msg_cipher = [pow(ord(c), e, n) for c in plaintext]
    #[(ord(char) ** key) % n for char in plaintext]
    #Return the array of bytes
    return msg_cipher

def decrypt(package, msg_ciphertext):
    #Unpack the key into its components
    d, n = package
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
    # [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return (''.join(msg_plaintext))
    

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print("RSA Encrypter/ Decrypter")
    p = int(input("Nhập mốt số nguyên tố : "))
    q = int(input("\nNhập một số nguyên tố khác : "))
    print("\nĐang tạo cặp khóa công khai / bí mật của bạn . . .")
    public, private = generate_keypair(p, q)
    print("\Khóa công khai của bạn là : ", public ,"\nKhóa bí mật của bạn là : ", private)
    message = input("Nhập thông điệp cần mã hóa với khóa bí mật của bạn : ")
    encrypted_msg = encrypt(private, message)
    print("\nThông điệp đã mã hóa của bạn là: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("\nDecrypting message with public key ", public ," . . .")
    print("\nThông điệp đã giải mã là :")
    print(decrypt(public, encrypted_msg))