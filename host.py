import socket
import threading
import hashlib
import os
import time

clients = {}
lock = threading.Lock()
COLORS = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

os.system('clear')
print("█  █  █  █  █ █  █▀▀")
print("█▀▄█  █  █   ██  █▄▄")
print("█  █  █▄▄█  █ █  █▄▄")
print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
print("Termchat - HOST SEVER")
print("")
time.sleep(1.5)
os.system('clear')

def get_color(username):
    hash_num = int(hashlib.md5(username.encode()).hexdigest(), 16)
    return COLORS[hash_num % len(COLORS)]

def broadcast(message, sender_socket=None):
    with lock:
        for client_sock in clients.copy():  # Use copy to avoid runtime changes
            try:
                if client_sock != sender_socket:
                    client_sock.send(message.encode('utf-8'))
                    print(f"[DEBUG] Sent to {clients[client_sock][0]}: {message}")  # Debug
            except Exception as e:
                print(f"[ERROR] Broadcast failed: {e}")
                del clients[client_sock]

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        print(f"[CONNECTION] New user: {username}")  # Debug
        user_color = get_color(username)
        
        with lock:
            clients[client_socket] = (username, user_color)
        
        join_msg = f"{user_color}** {username} joined! **\033[0m"
        broadcast(join_msg, client_socket)
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"[DISCONNECT] {username} left silently")
                break
            print(f"[MESSAGE] {username}: {message}")  # Debug
            full_msg = f"{user_color}{username}:\033[0m {message}"
            broadcast(full_msg, client_socket)
            
    except Exception as e:
        print(f"[ERROR] Client handling failed: {e}")
    finally:
        with lock:
            if client_socket in clients:
                username, _ = clients[client_socket]
                leave_msg = f"{user_color}** {username} left **\033[0m"
                broadcast(leave_msg)
                del clients[client_socket]
        client_socket.close()

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "0.0.0.0"

def start_server():
    port = 12345
    host_ip = get_local_ip()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)
    
    print(f"Server running on {host_ip if host_ip != '0.0.0.0' else 'all interfaces'}:{port}")
    print("Waiting for connections...")
    
    try:
        while True:
            client_sock, addr = server.accept()
            print(f"New connection from {addr[0]}")
            threading.Thread(target=handle_client, args=(client_sock,)).start()
    finally:
        server.close()

if __name__ == "__main__":
    start_server()