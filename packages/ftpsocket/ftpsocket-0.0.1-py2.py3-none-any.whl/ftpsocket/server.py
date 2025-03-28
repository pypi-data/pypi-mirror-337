import socket
import os
''' Internal FTP-OTS, 
Notice: the used socket are default host, dont change anything.'''
class FTPServer:
    def __init__(self, host='0.0.0.0', port=21):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"FTP Server listening on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            client_socket.send(b"220 Welcome to ftpsocket FTP server\n")
            self.handle_client(client_socket)
            
    def handle_client(self, client_socket):
        while True:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if command.startswith("STOR"):
                self.store_file(client_socket, command)
            elif command.startswith("RETR"):
                self.retrieve_file(client_socket, command)
            elif command.startswith("LIST"):
                self.list_files(client_socket)
            elif command.startswith("QUIT"):
                client_socket.send(b"221 Goodbye\n")
                client_socket.close()
                break
#File Storages - or TFS.
    def store_file(self, client_socket, command):
        filename = command.split(" ")[1]
        with open(filename, 'wb') as file:
            client_socket.send(b"150 Ok to send data\n")
            data = client_socket.recv(1024)
            while data:
                file.write(data)
                data = client_socket.recv(1024)
            client_socket.send(b"226 Transfer complete\n")

    def retrieve_file(self, client_socket, command):
        filename = command.split(" ")[1]
        if os.path.exists(filename):
            client_socket.send(b"150 Opening data connection\n")
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
            client_socket.send(b"226 Transfer complete\n")
        else:
            client_socket.send(b"550 File not found\n")

    def list_files(self, client_socket):
        files = os.listdir('.')
        client_socket.send(b"150 Here is the file list\n")
        for file in files:
            client_socket.send(f"{file}\n".encode('utf-8'))
        client_socket.send(b"226 Transfer complete\n")

if __name__ == "__main__":
    server = FTPServer()
    server.start()