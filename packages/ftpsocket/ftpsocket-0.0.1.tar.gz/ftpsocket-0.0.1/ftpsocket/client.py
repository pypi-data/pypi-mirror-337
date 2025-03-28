# client.py

import socket
import os

class FTPClient:
    def __init__(self, host='localhost', port=21):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def login(self):
        response = self.client_socket.recv(1024).decode('utf-8')
        print(response)

    def send_file(self, filename):
        if not os.path.exists(filename):
            print(f"File {filename} does not exist yet!")
            return
        self.client_socket.send(f"STOR {filename}".encode('utf-8'))
        with open(filename, 'rb') as file:
            data = file.read(1024)
            while data:
                self.client_socket.send(data)
                data = file.read(1024)
        response = self.client_socket.recv(1024).decode('utf-8')
        print(response)

    def retrieve_file(self, filename):
        self.client_socket.send(f"RETR {filename}".encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        if "150" in response:  # 150 is FTP code for file opening if its inted.
            with open(filename, 'wb') as file:
                data = self.client_socket.recv(1024)
                while data:
                    file.write(data)
                    data = self.client_socket.recv(1024)
            print(f"File {filename} received successfully.")
        else:
            print(f"Error: {response}")

    def list_files(self):
        self.client_socket.send(b"LIST")
        response = self.client_socket.recv(1024).decode('utf-8')
        print("Files on server:")
        print(response)

    def quit(self):
        self.client_socket.send(b"QUIT")
        self.client_socket.close()
        print("Connection closed.")#Quiting the socket
        

if __name__ == "__main__":
    client = FTPClient()
    client.login()
    
    #Listing the available options.
    print("\nSelect operation:")
    print("1. Show the files list.")
    print("2. Upload file (STOR)")
    print("3. Download file (RETR)")
    print("4. Quit")
    
    while True:
        operation = input("\nEnter operation number: ")
        
        if operation == "1":
            client.list_files()
        elif operation == "2":
            filename = input("Enter filename to upload: ")
            client.send_file(filename)
        elif operation == "3":
            filename = input("Enter filename to download: ")
            client.retrieve_file(filename)
        elif operation == "4":
            client.quit()
            break
        else:
            print("Invalid operation. Please try again.")