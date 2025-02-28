#!/usr/bin/env python3

import socket
import threading
import time

SEND_PORT = 3001
RECEIVE_PORT = 3000

def receive_messages():
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_socket.bind(('', RECEIVE_PORT))
    recv_socket.listen()

    client, addr = recv_socket.accept()
    print(f"Connected with {addr}")

    while True:
        msg = client.recv(1024).decode()
        if not msg or msg.lower() == "exit":
            break
        print(f"\nFriend: {msg}")

    client.close()
    recv_socket.close()

def send_messages():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while send_socket.connect_ex(("localhost", SEND_PORT)): 
        print("Waiting for connection...")
        time.sleep(2)

    while True:
        msg = input("You: ")
        send_socket.send(msg.encode())
        if msg.lower() == "exit":
            break

    send_socket.close()

threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
