#!/Users/sunny/Desktop/Terminal_game/myenv/bin/python

from banner import banner
from passwordChecker import check_pwned_password
from passwordAuditor import audit_passwords as auditor
from phishing_detector import detect_phishing
from utils import yellow, red

def show_tool_info(choice):
    if choice == "1-i":
        print(yellow("\n🔍 Password Breach Check"))
        print("This tool checks if your password has been exposed in any known data breaches.")
        print("It uses the HaveIBeenPwned API and keeps your password safe using k-anonymity.\n")

    elif choice == "2-i":
        print(yellow("\n🧪 Audit Weak Passwords"))
        print("This module checks the strength of your password using entropy calculation, common patterns, and length.")
        print("It flags weak passwords and gives you improvement suggestions.\n")

    elif choice == "3-i":
        print(yellow("\n🎣 Phishing Link Scanner"))
        print("This tool scans a given URL using the VirusTotal API and reports if it has been flagged as malicious or suspicious.")
        print("Useful for identifying fake login pages or phishing attempts.\n")

def main_menu():
    banner()

    while True:
        

        choice = input("Select an operation (1-4 or 1-i, 2-i...): ").strip().lower()

        if choice == "1":
            password = input("\nEnter a password to check: ")
            check_pwned_password(password)
        elif choice == "2":
            auditor()
        elif choice == "3":
            detect_phishing()
        elif choice == "4" or choice == "exit":
            print("\n👋 Exiting.......Stay safe and secure.")
            break
        elif choice in ["1-i", "2-i", "3-i"]:
            show_tool_info(choice)
        else:
            print("\n❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
