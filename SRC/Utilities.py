import random
import pyperclip

def generate_password(min_length=10):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%^&*()'

    # Set a password length (optional, can still be based on min_length)
    password_length = random.randint(10, 12)  # Adjust as desired

    # Create a list of random characters
    password_list = [random.choice(letters) for _ in range(password_length - 4)]
    password_list += [random.choice(symbols) for _ in range(2)]
    password_list += [random.choice(numbers) for _ in range(2)]

    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)
    return password

