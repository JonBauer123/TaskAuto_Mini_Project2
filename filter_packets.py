# This script filters out the the proper packets from a
# text wireshark capture.
def readFile(fd, L):
	f = open(fd, 'r')
	
	packetData = f.read().split('\n\n')

	for line in packetData:
		line = line.split()
		check = True
		if "ICMP" in line[11]:
			for word in line:
				if "unreachable" in word:
					check = False
					break
			
			if check == True:
				L.append(line)

	f.close()

def writeFilter(fd, L):
	f = open(fd, 'w')
	
	for line in L:
		for word in line[7::]:
			f.writelines(word)
			f.writelines(" ")
		f.writelines("\n")

	f.close()

def filter() :
	print 'called filter function in filter_packets.py'

	for i in range (1,5):
		#inFile = "Node" + str(i) + ".txt"
		inFile = "Node1.txt"
		L = []
		readFile(inFile, L)
		#outFile = "Node" + str(i) + "_filtered.txt"
		outFile = "Node1_filtered.txt"
		writeFilter(outFile, L)

if __name__ == "__main__":
	filter()