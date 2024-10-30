import socket

HOST = "10.0.0.1"  # Server's IP address
PORT = 1200       # Port number for communication

# Open a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print('Server listening on {}:{}'.format(HOST, PORT))
    
    while True:
        # Receive data from the client
        data, addr = s.recvfrom(1024)
        if not data:
            break 
        # Convert the received data to all caps
        response = data.decode('utf-8').upper()
        byte_response = response.encode('utf-8')
        
        # Send the response back to the client
        s.sendto(byte_response, addr)  # sendto takes 2 arguments: the response and the client address
