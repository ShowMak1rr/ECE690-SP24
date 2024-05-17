#Umass 690C Final Project
#Author:Changhao Zhao, Hengyi Zhu, Junfei Zhang
#2024/5/16

import socket
import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Predefined GUTI pool
GUTI_POOL = ["12345", "12456", "12567", "12678", "12789", "12890", "12901", "13012", "13123", "13234",
             "13345", "13456", "13567", "13678", "13789", "13890", "13901", "14012", "14123", "14234"]

# Randomly select a GUTI from the pool
def get_random_guti():
    return random.choice(GUTI_POOL)

# Randomly select a GUTI from the pool excluding the current GUTI
def get_random_guti_excluding(current_guti):
    available_gutis = [guti for guti in GUTI_POOL if guti != current_guti]
    return random.choice(available_gutis)

# Function to send data and measure time
def send_data(enable_guti_transform, num_packets):
    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client.connect(("127.0.0.1", 9999))
    
    guti = get_random_guti() if enable_guti_transform else "54321"  # Select GUTI based on whether the transformation system is enabled

    # Generate multiple data packets
    data_packets = ";".join([f"12{str(i).zfill(3)}" for i in range(num_packets)])
    message = f"{data_packets},{guti}"
    
    start_time = time.time()
    client.send(message.encode('utf-8'))
    
    # Receive the response from the server containing the transformed GUTI and data packet
    response = client.recv(1024).decode('utf-8')
    end_time = time.time()
    
    # Close the connection
    client.close()
    
    return end_time - start_time

# Function to plot a bar chart comparing the average times with and without GUTI transformation
def plot_bar_chart(times_with_transform, times_without_transform):
    labels = ['With GUTI Transform', 'Without GUTI Transform']
    average_times = [np.mean(times_with_transform), np.mean(times_without_transform)]
    std_devs = [np.std(times_with_transform), np.std(times_without_transform)]

    fig, ax = plt.subplots()
    ax.bar(labels, average_times, yerr=std_devs, capsize=10, color=['blue', 'orange'], width=0.6)

    ax.set_xlabel('System Mode')
    ax.set_ylabel('Average Time (seconds)')
    ax.set_title('Performance Comparison: With and Without GUTI Transform')
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    plt.show()

# Function to plot a scatter chart showing communication speed over time
def plot_scatter_chart(times_with_transform, times_without_transform):
    x = np.arange(1, len(times_with_transform) + 1)

    plt.scatter(x, times_with_transform, label='With GUTI Transform', color='blue')
    plt.scatter(x, times_without_transform, label='Without GUTI Transform', color='orange')

    z_with = np.polyfit(x, times_with_transform, 1)
    p_with = np.poly1d(z_with)
    plt.plot(x, p_with(x), "--", color='blue')

    z_without = np.polyfit(x, times_without_transform, 1)
    p_without = np.poly1d(z_without)
    plt.plot(x, p_without(x), "--", color='orange')

    plt.xlabel('Communication Attempt')
    plt.ylabel('Time (seconds)')
    plt.title('Communication Speed Over Time')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    plt.show()

# Function to plot a line chart showing performance over increasing data packets
def plot_line_chart(times_with_transform, times_without_transform, num_packets_list):
    plt.plot(num_packets_list, times_with_transform, label='With GUTI Transform', marker='o', color='blue')
    plt.plot(num_packets_list, times_without_transform, label='Without GUTI Transform', marker='o', color='orange')

    plt.xlabel('Number of Data Packets')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Over Increasing Data Packets')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    plt.show()

def main():
    num_tests = 50
    num_packets_list = range(1, 11)  # From 1 data packet to 10 data packets

    times_with_transform_single = []
    times_without_transform_single = []

    for _ in range(num_tests):
        times_with_transform_single.append(send_data(enable_guti_transform=True, num_packets=1))
        times_without_transform_single.append(send_data(enable_guti_transform=False, num_packets=1))
    
    avg_time_with_transform = np.mean(times_with_transform_single)
    avg_time_without_transform = np.mean(times_without_transform_single)
    
    std_with_transform = np.std(times_with_transform_single)
    std_without_transform = np.std(times_without_transform_single)
    
    print(f"Average time with GUTI transform: {avg_time_with_transform:.5f} seconds")
    print(f"Average time without GUTI transform: {avg_time_without_transform:.5f} seconds")
    print(f"Standard deviation with GUTI transform: {std_with_transform:.5f} seconds")
    print(f"Standard deviation without GUTI transform: {std_without_transform:.5f} seconds")
    
    plot_bar_chart(times_with_transform_single, times_without_transform_single)
    plot_scatter_chart(times_with_transform_single, times_without_transform_single)

    times_with_transform_multiple = []
    times_without_transform_multiple = []

    for num_packets in num_packets_list:
        times_with_transform_for_packets = []
        times_without_transform_for_packets = []

        for _ in range(5):  # Test each data packet number 5 times
            times_with_transform_for_packets.append(send_data(enable_guti_transform=True, num_packets=num_packets))
            times_without_transform_for_packets.append(send_data(enable_guti_transform=False, num_packets=num_packets))

        avg_time_with_transform = np.mean(times_with_transform_for_packets)
        avg_time_without_transform = np.mean(times_without_transform_for_packets)

        times_with_transform_multiple.append(avg_time_with_transform)
        times_without_transform_multiple.append(avg_time_without_transform)

        print(f"With GUTI Transform - {num_packets} packets: {avg_time_with_transform:.5f} seconds")
        print(f"Without GUTI Transform - {num_packets} packets: {avg_time_without_transform:.5f} seconds")
    
    avg_time_with_transform_multiple = np.mean(times_with_transform_multiple)
    avg_time_without_transform_multiple = np.mean(times_without_transform_multiple)

    print(f"Average time with GUTI transform (multiple packets): {avg_time_with_transform_multiple:.5f} seconds")
    print(f"Average time without GUTI transform (multiple packets): {avg_time_without_transform_multiple:.5f} seconds")
    
    plot_line_chart(times_with_transform_multiple, times_without_transform_multiple, num_packets_list)

if __name__ == "__main__":
    main()



