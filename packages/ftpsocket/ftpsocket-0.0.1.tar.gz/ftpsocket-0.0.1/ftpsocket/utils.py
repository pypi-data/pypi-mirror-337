#Not objectible
import socket
#defining: Creating Socket.
def create_socket(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))#Try to connect.
    return client_socket