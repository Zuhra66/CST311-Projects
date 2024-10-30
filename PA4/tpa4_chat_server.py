import ssl
import socket as s
import logging
import threading
import argparse
import sys

# Configure logging
logging.basicConfig()
log = logging.getLogger(f"SERVER:{__name__}")
log.setLevel(logging.DEBUG)

# Dictionary to keep track of connected clients
clients = {}

def broadcast_message(message, sender_socket):
    """Send message to all clients except the sender."""
    for client_socket in clients.values():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                log.error(f"Error sending message to client: {e}")
                client_socket.close()

def chat(connection_socket, username):
    """Handle communication for each client."""
    try:
        while True:
            message = connection_socket.recv(1024).decode()
            if not message:
                break
            log.info(f"{username}: {message}")
            broadcast_message(f"{username}: {message}", connection_socket)
    except Exception as e:
        log.error(f"Error handling {username}: {e}")
    finally:
        log.info(f"{username} has left the chat.")
        clients.pop(username, None)
        connection_socket.close()

def handle_client(connection_socket):
    """Handle new client connections."""
    try:
        username = connection_socket.recv(1024).decode()
        if username:
            log.info(f"{username} has connected.")
            clients[username] = connection_socket
            chat(connection_socket, username)
    except Exception as e:
        log.error(f"Error in client handling: {e}")
    finally:
        connection_socket.close()

def run_chat_server(server_host="0.0.0.0", server_port=12000, certfile=None, keyfile=None):
    """Run the chat server with TLS."""
    if not certfile or not keyfile:
        log.error("Both certfile and keyfile are required to start the server.")
        sys.exit(1)

    # Create a standard TCP socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Set up SSL/TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    # Bind and listen
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)

    log.info(f"The TLS-enabled chat server is ready on {server_host}:{server_port}")

    try:
        while True:
            # Accept a new connection
            connection_socket, addr = server_socket.accept()
            # Wrap the connection with SSL/TLS
            tls_conn = context.wrap_socket(connection_socket, server_side=True)
            # Start a new thread to handle the client
            threading.Thread(target=handle_client, args=(tls_conn,)).start()
    except KeyboardInterrupt:
        log.info("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Argument parser to allow the user to specify command line arguments
    parser = argparse.ArgumentParser(description="Start a TLS-enabled chat server.")
    parser.add_argument("--host", default="0.0.0.0", type=str, help="Server's hostname or IP address, default 0.0.0.0")
    parser.add_argument("--port", default=12000, type=int, help="Port number used by chat server, default 12000")
    parser.add_argument("--certfile", required=True, type=str, help="Path to the certificate file")
    parser.add_argument("--keyfile", required=True, type=str, help="Path to the private key file")

    # Parse the arguments
    args = parser.parse_args()

    # Run the chat server with the provided arguments
    run_chat_server(server_host=args.host, server_port=args.port, certfile=args.certfile, keyfile=args.keyfile)
