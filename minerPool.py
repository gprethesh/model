import socket
import threading
import redis
import json

# Constants
IP = socket.gethostbyname(socket.gethostname())
PORT = 65432
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address):
    try:
        # Receive data from client
        data = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        data = json.loads(data)

        response_message = "Data processed successfully"
        client_socket.send(response_message.encode("utf-8"))
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send(f"Error: {str(e)}".encode("utf-8"))
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f"Server started on {IP}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_handler.start()


# Start the server
start_server()
