from cryptography.fernet import Fernet

cipher_key = b'EQlqpKkBOy9bGPJx9bfC-fjUlaPYOJrkDqjfSt6My5Y='
cipher = Fernet(cipher_key)


def gen_account():
    login = bytes(input('LOGIN: ').strip(), 'utf-8')
    password = bytes(input('PASSWORD: ').strip(), 'utf-8')
    encrypted_login = cipher.encrypt(login)
    encrypted_password = cipher.encrypt(password)
    decrypted_login = cipher.decrypt(encrypted_login).decode()
    decrypted_password = cipher.decrypt(encrypted_password).decode()
    print(decrypted_login, decrypted_password)
    print(encrypted_login, encrypted_password)


if __name__ == '__main__':
    gen_account()
