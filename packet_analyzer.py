from filter_packets import filter
from packet_parser import parse
from compute_metrics import compute

filter()
node_data = parse()
compute(node_data)
