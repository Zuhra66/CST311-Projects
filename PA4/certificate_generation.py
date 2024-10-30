#!/usr/bin/env python3

import subprocess
from python_hosts import Hosts, HostsEntry
import os


def prompt_for_common_name():
    # Prompt for the common name of the chat server
    return input("Enter common name for your chat server:")


def prompt_for_passphrase():
    # Prompt for a passphrase for the server private key
    return input("Enter a challenge password for the server private key:")


def write_common_name(common_name):
    with open('server_common.txt', 'w') as f:
        print(common_name, file=f)


def update_host_file(common_name):
    hosts = Hosts(path='/etc/hosts')
    hosts.remove_all_matching(address='10.0.0.4')
    new_entry = HostsEntry(entry_type='ipv4', address='10.0.0.4', names=[common_name])
    hosts.add([new_entry])
    hosts.write()


def generate_private_key(passphrase):
    # Generate the private key with a passphrase
    cmd = f"openssl genrsa -aes256 -passout pass:{passphrase} -out chatserver-key.pem 2048"
    result = subprocess.run(cmd.split(" "), capture_output=True)
    if result.returncode != 0:
        print(f"Error generating private key: {result.stderr.decode()}")
    else:
        print("Private key generated successfully.")


def generate_CSR(common_name, passphrase):
    # Generate the CSR (Certificate Signing Request) for the server
    cmd = ("openssl req -new -key chatserver-key.pem -out chatserver.csr "
           f"-subj /C=US/ST=California/L=Monterey/O=Team3/OU=PA4/CN={common_name} "
           f"-passin pass:{passphrase}")
    result = subprocess.run(cmd.split(" "), capture_output=True)
    if result.returncode != 0:
        print(f"Error generating CSR: {result.stderr.decode()}")
    else:
        print("CSR generated successfully.")


def generate_cert_from_CSR(passphrase):
    # Generate a certificate from the CSR
    cmd = ("openssl x509 -req -days 365 -in chatserver.csr -CA /etc/ssl/demoCA/cacert.pem "
           "-CAkey /etc/ssl/demoCA/private/cakey.pem -CAcreateserial -out chatserver-cert.pem "
           f"-passin pass:{passphrase}")
    result = subprocess.run(cmd.split(" "), capture_output=True)
    if result.returncode != 0:
        print(f"Error generating certificate: {result.stderr.decode()}")
    else:
        print("Certificate generated successfully.")


def put_into_place():
    # Move the certificate and key to the appropriate directories
    if os.path.exists('chatserver-cert.pem'):
        subprocess.run("sudo mv chatserver-cert.pem /etc/ssl/demoCA/newcerts/.".split())
    else:
        print("Error: chatserver-cert.pem not found.")

    if os.path.exists('chatserver-key.pem'):
        subprocess.run("sudo mv chatserver-key.pem /etc/ssl/demoCA/private/.".split())
    else:
        print("Error: chatserver-key.pem not found.")

    if os.path.exists('chatserver.csr'):
        subprocess.run("sudo mv chatserver.csr /etc/ssl/demoCA/.".split())
    else:
        print("Error: chatserver.csr not found.")


if __name__ == "__main__":

    # Prompt for common name and passphrase
    common_name = prompt_for_common_name()
    passphrase = prompt_for_passphrase()

    # Write the common name to a file for later reference
    write_common_name(common_name)

    # Update the /etc/hosts file with the new common name
    update_host_file(common_name)

    # Generate the private key with the provided passphrase
    generate_private_key(passphrase)

    # Generate the CSR using the common name
    generate_CSR(common_name, passphrase)

    # Generate the certificate from the CSR
    generate_cert_from_CSR(passphrase)

    # Place the certificates and key in the appropriate directories
    put_into_place()

    print("Certificate generation completed successfully.")
