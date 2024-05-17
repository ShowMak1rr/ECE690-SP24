Project: Zero Trust Architecture Simulation with GUTI-Based Pseudonym System
This project simulates a Zero Trust architecture using a GUTI-based pseudonym system to enhance privacy in 5G networks.
The simulation consists of a server and a client, implemented using Python and TCP sockets.


Files
server.py: 
The server code that listens for client connections and handles data packets with GUTI transformation.

client.py: 
The client code that connects to the server, sends data packets, and handles the server's response.

test_performance.py: 
A script to test and evaluate the performance of the system with and without GUTI transformation.

Prerequisites
Python 3.12 or higher
matplotlib library for plotting (can be installed via pip)


Usage
A.Running the Server
1.Open a terminal or command prompt.
2.Run the server script

The server will start listening on port 9999 for client connections. It also starts a thread to listen for a shutdown command. 
To shut down the server, type shutdown in the terminal and press Enter.

B.Running the Client
1.Open another terminal or command prompt.
2.Run the client script:

When prompted, enter a five-digit data packet to send to the server. 
The client will randomly select a GUTI from the predefined pool, send the data packet along with the GUTI to the server, and print the server's response.

C.Performance Testing
The test_performance.py script evaluates the performance of the system with and without GUTI transformation.
It needs to be started after server.py runs.