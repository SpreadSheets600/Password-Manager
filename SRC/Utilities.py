import random
import pyperclip

def genpass():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%^&*()'
    
    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)
    return password

def pstrng(password):
    if len(password) < 6:
        return "WEAK"
    up = any(char.isupper() for char in password)
    digit = any(char.isdigit() for char in password)
    
    if up and digit:
        return "STRONG"
    return "MEDIUM"