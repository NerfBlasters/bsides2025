#!/usr/bin/env python3
import socket
import time
import sys

def receive_until(sock, timeout=0.5):
    """Receive data until timeout"""
    sock.settimeout(timeout)
    data = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data.decode('utf-8', errors='ignore')

def send_line(sock, line):
    """Send a line to the socket"""
    sock.send((line + "\n").encode())
    time.sleep(0.1)

# Connect to the server
host = "0.cloud.chals.io"
port = 21696

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

print("Connected!")

# Receive initial prompt
data = receive_until(sock)
print(data)

# Send the first password
send_line(sock, "FIREBALL_RULES")
data = receive_until(sock)
print(data)

# Read answers from wordlist file or command line arguments
if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
    # Read from wordlist file
    print(f"\nReading wordlist from: {sys.argv[1]}")
    with open(sys.argv[1], 'r') as f:
        answers = [line.strip().lower() for line in f if line.strip()]
else:
    # Take answers from command line arguments
    answers = sys.argv[1:] if len(sys.argv) > 1 else []

for i, answer in enumerate(answers):
    print(f"\n[{i+1}/{len(answers)}] Trying: {answer}")
    send_line(sock, answer)
    data = receive_until(sock)

    if "Wrong" in data or "scorched" in data:
        print(f"❌ {data.strip()}")
    else:
        print(f"✓ SUCCESS! Answer: {answer}")
        print(data)
        # Continue to see more riddles or flag
        while True:
            more_data = receive_until(sock)
            if more_data:
                print(more_data)
            else:
                break
        break

sock.close()
