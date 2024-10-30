import random
from socket import socket, AF_INET, SOCK_DGRAM

# Constants
HOST = "10.0.0.1"  # Server's IP address
PORT = 1200        # Port number used by the server
PING_COUNT = 10    # Number of pings to send
PACKET_LOSS_RATE = 0.4  # 40% packet loss rate
LOSS_COUNT = int(PING_COUNT * PACKET_LOSS_RATE)

def main():
    s = socket(AF_INET, SOCK_DGRAM) # Create a UDP Socket
    s.bind((HOST, PORT)) #  Assign IP address and port number to socket
    print('Server listening on {}:{}'.format(HOST, PORT))

    ping_count = 0 # Initialize variable to count number of pings
    loss_quota = LOSS_COUNT # Initialize variable for loss quota for each group of pings

    while True:
      data, addr = s.recvfrom(1024)  # Receive message
    
      ping_count += 1 # Increment ping count
    
      # Simulate packet loss with token bucket algorithm
      if loss_quota > 0 and random.randint(1, 10) <= LOSS_COUNT:
          print("Ping {} from {}: Packet lost".format(ping_count, addr))
          loss_quota -= 1 # Decrement loss quota
          continue
       
      # Respond to client if packet is received
      print("Ping {} from {}: Responding".format(ping_count, addr))
      s.sendto(data, addr)
    

      # Reset the loss quota and ping count variables after each ping burst
      if ping_count == PING_COUNT:
         ping_count = 0 # Reset variable for ping count
         loss_quota = LOSS_COUNT # Reset variable for loss quota


if __name__ == "__main__":
  main()

# The server sits in an infinite loop listening for incoming UDP packets. 
# When a packet comes in, the server will decide to respond based on the implemented packet loss simulation condition.