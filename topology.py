import os
import time
from os import link
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import Host
import time
from subprocess import Popen, PIPE
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf

class CustomTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
         # Add hosts
        h1 = self.addHost( 'Host1' )
        h2 = self.addHost( 'Host2' )
        h3 = self.addHost( 'Host3' )
        h4 = self.addHost( 'Host4' )

        # Add switchs
        s_left_up = self.addSwitch('s1')
        s_right_up = self.addSwitch('s2')
        s_left_down = self.addSwitch('s3')
        s_right_down = self.addSwitch('s4')

        # Add links
        self.addLink( h1, s_left_up , bw = 100 , delay='0.1ms')
        self.addLink( h1, s_left_down , bw = 100 , delay='0.1ms')
        self.addLink( h3, s_left_down , bw = 100 , delay='0.1ms')
        self.addLink( s_left_up, s_right_up , bw = 10 ) #A
        self.addLink( s_left_down, s_right_down , bw = 20 ) #B
        self.addLink( s_right_up, h2 , bw = 100 , delay='0.1ms')
        self.addLink( s_right_down, h2 , bw = 100 , delay='0.1ms')
        self.addLink( s_right_down, h4 , bw = 100 , delay='0.1ms')

def prefTest(net):
    #topo = CustomTopo()
    #net = Mininet(topo = topo, host = Host, link = TCLink)
    #net.start()
    
    h1, h2 = net.get('Host1', 'Host2')
    h3, h4 = net.get('Host3', 'Host4')

    h2.cmd("iperf -s &> h2_iperf_server.log &")
    h4.cmd("iperf -s &> h4_iperf_server.log &")

    h1.cmd("iperf -c 10.0.1.1 -t 50 &> h1_iperf.log &")
   # h1.cmd("iperf -c" + h2.IP() + " -t 50 &> h1_iperf.log &")
#    h1.cmd("ping " + h2.IP() + " > h1_ping.log &")
    h1.cmd("ping 10.0.1.1 > h1_ping.log &")
    print "sleep 1"
    time.sleep(10)

    h3.cmd("iperf -c" + h4.IP() + " -t 20 &> h3_iperf.log &")
    h3.cmd("ping " + h4.IP() + " > h3_ping.log &")

    print "sleep 2"
    time.sleep(50)

    #net.stop()

def main():
    # Making sure MPTCP is enabled on system and congestion control algorithm modules are loaded
    os.system('modprobe mptcp_balia; modprobe mptcp_wvegas; modprobe mptcp_olia; modprobe mptcp_coupled')
    os.system('sysctl -w net.mptcp.mptcp_enabled=1')
    os.system('sysctl -w net.mptcp.mptcp_path_manager=fullmesh')
    os.system('sysctl -w net.mptcp.mptcp_scheduler=default')

    topo = CustomTopo()
    net = Mininet(topo = topo, host = Host, link = TCLink)
    print "start"
    net.start()
 
   # Test throughput for different configurations
    for cc in ['lia', 'olia', 'balia', 'wvegas']:
        print('\n#### Testing bandwidth for {}####'.format(cc))

        # set congestion control algoritm
        os.system('sysctl -w net.ipv4.tcp_congestion_control={}'.format(cc))

        # test bandwidth between the two hosts
        src = net.get('Host1')
        dst = net.get('Host2')
        serverbw, _clientbw = net.iperf([src, dst], seconds=10)
        # print('BW on Server: {}'.format(serverbw))

        # CLI(net)
    print "stop"
    net.stop()

def MPTCP(net):
    #topo = CustomTopo()
    #net = Mininet(topo = topo, host = Host, link = TCLink)
    #net.start()
    
    h1, h2 = net.get('Host1', 'Host2')

    h1.cmd("ifconfig Host1-eth0 0")
    h1.cmd("ifconfig Host1-eth1 0")
    h2.cmd("ifconfig Host2-eth0 0")
    h2.cmd("ifconfig Host2-eth1 0")
    h1.cmd("ifconfig Host1-eth0 10.0.2.2 netmask 255.255.255.0")
    h1.cmd("ifconfig Host1-eth1 10.0.1.2 netmask 255.255.255.0")
    h2.cmd("ifconfig Host2-eth0 10.0.2.1 netmask 255.255.255.0")
    h2.cmd("ifconfig Host2-eth1 10.0.1.1 netmask 255.255.255.0")
    h1.cmd("ip rule add from 10.0.2.2 table 1")
    h1.cmd("ip rule add from 10.0.1.2 table 2")
    h1.cmd("ip route add 10.0.2.0/24 dev Host1-eth0 scope link table 1")
    h1.cmd("ip route add default via 10.0.2.1 dev Host1-eth0 table 1")
    h1.cmd("ip route add 10.0.1.0/24 dev Host1-eth1 scope link table 2")
    h1.cmd("ip route add default via 10.0.1.1 dev Host1-eth1 table 2")
    h1.cmd("ip route add default scope global nexthop via 10.0.2.1 dev Host1-eth0")
    h2.cmd("ip rule add from 10.0.2.1 table 1")
    h2.cmd("ip rule add from 10.0.1.1 table 2")
    h2.cmd("ip route add 10.0.2.0/24 dev Host2-eth0 scope link table 1")
    h2.cmd("ip route add default via 10.0.2.2 dev Host2-eth0 table 1")
    h2.cmd("ip route add 10.0.1.0/24 dev Host2-eth1 scope link table 2")
    h2.cmd("ip route add default via 10.0.1.2 dev Host2-eth1 table 2")
    h2.cmd("ip route add default scope global nexthop via 10.0.2.2 dev Host2-eth0")

if __name__=='__main__':
    topo = CustomTopo()
    net = Mininet(topo = topo, host = Host, link = TCLink)
   # key = "net.mptcp.mptcp_enabled"
   # value = 1
   # p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
   # stdout, stderr = p.communicate()
   # print "stdout=",stdout,"stderr=", stderr
    net.start()    
    MPTCP(net)
    prefTest(net)
    net.stop()
