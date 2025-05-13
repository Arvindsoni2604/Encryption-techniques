import os
import random
from PIL import Image

def gcd(a, b):
    """Computes the greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Computes modular inverse using Extended Euclidean Algorithm."""
    d, x1, x2, y1 = 0, 1, 0, 0
    temp_phi = phi
    while e > 0:
        temp1, temp2 = divmod(temp_phi, e)
        temp_phi, e = e, temp2
        x, y = x2 - temp1 * x1, d - temp1 * y1
        x2, x1, d, y1 = x1, x, y1, y
    return d + phi if d < 0 else d

def is_prime(num):
    """Checks if a number is prime."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_large_prime(bits=16):
    """Generates a large prime number of given bit size."""
    while True:
        num = random.randint(2**(bits-1), 2**bits - 1)
        if is_prime(num):
            return num

def generate_keys():
    """Generates RSA public and private keys."""
    p = generate_large_prime(16)
    q = generate_large_prime(16)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))  # Public and Private keys

def rsa_encrypt_block(block, e, n):
    """Encrypts a single block using RSA."""
    return pow(block, e, n)

def rsa_decrypt_block(block, d, n):
    """Decrypts a single block using RSA."""
    return pow(block, d, n)

def encrypt_image(input_path, output_path, public_key):
    """Encrypts an image using RSA."""
    img = Image.open(input_path)
    img_data = list(img.tobytes())
    
    e, n = public_key
    encrypted_data = [rsa_encrypt_block(pixel, e, n) for pixel in img_data]

    # Save as binary format
    with open(output_path, 'wb') as f:
        for num in encrypted_data:
            f.write(num.to_bytes((n.bit_length() + 7) // 8, byteorder='big'))

def decrypt_image(input_path, output_path, private_key, mode, size):
    """Decrypts an RSA-encrypted image."""
    d, n = private_key
    block_size = (n.bit_length() + 7) // 8  # Determine byte length

    encrypted_data = []
    with open(input_path, 'rb') as f:
        while block := f.read(block_size):
            encrypted_data.append(int.from_bytes(block, byteorder='big'))

    decrypted_data = bytes([rsa_decrypt_block(pixel, d, n) for pixel in encrypted_data])

    img = Image.frombytes(mode, size, decrypted_data)
    img.save(output_path)

# Generate keys
public_key, private_key = generate_keys()

# Example Usage
img = Image.open("pikachu.jpg")
encrypt_image("pikachu.jpg", "encrypted.bin", public_key)
decrypt_image("encrypted.bin", "decrypted.jpg", private_key, img.mode, img.size)
print("RSA Encryption and Decryption Complete!")
