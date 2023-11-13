from mininet.node import RemoteController,CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch, Host
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
class MyTopo( Topo ):

    def __init__( self ):
        Topo.__init__(self)
        
        # Add hosts and switches
        host1 = self.addHost('h1', cls=Host, ip='192.168.31.74/24', defaultRoute='via 192.168.31.1')
        host2 = self.addHost('h2', cls=Host, ip='192.168.31.75/24', defaultRoute='via 192.168.31.1')
        host3 = self.addHost('h3', cls=Host, ip='192.168.31.76/24', defaultRoute='via 192.168.31.1')
        host4 = self.addHost('h4', cls=Host, ip='192.168.31.77/24', defaultRoute='via 192.168.31.1')
	
        switch1 = self.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13', ip='192.168.31.1/24')
        switch2 = self.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13', ip='192.168.31.2/24')

# 更新连接的IP地址配置
        self.addLink(host1, switch1, 1, 1, intfName1='h1-eth0', params1={'ip': '192.168.31.74/24'})
        self.addLink(host2, switch1, 1, 2, intfName1='h2-eth0', params1={'ip': '192.168.31.75/24'})
        self.addLink(host3, switch2, 1, 1, intfName1='h3-eth0', params1={'ip': '192.168.31.76/24'})
        self.addLink(host4, switch2, 1, 2, intfName1='h4-eth0', params1={'ip': '192.168.31.77/24'})
        self.addLink(switch1, switch2, 3, 3)

topos = { 'mytopo': ( lambda: MyTopo() ) }

