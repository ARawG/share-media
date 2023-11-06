"""Importing libraries"""
import socket
import os
import time

ip = "localhost"
port = 8092
buffer_size = 8192 #Bytes => 8 KB


files_list = []
def receive_file():
    """This function receive data from the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, port))
        client.send("down".encode())
        # Receive files list and print
        server_files = client.recv(buffer_size).decode()
        print(server_files)
        print("please choose a file to download:")
        file_name = input()
        print("log")
        client.sendall(file_name.encode())
        file_size = int(client.recv(buffer_size).decode())
        requested_file = client.recv(buffer_size)
        
        
        if requested_file == b"File not found!":
            print(requested_file.decode()) 
        else:
            # File receiving cycle
            with open(f"./client-files/{file_name}", "wb") as file:
                download = 0
                
                while (download<file_size):
                    data = client.recv(buffer_size)
                    file.write(data)
                    download+=buffer_size
                    
                time.sleep(1)     
                client.send(b"File sent!")
                    
            print("file downloaded from server.")

def send_file(file_name):
    """This function send data to server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, port))
        print("connected to the server.")
        client.send("up".encode())
        time.sleep(1)
        # Error handling
        try:
            path = f"./client-files/{file_name}"
            file_size = os.stat(path).st_size

            client.send(str(file_size).encode())
            client.send(file_name.encode())

            # Sending process to sending file to the server
            with open(path, "rb") as file:
                steps = int(file_size/buffer_size + 1)
                
                download = 0
                    
                while(download<file_size):
                    data = file.read(buffer_size)
                    client.send(data)
                    download+=buffer_size
                time.sleep(1)    
                client.send(b"File sent!")
                print("\nFile sent!!!")
                
        except FileNotFoundError:
            print("File not found!")
    
def client_answer():
    global ans
    ans = (int(input("If you wanna download a file write 1 otherwise write 2. \n")))
    
def select_file_to_upload():
    global selected_file
    selected_file_test = input("Please choose a file to upload:")
    if(selected_file_test in os.listdir("./client-files")):
        selected_file = selected_file_test
    else:
        raise Exception("Please choose a valid")
        
def task_manager():
    """This function is handling client request."""
    client_answer()
    if ans == 1:
        receive_file()
        print("File downloaded")
    elif ans == 2:
        print("available files:")
        files = os.listdir("./client-files")
        for file in files:
            print(file)
        select_file_to_upload()
        path1 = selected_file
        print(path1.split("/")[-1])
        fileName = path1.split("/")[-1]
        send_file(fileName)
        print("File uploaded")
    else:
        print(ans, type(ans))
        raise Exception("Please choosse a valid number.")
    
if __name__ == "__main__":
    task_manager()
    