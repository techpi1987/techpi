# Ask the owner to set the correct credentials (for demo only)
user_id_correct = input("Set the correct user id: ").strip()
password_correct = input("Set the correct password: ").strip()


attempts = 0
MAX_ATTEMPTS = 5

while attempts < MAX_ATTEMPTS:
    user_id = input("Enter your user id: ").strip()
    password = input("Enter your password: ").strip()

    if password == password_correct and user_id == user_id_correct:
        print("Access granted")
        break
    else:
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts
        if remaining > 0:
            print(f"Access denied . Attempts left: {remaining}")
        else:
            print("Account locked . Too many failed attempts.")