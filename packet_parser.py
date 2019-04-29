import struct
import socket

INPUT_PATH = "Node{}_filtered.txt"
PACKET_FORMAT = "!" + ("x" * 14) + "xxHxxxxBxxxLL" + "BxxHH"
# length, ttl, source, dest, type, code, checksum, rest


class Packet:
    def __init__(self, bytes, id, time):
        length, ttl, src, dst, type, ident, seq = struct.unpack(PACKET_FORMAT, str(bytes[:struct.calcsize(PACKET_FORMAT)]))
        self.src = socket.inet_ntoa(struct.pack('!L', src))
        self.dst = socket.inet_ntoa(struct.pack('!L', dst))
        self.seq = "{}/{}".format(ident, seq)
        self.ttl = ttl

        if type == 8:
            self.type = "request"
        elif type == 0:
            self.type = "reply"
        else:
            raise Exception()

        self.time = time
        self.id = id

        self.total_length = len(bytes)
        self.content_length = len(bytes) - 42

    def __str__(self):
        return "{}: {} -> {}".format(self.id, self.src, self.dst)


class Ping:
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply

    def __str__(self):
        return "({} / ()): {} -> {}".format(self.request.id, self.reply.id, self.request.src, self.request.dst)


class Node:
    def __init__(self, packets, pings, id):
        self.packets = packets
        self.pings = pings
        self.id = id


def parse():
    nodes = []

    for i in range(1, 5):
        unmatched_requests = {}
        pings = []
        packets = []

        with open(INPUT_PATH.format(i)) as f:
            text = f.read()
            packet_datas = text.split("\n\nNo.")
            for packet_data in packet_datas:
                if not packet_data:
                    continue

                id, time = filter(None, packet_data.split("\n")[1].split(" "))[:2]

                trimmed_data = packet_data.split("\n")[3:]
                trimmed_data = "".join(map(lambda x: x[6:53].replace(" ", ""), trimmed_data))
                packet_bytes = bytearray.fromhex(trimmed_data)
                packet = Packet(packet_bytes, int(id), float(time))

                if packet.type == "request":
                    unmatched_requests[packet.seq] = packet
                else:
                    pings.append(Ping(unmatched_requests[packet.seq], packet))

                packets.append(packet)
        nodes.append(Node(packets, pings, i))

    return nodes

if __name__ == '__main__':
    parse()
