import requests
from hashlib import sha1
from light_blue.utils import green, red, yellow


def check_pwned_password(password):
    hashed = sha1(password.encode()).hexdigest().upper()
    prefix, suffix = hashed[:5], hashed[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        lines = response.text.splitlines()
        found = next((line for line in lines if line.startswith(suffix)), None)

        if found:
            count = found.split(":")[1]
            print(red("\n⚠️  Warning: This password has been compromised in past data breaches."))
            print(yellow(f"It has appeared {int(count):,} times in leaked datasets across the internet."))
            print(red(
                    "Continuing to use this password puts your accounts at serious risk. "
                    "Attackers often exploit reused or breached passwords to gain unauthorized access. "
                    "We strongly recommend replacing it with a unique, strong password that hasn’t appeared in any breach. "
                    "Using a password manager can help you generate and store secure passwords for each of your accounts."
                    ))

        else:
            print(green("\n✅ Good news — this password has not been found in any known data breaches."))
            print(green(
                    "While this is a positive sign, it's still important to follow best security practices. "
                    "Use strong, unique passwords for each account and consider updating them regularly to stay ahead of emerging threats. "
                    "Regular password changes reduce the risk of exposure from future breaches or leaks."
                        ))

    except Exception as e:
        print(red(f"Error checking password: {e}"))
