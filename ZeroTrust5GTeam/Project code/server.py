#Umass 690C Final Project
#Author:Changhao Zhao, Hengyi Zhu, Junfei Zhang
#2024/5/16

import socket
import random
import threading

# Predefined GUTI pool
GUTI_POOL = ["12345", "12456", "12567", "12678", "12789"]

# Select a GUTI from the pool that is different from the current GUTI
def get_random_guti_excluding(current_guti):
    available_gutis = [guti for guti in GUTI_POOL if guti != current_guti]
    return random.choice(available_gutis)

def handle_client(client_socket):
    try:
        # Receive data packet and GUTI from the client
        request = client_socket.recv(1024).decode('utf-8')
        if request:
            data_packet, guti = request.split(',')
            transformed_guti = get_random_guti_excluding(guti)
            print("Zero Trust Mode Activated")
            print(f"User: {transformed_guti} requests to send message: {data_packet}")

            # Send back the transformed GUTI and data packet to the client
            response = f"{data_packet},{transformed_guti}"
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Close the connection
        client_socket.close()

def listen_for_shutdown(server):
    while True:
        command = input("Type 'shutdown' to close the server: ")
        if command.strip().lower() == "shutdown":
            print("Shutdown command received. Shutting down server...")
            server.close()
            break

def main():
    global server
    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to local address and port
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    # Create a thread to listen for shutdown commands
    shutdown_thread = threading.Thread(target=listen_for_shutdown, args=(server,))
    shutdown_thread.start()
    
    while True:
        try:
            # Accept client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            # Handle client request
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except OSError:
            break  # Exit the loop if the server is closed

if __name__ == "__main__":
    main()
