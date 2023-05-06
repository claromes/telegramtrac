# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def crypt_code(code, api_id):
    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX)

    sign_in_code = code.encode()

    ciphertext, tag = cipher.encrypt_and_digest(sign_in_code)

    file_out = open('sign_in/encrypted_code_{}.bin'.format(api_id), 'wb')
    for i in (key, cipher.nonce, tag, ciphertext):
        file_out.write(i)
    file_out.close()

def crypt_password(password, api_id):

    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX)

    sign_in_password = password.encode()

    ciphertext, tag = cipher.encrypt_and_digest(sign_in_password)

    file_out = open('sign_in/encrypted_password_{}.bin'.format(api_id), 'wb')
    for i in (key, cipher.nonce, tag, ciphertext):
        file_out.write(i)
    file_out.close()

def decrypt_code(api_id):
    file_in = open('sign_in/encrypted_code_{}.bin'.format(api_id), 'rb')
    key, nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, 16, -1) ]
    file_in.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    sign_in_code_decrypt = cipher.decrypt_and_verify(ciphertext, tag)

    sign_in_code_decode = sign_in_code_decrypt.decode()

    return sign_in_code_decode

def decrypt_password(api_id):
    file_in = open('sign_in/encrypted_password_{}.bin'.format(api_id), 'rb')
    key, nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, 16, -1) ]
    file_in.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    sign_in_password_decrypt = cipher.decrypt_and_verify(ciphertext, tag)

    sign_in_password_decode = sign_in_password_decrypt.decode()

    return str(sign_in_password_decode)
