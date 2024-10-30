"""Chat client for CST311 Programming Assignment 3"""
__author__ = "[team3]"
__credits__ = [
  "Your",
  "Names",
  "Here"
]

# Import statements
import socket as s

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = 'localhost'
server_port = 12000

def main():
  # Create socket
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  
  try:
    # Establish TCP connection
    client_socket.connect((server_name, server_port))
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)
    
  try:
    while True:
      # Get input from user
      user_input = input('You: ')
      
      # Send message to server
      client_socket.send(user_input.encode())
      
      # Exit if the user types 'bye'
      if user_input.lower() == 'bye':
        print('You left the chat.')
        break
      
      # Receive response from server
      server_response = client_socket.recv(1024)
      server_response_decoded = server_response.decode()
      
      # Print response from the other client via the server
      print('Friend: ' + server_response_decoded)
      
      # If the other client sends 'bye', close the connection
      if server_response_decoded.lower() == 'bye':
        print('Your friend left the chat.')
        break
      
  finally:
    # Close socket after exiting the chat
    client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()
