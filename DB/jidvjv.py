from cryptography.fernet import Fernet
import sqlite3, getpass
from colorama import Fore

#password = getpass.getpass("Enter password: ")
# key = Fernet.generate_key()
key = b'9pMsjdi84caLcW_kOW_Nk2d2nPuHwD26LACoADGZin8='
f = Fernet(key)
#encrypted_pass = f.encrypt(password.encode()).decode()

conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()
cursor.execute('''
               create table if not exists password(
               id integer PRIMARY KEY autoincrement not null,
               website TEXT NOT NULL,
               username TEXT UNIQUE NOT NULL,
               password TEXT UNIQUE NOT NULL)
               ''')
cursor.execute('''
               create table if not exists user(
               id integer PRIMARY key autoincrement NOT NULL,
               username TEXT UNIQUE NOT NULL,
               password TEXT UNIQUE NOT NULL)
''')

def register():
    username = input("Enter your username: ")
    user_password = input("Enter your password: ") #getpass.getpass("Enter your password: ")
    encrypted_pass = f.encrypt(user_password.encode()).decode()

    try:
        cursor.execute(f"SELECT password FROM user")
        for password in cursor.fetchall():
            password = f.decrypt(password[0]).decode()
            if password == user_password:
                print(Fore.RED + "username/password are/is already taken\nPlease set another ones" + Fore.RESET)
                register()
                quit()
        cursor.execute("INSERT INTO user (username, password) VALUES (?,?)", (username, encrypted_pass))
        conn.commit()
        print(Fore.GREEN + "Registered successfully" + Fore.RESET)
    except sqlite3.IntegrityError:
        print(Fore.RED + "username/password are/is already taken\nPlease set another ones" + Fore.RESET)
        register()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute(f"SELECT password FROM USER where username = '{username}'")
    u_password = cursor.fetchone()[0]
    user_password = f.decrypt(u_password).decode()
    
    if password == user_password:
        user_id = cursor.execute(f"SELECT id FROM user WHERE password = '{u_password}'")
        user_id = cursor.fetchall()[0][0]
        return True, user_id
    else:
        return False, None

def app():
    print("""          1 => Login
          2 => Register
          3 => Exit""")
    
    user_input = input("Select action: ")
    
    if user_input == '1':
        try:
            verification, user_id = login()
            if verification:
                cursor.execute(f"SELECT username, password FROM user WHERE id = {user_id}")
                info = cursor.fetchone()
                print(Fore.GREEN + f"logges in successfully with:\nuser id: {user_id}\nusername: {info[0]}\npassword: {f.decrypt(info[1]).decode()}" + Fore.RESET)
                print("""                1 => Change profile
                2 => Delete Profile
                3 => Quit""")
                user_input = input("Select action: ")
            else:
                print(Fore.RED + "Password is wrong\nPlease try again" + Fore.RESET)
                app()

            if user_input == '1':
                user_input = input("1 => Change username\n2 => Change password\n3 => Change username and password\nSelect action: ")
                if user_input == '1':
                    cursor.execute(f"UPDATE user SET username = '{input("Enter your new user name: ")}' WHERE id = {user_id}")
                elif user_input == '2':
                    new_password = input("Enter your new password: ")
                    cursor.execute(f"UPDATE user SET password = '{f.encrypt(new_password.encode()).decode()}' WHERE id = {user_id}")
                elif user_input == '3':
                    new_username = input("Enter your new user name: ")
                    new_password = input("Enter your new password: ")
                    cursor.execute(f"UPDATE user SET username = '{new_username}', password = '{f.encrypt(new_password.encode()).decode()}' WHERE id = {user_id}")
                print(Fore.GREEN + "Profile changes successfully" + Fore.RESET)
                conn.commit()
            elif user_input == '2':
                user_input = input("Are you sure you want delete your profile? (Y/N): ")
                if user_input.startswith('y'):
                    cursor.execute(f"DELETE FROM user WHERE id = {user_id}")
                    conn.commit()
                    print(Fore.RED + "Profile deleted successfully" + Fore.RESET)
        except TypeError:
            print(Fore.RED + "Username is wrong\nplese try again" + Fore.RESET)
            app()
        except:
            print(Fore.RED + "An unexpexted error happened\nPlease try again" + Fore.RESET)
            app()
    elif user_input == '2':
        register()
        app()
    elif user_input == '3':
        quit()

    elif user_input == '99':
        cursor.execute('Drop table password')
        cursor.execute('Drop table user')
        print(Fore.RED + "Tables deleted successfully" + Fore.RESET)
        conn.commit()

    else:
        print(Fore.RED + "Unvalid selection!" + Fore.RESET)
        app()

app()