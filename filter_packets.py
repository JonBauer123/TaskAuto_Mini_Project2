# This script filters out the the proper packets from a
# text wireshark capture.


def readFile(fd, L):
    f = open(fd, 'r')

    packetData = f.read().split('\n\nNo.')

    for packet in packetData:
        header = packet.split("\n")[1]
        if "ICMP" in header and "unreachable" not in header:
            L.append(packet)

    f.close()


def writeFilter(fd, L):
    f = open(fd, 'w')

    for packet in L:
        f.write(packet + "\n\nNo.")

    f.close()


def filter():
    for i in range(1, 5):
        # inFile = "Node" + str(i) + ".txt"
        inFile = "Node1.txt"
        L = []
        readFile(inFile, L)
        # outFile = "Node" + str(i) + "_filtered.txt"
        outFile = "Node1_filtered.txt"
        writeFilter(outFile, L)


if __name__ == "__main__":
    filter()
