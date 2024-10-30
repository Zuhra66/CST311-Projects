# import necessary libraries
from socket import socket, AF_INET, SOCK_DGRAM
import random
import time

def main():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    serverName = 'localhost'  # Replace 'localhost' with server IP
    serverPort = 12000

    for seq in range(1, 11):
        # Sleep for 3 seconds between heartbeats
        time.sleep(3)
        # Decide whether to drop the message (simulate 30% packet loss)
        rand = random.randint(1, 10)
        if rand <= 3 and seq != 10:
            # Simulate packet loss: skip sending
            print("Heartbeat %d dropped." % seq)
            continue
        else:
            # Send the heartbeat message in the format expected by the server
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            message = "sequence %d, time %s" % (seq, timestamp)
            clientSocket.sendto(message.encode(), (serverName, serverPort))
            print("Heartbeat %d sent." % seq)

if __name__ == "__main__":
    main()