import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening on", server_address)

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    connection, client_address = server_socket.accept()

    try:
        print("Connection from", client_address)

        # Receive the data from the client
        data = connection.recv(1024)
        print("Received:", data.decode())

        # Send a response back to the client
        connection.sendall(b"Message received. Thank you!")

    finally:
        # Clean up the connection
        connection.close()
