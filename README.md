# Inputs to Mail

This project captures inputs from the keyboard, mouse, screenshots, and microphone and sends them to your email. It is designed for testing the security of information systems.

## Installation

No installation is required—just run the script.

## Usage

1. **Create an account on [Mailtrap](https://mailtrap.io/) using a temporary email.**
2. **Set your SMTP username and password in `keylogger.py`.**
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the script:**
   ```bash
   python3 keylogger.py
   ```
5. **Receive data from the target computer every 10 seconds.**
6. **If the target discovers the code and opens it, the program automatically deletes itself to protect your credentials.**
