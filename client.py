import socket
import threading
import sys
import time
import os

COLORS = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

os.system('clear')
print("█  █  █  █  █ █  █▀▀")
print("█▀▄█  █  █   ██  █▄▄")
print("█  █  █▄▄█  █ █  █▄▄")
print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
print("Termchat - Terminal Chat")
print("")
time.sleep(1.5)
os.system('clear')

def receive_messages(sock, username):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                print("\n[ERROR] Connection closed by server")
                break
            sys.stdout.write('\r\033[K') 
            print(f"{message}")
            sys.stdout.write(f"{username}: ")
            sys.stdout.flush()
        except Exception as e:
            print(f"\n[ERROR] Receive failed: {e}")
            break

def start_client():
    try:
        host_ip = input(f"Enter host IP:\033[96m ")
        port = 12345
        username = input(f"\033[0mChoose a username:\033[1m ").strip()
        
        if not username:
            print("[ERROR] Username cannot be empty!")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host_ip, port))
        client.send(username.encode('utf-8'))
        
        print(f"\033[92mConnected!\033[0m Start chatting...")
        print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
        print("")
        
        receive_thread = threading.Thread(target=receive_messages, args=(client, username))
        receive_thread.daemon = True
        receive_thread.start()
        
        while True:
            try:
                message = input(f"\033[1m{username}\033[0m: ")
                if message.lower() == '/exit':
                    break
                client.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                print("\nExiting...")
                break
                
    finally:
        client.close()
        print("Disconnected from server")

if __name__ == "__main__":
    start_client()