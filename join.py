import netifaces

import socket
import struct

# Get the IP address of the first available local interface
local_interface = None
interfaces = netifaces.interfaces()

for interface in interfaces:
    if netifaces.AF_INET in netifaces.ifaddresses(interface):
        addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
        if addresses:
            local_interface = addresses[0]['addr']
            print(interface)
            break

if not local_interface:
    raise ValueError("No valid local interface found")

print("Local interface IP:", local_interface)

print('Enter your multicast_group:')
x = input()

print('Enter your multicast_port:')
y = input()

# Specify the multicast group address and port
multicast_group = x
multicast_port = int(y)

# Specify the IP address of the local interface
# local_interface = '172.20.1.107'

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket options to enable multicast
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# Bind the socket to the local interface and port
sock.bind((local_interface, multicast_port))

# Join the multicast group on the specified interface
group = socket.inet_aton(multicast_group)
interface = socket.inet_aton(local_interface)
mreq = group + interface
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive and process incoming multicast messages
while True:
    data, addr = sock.recvfrom(1024)
    decoded_data = data.decode('utf-8', errors='replace')
    print("Received message:", decoded_data)
# Close the socket
sock.close()