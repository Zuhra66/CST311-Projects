import socket
from pathlib import Path
import argparse
import re

def run_server(HOST, PORT, report_location):

    # set save location for report
    report_location = report_location if report_location else Path.cwd()

    # open a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        hb_truth = 1
        missing_msg = "Missing UDP heartbeat"
        print('Server listening on {}:{}'.format(HOST, PORT))

        # Start loop listening for incoming udp packets
        while True:
            data, addr = s.recvfrom(1024)
            ip = addr[0]

            # Open file for report writing
            with open(f"{report_location}/server_hb_report_{ip}.txt", 'a') as f:
                if not data:
                    msg = missing_msg
                else:
                    try:
                        # Parse incoming message conforming to heartbeat message format
                        sequence, time = re.findall(r'sequence\s+(\d+),\s+time\s+([\d:]+)', data.decode())[0]
                        sequence = int(sequence)
                        msg = f"Messages received: sequence {sequence}, time {time}"
                    except IndexError:
                        msg = missing_msg

                    # If heartbeat truth is less than recieved heartbeat, means we dropped a heartbeat
                    if hb_truth < sequence:
                        # for number of missed heartbeats, print missing message
                        for count in range(sequence - hb_truth):
                            f.write(f"HB {hb_truth}: {missing_msg}\n")
                            print(f"HB {hb_truth}: {missing_msg}")
                            hb_truth += 1
                    # If heartbeat truth is greater than recieved heartbeat, means client is starting
                    # heartbeat notifications over again
                    elif hb_truth > sequence:
                        hb_truth = 1
                        # for number of missed heartbeats, print missing message
                        for count in range(sequence - 1):
                            f.write(f"HB {hb_truth}: {missing_msg}\n")
                            print(f"HB {hb_truth}: {missing_msg}")
                            hb_truth += 1
           
                # Write out successfully recieved heartbeat message 
                f.write(f"HB {hb_truth}: {msg}\n")
                print(f"HB {hb_truth}: {msg}")
            hb_truth += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, type=str, help="Server's hostname or IP address")
    parser.add_argument("--port", required=True, type=int, help="Port number used by the server")
    parser.add_argument("--report", default=None, type=str, help="Location to save report, default to pwd")

    args = parser.parse_args()
    run_server(args.host, args.port, args.report)