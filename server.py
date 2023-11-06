"""Importing library"""
import socket
import os
import threading

"""Initial data"""
ip = "127.0.0.1"
port = 8092
buffer_size = 8192 

def send_file(client):
    """This function sends data to clients."""
    files = os.listdir("./server-files")
    files_path = "\n".join(files)
    client.send(files_path.encode())
    requested_file = client.recv(buffer_size).decode()
    
    # Error handling
    try:
        file_path = f"./server-files/{requested_file}"
        file_size = os.stat(file_path).st_size
        client.send(str(file_size).encode())
        with open(file_path, "rb") as file:
            steps = int(file_size/buffer_size + 1)
            for step in range(steps):
                data = file.read(buffer_size)
                client.send(data)
            client.send(b"File sent!")
            print("File sent!!!")
            
    except FileNotFoundError:
        client.send(b"File not found!")


def receive_file(client):
    """This function receives data from clients."""
    file_size = int(client.recv(buffer_size).decode())
    print("file_size:", file_size)
    file_name = client.recv(buffer_size).decode()
    with open(f"./server-files/{file_name}", "wb") as file:
        while True:
            data = client.recv(buffer_size)
            if data == b"file sent!":
                break
            file.write(data)
    print("File downloaded from server.") 

"""Server main loop for listening."""
def task_manager():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((ip, port))
            server.listen(5)
            print(f"Server is listening on address:{ip,port}...")
            client, address = server.accept() 
            print(f"Client with address: {address} connected")
            
            # Threading system
            answer = client.recv(buffer_size).decode()
            if answer == "up":
                client_thread = threading.Thread(target=receive_file, args=(client,))
                client_thread.start()
            if answer == "down":
                client_thread = threading.Thread(target=send_file, args=(client,))
                client_thread.start()
            
task_manager()
