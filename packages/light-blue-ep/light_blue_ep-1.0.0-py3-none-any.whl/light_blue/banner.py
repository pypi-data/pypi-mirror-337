#!/Users/sunny/Desktop/Terminal_game/myenv/bin/python

import shutil
import time
from pyfiglet import Figlet
from termcolor import colored
from utils import yellow

def print_menu():
        print(yellow("\n🧠 Light Blue — Hacker simulator"))
        print("1. 🔍 Run a password breach check")
        print("2. 🧪 Audit weak passwords")
        print("3. 🎣 Check the phishing link")
        print("4. ❌ Exit (Press ""Exit"" to quit\n")
        print("\nAdd -i to any option (e.g., 1-i) to learn more about that tool.\n")


        print ("\n----------------------------------------------------------------------------------------------------\n")
        print(yellow(""" 👋 Welcome to Light Blue — Hacker Simulator 🧠💻""") +"""
You're stepping into the role of a white-hat hacker whose mission is to help users stay secure online.
Use tools to check for password breaches, audit password strength, and identify phishing traps.
This is a fun and educational tool that simulates a few common security tools and techniques.
You can check if a password has been breached, audit a list of passwords, and spot phishing links.
The tool is for educational purposes only and does not perform any real hacking or security testing.

Created by -- Nithish Yenaganti
                        """)
        print ("\n----------------------------------------------------------------------------------------------------\n")

        
def type_out_centered_block(text_block, color="cyan", delay=0.002):
    columns = shutil.get_terminal_size().columns
    lines = text_block.strip().splitlines()

    for line in lines:
        centered = line.strip().center(columns)
        print(colored(centered, color))
        time.sleep(delay)

def banner():
  
    
    # Lock ASCII Art (compact)
    ascii_image = r"""
     .--------.
    / .------. \
   / /        \ \
   | |  LOCK  | |
  _| |________| |_
.' |_|        |_| '.
'._____ ____ _____.'
|     .'____'.     |
'.__.'.'    '.'.__.'
'.__  |      |  __.'
|   '.'.____.'.'   |
'.____'.____.'____.'
'.________________.'
""".strip()

    #  Banner Text
    full_text = "Light Blue"
    fig = Figlet(font='starwars')  # 'big', 'doh', '3-d' also work great
    ascii_banner = fig.renderText(full_text).strip()

    # Combine lock + banner
    full_display = ascii_image + "\n" + ascii_banner

    # Print from top, no spacing tricks
    type_out_centered_block(full_display, color="cyan", delay=0.005)
    print_menu()
    


