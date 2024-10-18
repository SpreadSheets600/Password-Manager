import random
import pyperclip

def generate_password(min_length=6):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%^&*()'

    password_length = random.randint(10, 12)

    password_list = [random.choice(letters) for _ in range(password_length - 4)]
    password_list += [random.choice(symbols) for _ in range(2)]
    password_list += [random.choice(numbers) for _ in range(2)]

    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    return password


def password_strength(password):
    if len(password) < 6:
        return "WEAK"
    up = any(char.isupper() for char in password)
    digit = any(char.isdigit() for char in password)

    if up and digit:
        return "STRONG"
    return "MEDIUM"

