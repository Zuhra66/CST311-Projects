#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "[team name here]"
__credits__ = [
  "Your",
  "Names",
  "Here"
]


import socket as s
import time

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

def connection_handler(connection_socket, address):
  # Read data from the new connectio socket
  #  Note: if no data has been sent this blocks until there is data
  query = connection_socket.recv(1024)
  
  # Decode data from UTF-8 bytestream
  query_decoded = query.decode()
  
  # Log query information
  log.info("Received query test \"" + str(query_decoded) + "\"")
  
  # Perform some server operations on data to generate response
  time.sleep(10)
  response = query_decoded.upper()
  
  # Sent response over the network, encoding to UTF-8
  connection_socket.send(response.encode())
  
  # Close client socket
  connection_socket.close()
  

def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(2)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))

  try:
        # Accept connection from Client X
        connection_socket_X, address_X = server_socket.accept()
        log.info("Connected to Client X at " + str(address_X))

        # Accept connection from Client Y
        connection_socket_Y, address_Y = server_socket.accept()
        log.info("Connected to Client Y at " + str(address_Y))

        while True:
            # Receive message from Client X
            message_X = connection_socket_X.recv(1024).decode()
            log.info(f"Received from Client X: {message_X}")

            # Check for exit condition
            if message_X.lower() == "bye":
                connection_socket_Y.send("Client X has left the chat.".encode())
                break
            else:
                # Forward message to Client Y
                connection_socket_Y.send(message_X.encode())

            # Receive message from Client Y
            message_Y = connection_socket_Y.recv(1024).decode()
            log.info(f"Received from Client Y: {message_Y}")

            # Check for exit condition
            if message_Y.lower() == "bye":
                connection_socket_X.send("Client Y has left the chat.".encode())
                break
            else:
                # Forward message to Client X
                connection_socket_X.send(message_Y.encode())

  except Exception as e:
      log.error(f"An error occurred: {e}")
  finally:
      # Close client sockets
      connection_socket_X.close()
      connection_socket_Y.close()
      # Close server socket
      server_socket.close()
  

  '''# Surround with a try-finally to ensure we clean up the socket after we're done
  try:  STARTER CODE
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()
      log.info("Connected to client at " + str(address))
      # Pass the new socket and address off to a connection handler function
      connection_handler(connection_socket, address)
  finally:
    server_socket.close()

if __name__ == "__main__":
  main()'''
