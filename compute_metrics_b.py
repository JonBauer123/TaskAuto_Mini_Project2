def compute_b(nodes):
    for node in nodes:
        rtt_sum = 0
        frame_total = 0
        payload_total = 0
        count = len(node.pings)

        for ping in node.pings:
            rtt = (ping.reply.time - ping.request.time) * 1000

            rtt_sum += rtt
            frame_total += ping.request.total_length
            payload_total += ping.request.content_length

        print("Average RTT {}".format(rtt_sum / count))
        print("Echo Request Throughput {}".format(frame_total / rtt_sum))
        print("Echo Request Goodput {}".format(payload_total / rtt_sum))