from cryptography.fernet import Fernet
import cryptography.fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from colorama import Fore
import base64, cryptography

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    try:
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key
    except:
        write_key()
        print("New key created due to not existing key")
        load_key()

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    # Key Derivation Function
    kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=salt, iterations=100000)

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def decrypt_derive_key_from_password():
    derive_key_from_password()

master_psw = input("What is the master password? ")
key = load_key()
fer = Fernet(derive_key_from_password(master_psw, key))

def view():
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            try:
                data = line.rstrip()
                user, passw = data.split("|")
                print(Fore.GREEN+"User:", user, "| Password:", fer.decrypt(passw.encode()).decode()+Fore.RESET)
            except cryptography.fernet.InvalidToken:
                print(Fore.RED+"You do not have the Master password to read this password :)"+Fore.RESET)

def add():
    name = input('Account Name: ')
    pwd = input("Password: ")

    if '|' in name or '|' in pwd:
        print(Fore.RED+"Name and Password must not include '|' please insert another one :)"+Fore.RESET)
        add()
    else:
        with open('passwords.txt', 'a') as f:
            f.write(name + "|" + fer.encrypt((pwd).encode()).decode() + "\n")
        print(Fore.GREEN+"Name and password saves successfully"+Fore.RESET)

if __name__ == '__main__':
    while True:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
        if mode == "q":
            break

        if mode == "view":
            view()
        elif mode == "add":
            add()
        else:
            print("Invalid mode.")
            continue