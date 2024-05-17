#Umass 690C Final Project
#Author:Changhao Zhao, Hengyi Zhu, Junfei Zhang
#2024/5/16
import socket
import random

# Predefined GUTI pool
GUTI_POOL = ["12345", "12456", "12567", "12678", "12789"]

# Randomly select a GUTI from the pool
def get_random_guti():
    return random.choice(GUTI_POOL)

def main():
    # Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client.connect(("127.0.0.1", 9999))

    # Randomly select a GUTI from the pool
    guti = get_random_guti()
    
    print("Zero Trust Mode Activated")
    print(f"User GUTI: {guti} successfully hide in zero-trust mode")

    data_packet = input("Please enter the data you want to send (five digits): ")
    while not data_packet.isdigit() or len(data_packet) != 5:
        data_packet = input("Invalid input. Please enter exactly five digits: ")
    
    # Send data packet and GUTI to the server
    message = f"{data_packet},{guti}"
    client.send(message.encode('utf-8'))
    
    # Receive response from the server containing the transformed GUTI and data packet
    response = client.recv(1024).decode('utf-8')
    if response:
        data_packet, transformed_guti = response.split(',')
        print(f"User: {transformed_guti} successfully sent a message in zero-trust mode : {data_packet}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()
