from cryptography.fernet import Fernet

class Passwordmanager:

    def __init__(self):
        self.key = None
        self.Password_file = None
        self.password_dict = {}

    def create_key(self, path):
        # FIXED: Corrected spelling to generate_key()
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()        

    def create_password_file(self, path, initial_values=None):
        self.Password_file = path
        
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):  
        self.Password_file = path

        with open(path, 'r') as f:
            for line in f:
                # FIXED: Added .strip() to clean up trailing newlines
                line = line.strip()
                if not line or ':' not in line:
                    continue  # Skips empty lines or malformed data
                
                site, encrypted = line.split(':', 1)
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password  

        if self.Password_file is not None:
            # FIXED: Changed mode to 'a' to reliably append lines
            with open(self.Password_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ':' + encrypted.decode() + '\n')

    def get_password(self, site):
        return self.password_dict[site]


def main():
    # This dictionary acts as initial mockup data
    initial_passwords = {
        "email": "1234567",
        "facebook": "helloworld123",
        "something": "myfavoritepassword_123"
    }

    pm = Passwordmanager()

    print("""\nWhat do you want to do?
    1. Create a new key
    2. Load an existing key
    3. Create a new password file
    4. Load an existing password file
    5. Add a new password
    6. Get a password
    7. Exit
    """)

    done = False

    while not done:
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            path = input("Enter the path to save the key (e.g., secret.key): ")
            pm.create_key(path)
            print("Key created and saved.")

        elif choice == "2":
            path = input("Enter the path to load the key: ")
            try:
                pm.load_key(path)
                print("Key loaded.")    
            except FileNotFoundError:
                print("Key file not found!")

        elif choice == "3": 
            if pm.key is None:
                print("Please load or create a key first!")
                continue
            path = input("Enter the path to save the password file (e.g., passwords.txt): ")
            pm.create_password_file(path, initial_passwords)
            print("Password file created and saved.")

        elif choice == "4": 
            if pm.key is None:
                print("Please load or create a key first!")
                continue
            path = input("Enter the path to load the password file: ")
            try:
                pm.load_password_file(path)
                print("Password file loaded.")
            except FileNotFoundError:
                print("Password file not found!")

        elif choice == "5": 
            if pm.key is None:
                print("Please load or create a key first!")
                continue
            site = input("Enter the site name: ")
            # FIXED: Changed variable name to 'pwd' to prevent overwriting the dict template
            pwd = input("Enter the password: ")
            pm.add_password(site, pwd)
            print(f"Password for {site} added.")

        elif choice == "6":
            site = input("Enter the site name: ")
            try:
                password = pm.get_password(site)
                print(f"Password for {site}: {password}")
            except KeyError:
                print(f"No password found for {site}.")
        
        elif choice == "7":
            done = True
            print("Exiting.")

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

