import struct
import socket

INPUT_PATH = "Node1_filtered.txt"
PACKET_FORMAT = "!" + ("x" * 14) + "xxHxxxxBxxxLL" + "BxxHH"
# length, ttl, source, dest, type, code, checksum, rest


class Packet:
    def __init__(self, bytes):
        length, ttl, src, dst, type, ident, seq = struct.unpack(PACKET_FORMAT, str(bytes[:struct.calcsize(PACKET_FORMAT)]))
        self.src = socket.inet_ntoa(struct.pack('!L', src))
        self.dst = socket.inet_ntoa(struct.pack('!L', dst))
        self.seq = "{}/{}".format(ident, seq)
        self.ttl = ttl
        self.type = "request" if type == 8 else "reply"

    def __str__(self):
        return "{}: {} -> {}".format(self.seq, self.src, self.dst)


class Ping:
    def __init__(self, request, reply):
        self.request = request
        self.reply = reply

        # self.total_sent =
        # self.total_received =
        # self.payload_sent =
        # self.payload_recevied =

    def __str__(self):
        return "({} / {}): {} -> {}".format(self.request.seq, self.reply.seq, self.request.src, self.request.dst)


def parse():
    unmatched_requests = {}
    pings = []
    packets = []

    with open(INPUT_PATH) as f:
        text = f.read()
        packet_datas = text.split("\n\nNo.")
        for packet_data in packet_datas:
            if not packet_data:
                continue

            trimmed_data = packet_data.split("\n")[3:]
            trimmed_data = "".join(map(lambda x: x[6:53].replace(" ", ""), trimmed_data))
            packet_bytes = bytearray.fromhex(trimmed_data)
            packet = Packet(packet_bytes)

            if packet.type == "request":
                unmatched_requests[packet.seq] = packet
            else:
                pings.append(Ping(unmatched_requests[packet.seq], packet))

            packets.append(packet)

    return packets, pings

if __name__ == '__main__':
    parse()
