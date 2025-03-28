# 🧠 Light Blue — Hacker Simulator (Terminal Game)

**Light Blue** is a fun, educational, and interactive terminal-based cybersecurity simulation tool built in Python.  
It helps users **learn and explore basic security concepts** like password safety, entropy, and phishing detection — all from the comfort of your terminal.

🔐 Perfect for students, ethical hackers, and anyone curious about cybersecurity!

> ⚠️ For educational use only. This tool simulates real-world scenarios but does **not perform any real hacking**.

---

## 🎮 Features

### 🔍 Password Breach Checker
Check if a password has been exposed in known data breaches using the [Have I Been Pwned](https://haveibeenpwned.com/) API (via k-anonymity for safety).

### 🧪 Password Auditor
Evaluate a password’s strength based on:
- Entropy (randomness)
- Common weak patterns
- Length & character variety  
Includes suggestions for improving weak passwords.

### 🎣 Phishing Link Scanner
Scan suspicious URLs using the [VirusTotal](https://virustotal.com) API and detect if they’re malicious or flagged by security engines.

---

## 🚀 How to Install


```bash
pip install light-blue
pip install -r requirements.txt
