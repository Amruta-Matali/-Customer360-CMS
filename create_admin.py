
from modules.user_operations import create_user

username = input("Enter username: ")
email = input("Enter email: ")
password = input("Enter password: ")

result = create_user(username, email, password)

if result:
    print("Initial login account created successfully!")
else:
    print("Account creation failed.")
