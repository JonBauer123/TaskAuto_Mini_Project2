def compute(nodes):
	print('called compute function in compute_metrics.py')


	for thing in nodes:
		request_sent = 0
		request_rec = 0
		repley_sent = 0
		repley_rec = 0

		bytes_sent = 0
		bytes_rec = 0

		data_sent = 0
		data_rec = 0
		for i in range(0,len(thing.packets)):
			if thing.packets[i].type == "request":
				if thing.packets[i].src == "192.168.100.1":
					request_sent+=1
					bytes_sent+=thing.packets[i].total_length
					data_sent+=thing.packets[i].content_length
				else:
					request_rec+=1
					bytes_rec+=thing.packets[i].total_length
					data_rec+=thing.packets[i].content_length
			if thing.packets[i].type == "reply":
				if thing.packets[i].src == "192.168.100.1":
					repley_sent+=1
				else:
					repley_rec+=1


		print "Request Sent: " + str(request_sent)
		print "Request Rec: " + str(request_rec)
		print "Request Sent: " + str(repley_sent)
		print "Request Rec: " + str(repley_rec)

		print "Bytes Sent: " + str(bytes_sent)
		print "Bytes Rec: " + str(bytes_rec)
		print "Data Sent: " + str(data_sent)
		print "Data Rec: " + str(data_rec)
		break

		