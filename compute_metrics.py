def compute(nodes):
	print('called compute function in compute_metrics.py')

	for thing in nodes:
		for i in range(0,len(thing.packets)):
			if thing.packets[i].type == "request":
				print "REQUEST: " + thing.packets[i].src
			if thing.packets[i].type == "reply":
				print "REPLEY: " + thing.packets[i].dst

		print "-----------------"