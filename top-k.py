from scapy.all import *
import time
import resource

# 创建字典
flow_frequency = {}
start_time = time.time()
packets = rdpcap("trace1.pcap")

for packet in packets:
    if IP in packet:
        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        protocol = ip_layer.proto

        if protocol == 6:  # TCP
            flow = (src_ip, dst_ip, "TCP")
            # 构建特征元组
            if flow in flow_frequency:
                flow_frequency[flow] += 1
            else:
                flow_frequency[flow] = 1
        elif protocol == 17:  # UDP
            flow = (src_ip, dst_ip, "UDP")
            if flow in flow_frequency:
                flow_frequency[flow] += 1
            else:
                flow_frequency[flow] = 1

k = 30
top_flows = sorted(flow_frequency.items(), key=lambda x: x[1], reverse=True)[:k]
print("频率最高的流量：")
for flow, frequency in top_flows:
    src_ip, dst_ip, protocol = flow
    print("源IP:{},目的IP:{},协议类型：{},频率：{}".format(src_ip, dst_ip, protocol, frequency))

end_time = time.time()
runtime = end_time - start_time
memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # KB
print("运行时间：{:.3f}秒".format(runtime))
print("占用内存：{:.2f}KB".format(memory_usage))

