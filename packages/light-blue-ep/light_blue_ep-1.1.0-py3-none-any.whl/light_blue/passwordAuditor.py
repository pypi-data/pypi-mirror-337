from light_blue.utils import green, red, yellow
import math

def calculate_entropy(password):
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    pool = 0
    if has_lower: pool += 26
    if has_upper: pool += 26
    if has_digit: pool += 10
    if has_symbol: pool += 33

    if pool == 0:
        return 0

    return round(len(password) * math.log2(pool), 2)

def is_common_word(password):
    common_words = [
        'password', 'admin', 'welcome', 'qwerty', 'letmein',
        '123456', 'monkey', 'football', 'baseball', 'dragon'
    ]
    pw_lower = password.lower()
    return any(word in pw_lower for word in common_words)

def score_password(password):
    score = 0
    if len(password) >= 12: score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c in "!@#$%^&*()" for c in password): score += 1
    return score

def audit_passwords():
    print("\nEnter passwords separated by commas:")
    passwords = input(">> ").split(',')

    for pwd in passwords:
        pwd = pwd.strip()
        entropy = calculate_entropy(pwd)
        common = is_common_word(pwd)
        score = score_password(pwd)

        print(f"\n🔐 {pwd}")
        print(yellow(f"Entropy: {entropy} bits"))

        if common:
            print(red("⚠️ Contains a common dictionary word."))

        if score == 4:
            print(green("Strength: Strong ✅"))
        elif score >= 2:
            print(yellow("Strength: Moderate ⚠️"))
        else:
            print(red("Strength: Weak ❌"))
