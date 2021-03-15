import socket

'''
    https://gqrx.dk/doc/streaming-audio-over-udp
    
    GQRX Import format
    Channels: 1 (left)
    Sample rate: 48 kHz
    Sample format: 16 bit signed, little endian (S16LE)
'''

# localhost
UDP_IP = "127.0.0.1"

# GQRX default port
UDP_PORT = 7355

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
    print("Received data: %s" % data)
    
