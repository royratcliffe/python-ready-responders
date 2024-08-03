from select import select
from dataclasses import dataclass
import socket

@dataclass
class Read:
    socket: any

@dataclass
class Write:
    socket: any

@dataclass
class Except:
    socket: any

class Sockets:
    """
    Zero or more sockets on which ready events yield by selection.
    """
    socks = []

    def ready(self, timeout=None):
        """
        Yields zero or more socket-ready events.
        """
        if len(self.socks) != 0:
            rlist, wlist, xlist = select(self.socks, self.socks, self.socks, timeout)
            for r in rlist:
                yield Read(r)
            for w in wlist:
                yield Write(w)
            for x in xlist:
                yield Except(x)

    def add(self, sock):
        self.socks.append(sock)
        return sock

    def bind_dgram(self, address):
        """
        Binds a datagram socket to an address.
        Datagram sockets do not listen with backlog nor accept.
        Sockets default to the Internet address family.
        """
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.bind(address)
        return self.add(sock)

    def connect_dgram(self, address):
        """
        Connects a datagram socket.
        """
        sock = socket.socket(type=socket.SOCK_DGRAM)
        sock.connect(address)
        return self.add(sock)

    def remove(self, sock):
        self.socks.remove(sock)
