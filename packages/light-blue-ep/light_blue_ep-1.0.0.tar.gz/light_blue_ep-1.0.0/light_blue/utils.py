import time
import sys


def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def cyan(text):
    return f"\033[96m{text}\033[0m"


def loader():
    while True:
        for cursor in "|/-\\":
            yield cursor
