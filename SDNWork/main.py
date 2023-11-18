from flask import Flask, render_template, g,jsonify,request
import random
import time
import numpy as np
import get_topo
import CountMinSketch
import TopK
import subprocess

app = Flask(__name__)
alert_info = []

# class CountMinSketch:
#     def __init__(self, width, depth):
#         self.width = width
#         self.depth = depth
#         self.sketch = np.zeros((depth, width), dtype=int)
#     def update(self, key):
#         for i in range(self.depth):
#             hash_value = hash(str(i) + str(key)) % self.width
#             self.sketch[i, hash_value] += 1
#     def estimate(self, key):
#         min_count = float('inf')
#         for i in range(self.depth):
#             hash_value = hash(str(i) + str(key)) % self.width
#             min_count = min(min_count, self.sketch[i, hash_value])
#         return min_count
# def get_count_min_sketch():
#     if 'count_min_sketch' not in g:
#         g.count_min_sketch = CountMinSketch(width=100, depth=5)
#     return g.count_min_sketch
#
# def generate_traffic():
#     traffic = []
#     for _ in range(1000):  # 生成一些正常流量包
#         source_ip = f"192.168.0.{random.randint(1, 10)}"
#         traffic.append({"source_ip": source_ip})
#     # 在流量中添加一些重流的示例
#     for _ in range(50):  # 生成一些重流
#         source_ip = f"192.168.0.{random.randint(1, 5)}"  # 重流集中在前五个IP
#         traffic.append({"source_ip": source_ip})
#     return traffic
#
#
# def process_traffic(traffic):
#     dict = {}
#     with app.app_context():  # 确保在应用上下文中执行
#         count_min_sketch = get_count_min_sketch()
#         threshold = 100  # 阈值，
#         for packet in traffic:
#             key = packet["source_ip"]
#             count_min_sketch.update(key)
#             count = count_min_sketch.estimate(key)
#             # print(f"Key: {key}, Count: {count}")  # 添加打印语句
#             if count > threshold:
#                 dict[key] = count;
#                 # print(f"Key: {key}, Count: {count}")  # 添加打印语句
#                 # print(dict[key])
#         for key, value in dict.items():
#             alert_info.append(f"Heavy Hitter Detected: {key} with count {value}")

@app.route('/')
def index():
    return render_template('index.html', alert_info=alert_info)

@app.route('/api/create-topology', methods=['POST'])
def api_create_topology():
    data = request.get_json()
    file_path = data.get('file')
    controller_ip = data.get('controller', {}).get('ip')
    controller_port = data.get('controller', {}).get('port')

    command = f"sudo mn --custom {file_path} --topo mytopo --controller=remote,ip={controller_ip},port={controller_port} --switch ovsk,protocols=OpenFlow13"
    subprocess.Popen(command, shell=True)

    return jsonify({"result": "success"})

@app.route('/api/topology', methods=['GET'])
def api_topology():
    topology = get_topo.get_topology()
    return jsonify(topology)

@app.route('/api/countmin', methods=['GET'])
def api_countmin():
    print("counting..")
    result = CountMinSketch.do_CountMin()  # 调用do_CountMin()函数获取结果
    return result

@app.route('/api/topk', methods=['GET'])
def api_topk():
    k = int(request.args.get('k'))  # 获取前端传递的k值
    print("begin to analyze packets")
    result = TopK.analyze_packets("traces/packet.pcap", k)  # 调用analyze_packets函数进行流量分析
    return jsonify(result)
if __name__ == '__main__':
    # traffic = generate_traffic()
    # process_traffic(traffic)
    app.run()
