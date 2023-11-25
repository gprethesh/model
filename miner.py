import socket
import json
import config


def send_data_to_miner_pool(job_id, miner_wallet_address):
    # Data to be sent
    data = {
        "job_id": job_id,
        "miner_wallet_address": miner_wallet_address,
    }
    serialized_data = json.dumps(data)

    # Constants for server connection
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 65432
    BUFFER_SIZE = 1024

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client.connect((SERVER_IP, SERVER_PORT))

    # Send the serialized data
    client.send(serialized_data.encode("utf-8"))

    # Wait for the server's response
    response = client.recv(BUFFER_SIZE).decode("utf-8")

    # Close the connection
    client.close()

    return response


job_id = "12345"
miner_wallet_address = config.WALLET_ADDRESS

response = send_data_to_miner_pool(job_id, miner_wallet_address)

print("Response from inode:", response)
