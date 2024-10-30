import threading
import socket as s
import ssl
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(f"CLIENT:{__name__}")
log.setLevel(logging.DEBUG)

chatting = True

def send_message(client_socket):
    """Send messages to the server."""
    global chatting
    try:
        while chatting:
            user_input = input("")
            if user_input.lower() == "bye":
                chatting = False
                break
            # Check if socket is open before sending
            if client_socket:
                client_socket.send(user_input.encode())
                log.debug(f"Message sent: {user_input}")
            else:
                log.error("Socket is closed. Cannot send message.")
                break
    except OSError as e:
        log.error(f"Error while sending message: {e}")
        chatting = False

def receive_message(client_socket):
    """Receive messages from the server."""
    global chatting
    try:
        while chatting:
            server_response = client_socket.recv(1024).decode()
            if server_response:
                print(f"{server_response}")
            else:
                break
    except OSError as e:
        log.error(f"Error receiving message: {e}")
    finally:
        chatting = False
        log.info("Disconnected from the server.")

def start_chat_client(server_host="10.0.0.1", server_port=12000, cafile="cacert.pem"):
    """Connect to the chat server using TLS encryption."""
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    
    tls_client_socket = context.wrap_socket(client_socket, server_hostname=server_host)
    
    try:
        log.info(f"Attempting to connect to {server_host}:{server_port} with TLS...")
        tls_client_socket.connect((server_host, server_port))
        log.info(f"Successfully connected to {server_host}:{server_port} with TLS")

        username = input("Enter your username: ")
        tls_client_socket.send(username.encode())
        log.info(f"Username {username} sent to server")

        # Start threads for sending and receiving messages
        threading.Thread(target=receive_message, args=(tls_client_socket,), daemon=True).start()
        threading.Thread(target=send_message, args=(tls_client_socket,)).start()

        # Keep the main thread alive while chatting
        while chatting:
            pass

    except ssl.SSLError as ssl_error:
        log.error(f"SSL error: {ssl_error}")
    except Exception as e:
        log.error(f"Connection failed: {e}")
    finally:
        try:
            tls_client_socket.close()
            log.info("Connection closed")
        except Exception as e:
            log.error(f"Error closing socket: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default='10.0.0.1', type=str, help="Chat server's hostname or IP address, default '10.0.0.1'")
    parser.add_argument("--port", default=12000, type=int, help="Port number used by the chat server, default 12000")
    parser.add_argument("--cafile", default="cacert.pem", type=str, help="CA certificate file")

    args = parser.parse_args()
    start_chat_client(server_host=args.server, server_port=args.port, cafile=args.cafile)
