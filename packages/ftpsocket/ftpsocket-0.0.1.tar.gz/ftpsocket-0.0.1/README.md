#ftpsocket: FTP using socket.
<img src="https://static.pepy.tech/badge/ftpsocket" height="30" /> <img src="https://static.pepy.tech/badge/ftpsocket/month" height="30" />

#ftpsocket: SOCKET-FTP

#ftpsocket:
__is a Python library designed to implement FTP server and client functionality using sockets for transferring files over the network. It allows you to send and receive files securely between devices connected to the same network.__
--- 
##Installation:
To install the ftpsocket library:
```bash
pip install ftpsocket
```
---

Usage Examples

#1. Starting the FTP Server:

In this example, we'll create and run an FTP server.

from ftpsocket.server import FTPServer

# Create and start the FTP server on the desired address and port
```python
ftp_server = FTPServer(host='0.0.0.0', port=21)
ftp_server.start()
```
#2. FTP Client Example:

The client connects to the server and sends a file.
```python
from ftpsocket.client import FTPClient
```
# Connect to an FTP server on a specific address and port
```python
ftp_client = FTPClient(host='127.0.0.1', port=21)# the local hosted.
ftp_client.connect()
```
# Send a file to the server
```python
ftp_client.send_file('example.txt')
```
# Close the connection after the file is sent
```python
ftp_client.close()
```

---

##Explanation:

FTPServer: This class allows you to start an FTP server that listens for incoming client connections, handling file uploads and downloads, at the local network.
FTPClient: The client connects to the server, sends files, and manages the connection.


##Features:

**FTP-like server-client file transfer over the network.**
##Note:**To secure connection using Python sockets, use ftpsocket.**
