import socket

HOST = "10.0.0.1"  # Server's IP address
PORT = 1200        # Port number used by the server

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST,PORT)) 
    while True:
        # Request user input
        message = input("Enter a message to send to the server (type 'done' to quit): ")
        
        if message.lower() == 'done':
            break
        
        byte_msg = message.encode('utf-8')
   

        s.sendall(byte_msg) 
        
        # Receive response from server
      
        data = s.recv(1024)
        print("Received: {}".format(data.decode('utf-8')))
