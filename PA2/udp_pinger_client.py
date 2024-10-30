import socket
import time

# Constants
HOST = "10.0.0.1"  # Server's IP address
PORT = 1200        # Port number used by the server
PING_COUNT = 10    # Number of pings to send
TIMEOUT = 1        # 1 second timeout for each ping

# Initialize statistics
min_rtt = float('inf')
max_rtt = float('-inf')
total_rtt = 0
packets_lost = 0

# Create a UDP socket and set the timeout
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(TIMEOUT)  # Set timeout for receiving packets
    
    for i in range(1, PING_COUNT + 1):
        message = "Ping" + str(i)
        byte_msg = message.encode('utf-8')
        start_time = time.time()  # Record the time when the message is sent
        
        try:
            # Send the message to the server
            s.sendto(byte_msg, (HOST, PORT))
            
            # Receive response from the server
            data, addr = s.recvfrom(1024)
            end_time = time.time()  # Record the time when the response is received
            
            # Calculate the round-trip time (RTT)
            rtt = (end_time - start_time) * 1000  # Convert to milliseconds
            total_rtt += rtt
            
            # Update min and max RTT
            if rtt < min_rtt:
                min_rtt = rtt
            if rtt > max_rtt:
                max_rtt = rtt
            
            # Print the response and RTT
            print("Ping {}: rtt = {:.3f} ms".format(i, rtt))
        
        except socket.timeout:
            # If no response is received within the timeout
            print("Ping {}: Request timed out".format(i))
            packets_lost += 1

# Calculate average RTT
if PING_COUNT - packets_lost > 0:
    avg_rtt = total_rtt / (PING_COUNT - packets_lost)
else:
    avg_rtt = 0

# Calculate packet loss rate
packet_loss_rate = (packets_lost / PING_COUNT) * 100

# Print summary statistics
print("\nSummary values")
print("min_rtt = {:.3f} ms".format(min_rtt))
print("max_rtt = {:.3f} ms".format(max_rtt))
print("avg_rtt = {:.3f} ms".format(avg_rtt))
