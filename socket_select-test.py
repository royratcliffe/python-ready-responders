import socket_select
import time
import sys

sockets = socket_select.Sockets()
server = sockets.bind_dgram(('', 9876))
client = sockets.connect_dgram(('localhost', 9876))

# Shared memory context for demonstration purposes.
# Access is synchronous between ready-responders.
count = 0
start = time.monotonic()

while time.monotonic() < start + 10:
    readies = list(sockets.ready(1.0))
    # In practice, there will always be sockets ready unless they all close.
    if len(readies) == 0:
        break
    for ready in readies:
        match ready:
            case socket_select.Write(sock) if sock == client:
                sock.send(str(count).encode())
                count += 1
                if count == 10:
                    sock.close()
                    sockets.remove(sock)
            case socket_select.Read(sock) if sock.getsockname()[1] == 9876:
                # Demonstrates a guard condition by socket port.
                # Asking for the peer name raises an exception if not connected.
                # This includes bound datagram sockets.
                data = sock.recv(1024)
                print(data)

sys.exit(0)
