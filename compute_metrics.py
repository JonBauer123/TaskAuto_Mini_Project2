def i_started(request, i):
    src = request.src
    if src == "192.168.100.1" and i == 1:
        return True
    if src == "192.168.100.2" and i == 2:
        return True
    if src == "192.168.200.1" and i == 3:
        return True
    if src == "192.168.200.2" and i == 4:
        return True

    return False


def compute(nodes):

    node_datas = []

    for node in nodes:
        request_sent = 0
        request_rec = 0
        repley_sent = 0
        repley_rec = 0

        bytes_sent = 0
        bytes_rec = 0

        data_sent = 0
        data_rec = 0

        rtt_sum = 0
        frame_total = 0
        payload_total = 0
        count = 0
        hop_count = 0
        reply_delay_sum = 0
        reply_delay_count = 0

        node_data = [node.id]

        for i in range(0, len(node.packets)):
            if node.packets[i].type == "request":
                if i_started(node.packets[i], node.id):  # node.packets[i].src == "192.168.100.1":
                    request_sent += 1
                    bytes_sent += node.packets[i].total_length
                    data_sent += node.packets[i].content_length
                else:
                    request_rec += 1
                    bytes_rec += node.packets[i].total_length
                    data_rec += node.packets[i].content_length
            if node.packets[i].type == "reply":
                if i_started(node.packets[i], node.id):  # node.packets[i].src == "192.168.100.1":
                    repley_sent += 1
                else:
                    repley_rec += 1

        node_data.append(request_sent)
        node_data.append(request_rec)
        node_data.append(repley_sent)
        node_data.append(repley_rec)

        node_data.append(bytes_sent)
        node_data.append(bytes_rec)
        node_data.append(data_sent)
        node_data.append(data_rec)

        for ping in node.pings:
            if not i_started(ping.request, node.id):
                reply_delay_sum += (ping.reply.time - ping.request.time) * 1000000
                reply_delay_count += 1
                continue

            rtt = (ping.reply.time - ping.request.time) * 1000

            rtt_sum += rtt
            frame_total += ping.request.total_length
            payload_total += ping.request.content_length
            count += 1
            hop_count += ping.request.ttl - ping.reply.ttl + 1

        node_data.append(rtt_sum / count)
        node_data.append(frame_total / rtt_sum)
        node_data.append(payload_total / rtt_sum)
        node_data.append(reply_delay_sum / reply_delay_count)

        node_data.append(float(hop_count) / count)

        node_datas.append(node_data)

    write(node_datas)


def write(node_datas):
    template = """Node {0}

Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received
{1},{2},{3},{4}
Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)
{5},{6}
Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)
{7},{8}

Average RTT (milliseconds),{9:.2f}
Echo Request Throughput (kB/sec),{10:.1f}
Echo Request Goodput (kB/sec),{11:.1f}
Average Reply Delay (microseconds),{12:.2f}
Average Echo Request Hop Count,{13:.2f}

"""

    with open("output.csv", "w+") as f:
        for node_data in node_datas:
            f.write(template.format(*node_data))
