import requests
from requests.auth import HTTPBasicAuth

def get_topology():
    # 控制器的IP地址和端口
    url = 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/'

    # 使用HTTP Basic Auth进行身份验证
    auth = HTTPBasicAuth('admin', 'admin')

    # 发送GET请求
    response = requests.get(url, auth=auth, headers={'Accept': 'application/json'})

    # 检查请求是否成功
    if response.status_code == 200:
        # 输出返回的JSON数据
        return (response.json())
    else:
        print('Failed to get network topology. HTTP response code:', response.status_code)
