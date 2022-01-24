from os import link
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.node import Host
import time

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
    
def prefTest():
    topo = CustomTopo()
    net = Mininet(topo = topo, host = Host, link = TCLink)
    print("net start ...")
    net.start()
    
    h1, h2 = net.get('Host1', 'Host2')
    h3, h4 = net.get('Host3', 'Host4')

    print "h2 iperf running"
    # h2 iperf -s &> h2.log &
    h2.cmd("fsystemctl stop firewalld.service  &> h2.log &")
    h2.cmd("iperf -s &> h2_iperf_server.log &")
    print "h4 iperf running"
    h4.cmd("iperf -s &> h4_iperf_server.log &")

    # print "h1 iperf running"
    # net.iperf( ( h1, h2 ), l4Type='UDP' )

    # h1 iperf -t 120 -c 10.0.0.2 &> h1.log &
    # print "h2 ip : " + h2.IP()
    # h1.cmd("systemctl stop firewalld.service  &> h1.log &")
    h1.cmd("iperf -c" + h2.IP() + " -t 50 &> h1_iperf.log")
    # print "h1 ping running"
    # h1.cmd("ping " + h2.IP() + " > h1_ping.txt &")

    print "sleep 1"
    time.sleep(10)

    print "h3 iperf running"
    h3.cmd("iperf -c" + h4.IP() + " -t 20 &> h3_iperf.log")
    # print "h3 ping running"
    # h3.cmd("ping " + h4.IP() + " > h3_ping.txt &")

    print "sleep 2"
    time.sleep(50)

    print "net stop"
    net.stop()

if __name__=='__main__':
    prefTest()








# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.link import TCLink
# from mininet.util import dumpNodeConnections

# class DumbbellTopo(Topo):
#     def __init__( self ):
#         "Create custom topo."
#         Topo.__init__( self )
#          # Add hosts
#         h1 = self.addHost( 'h1' )
#         h2 = self.addHost( 'h2' )
#         h3 = self.addHost( 'h3' )
#         h4 = self.addHost( 'h4' )

#         # Add switchs
#         s1 = self.addSwitch('s1')
#         s2 = self.addSwitch('s2')
#         s3 = self.addSwitch('s3')
#         s4 = self.addSwitch('s4')

#         # Add links
#         self.addLink( h1, s1 ,cls=TCLink, bw = 100 , delay='0.1ms')
#         self.addLink( h1, s3 ,cls=TCLink, bw = 100 , delay='0.1ms')
#         self.addLink( h3, s3 ,cls=TCLink, bw = 100 , delay='0.1ms')
#         self.addLink( s1, s2 ,cls=TCLink, bw = 10 ) #A
#         self.addLink( s3, s4 ,cls=TCLink, bw = 20 ) #B
#         self.addLink( s2, h2 ,cls=TCLink, bw = 100 , delay='0.1ms')
#         self.addLink( s4, h2 ,cls=TCLink, bw = 100 , delay='0.1ms')
#         self.addLink( s4, h4 ,cls=TCLink, bw = 100 , delay='0.1ms')


# def dumbbell_test():
#     """ Create and test a dumbbell network.
#     """
#     topo = DumbbellTopo()
#     net = Mininet(topo)
#     net.start()

#     print("Dumping host connections...")
#     # dumpNodeConnections(net.hosts)

#     print("Testing network connectivity...")
#     h1, h2 = net.get('h1', 'h2')
#     h3, h4 = net.get('h3', 'h4')

#     # for i in range(1, 10):
#     #     net.pingFull(hosts=(h1, h2))

#     # for i in range(1, 10):
#     #     net.pingFull(hosts=(h2, h1))

#     # for i in range(1, 10):
#     #     net.pingFull(hosts=(h4, h3))

#     # for i in range(1, 10):
#     #     net.pingFull(hosts=(h3, h4))

#     print("Testing bandwidth between h1 and h2...")
#     # net.iperf(hosts=(h1, h2), fmt='m', seconds=10, port=5001)
#     # net.iperf([h1, h2])
#     h1.cmd("iperf -c "+h2.IP()+" -t 50 > h1_iperf.txt")
#     h2.cmd("iperf -s  > h2_iperf_server.txt")
    

#     print("Testing bandwidth between h3 and h4...")
#     # net.iperf(hosts=(h3, h4), fmt='m', seconds=10, port=5001)
#     net.iperf([h3, h4])

#     print("Stopping test...")
#     net.stop()

# if __name__=='__main__':
#     dumbbell_test()

# from distutils.command.build import build
# from mininet.net import Mininet
# from mininet.node import OVSSwitch, Controller, RemoteController
# from mininet.topolib import TreeTopo
# from mininet.log import setLogLevel
# from mininet.cli import CLI

# setLogLevel( 'info' )

# Two local and one "external" controller (which is actually c0)
# Ignore the warning message that the remote isn't (yet) running
# c0 = Controller( 'c0', port=6633 )
# c1 = Controller( 'c1', port=6634 )
#c2 = RemoteController( 'c2', ip='127.0.0.1', port=6633 )

#cmap = { 's1': c0, 's2': c1, 's3': c2 }

# class MultiSwitch( OVSSwitch ):
#     "Custom Switch() subclass that connects to different controllers"
#     def start( self, controllers ):
#         return OVSSwitch.start( self, [ cmap[ self.name ] ] )

# net = Mininet(build = False)
# net = Mininet( topo=topo, switch=MultiSwitch, build=False )

# Add hosts
# h1 = net.addHost( 'h1' )
# h2 = net.addHost( 'h2' )
# h3 = net.addHost( 'h3' )
# h4 = net.addHost( 'h4' )

#     # Add switchs
# s1 = net.addSwitch('s1')
# s2 = net.addSwitch('s2')
# s3 = net.addSwitch('s3')
# s4 = net.addSwitch('s4')

#     # Add links
# net.addLink( h1, s1 )#, bw = 100 , delay='0.1ms')
# net.addLink( h1, s3 )#, bw = 100 , delay='0.1ms')
# net.addLink( h3, s3 )#, bw = 100 , delay='0.1ms')
# net.addLink( s1, s2 )#, bw = 10 ) #A
# net.addLink( s3, s4 )#, bw = 20 ) #B
# net.addLink( s2, h2 )#, bw = 100 , delay='0.1ms')
# net.addLink( s4, h2 )#, bw = 100 , delay='0.1ms')
# net.addLink( s4, h4 )#, bw = 100 , delay='0.1ms')
# for c in [ c0, c1 ]:
#     net.addController(c)
# net.build()
# net.start()
# CLI( net )
# net.stop()



# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.node import CPULimitedHost
# from mininet.link import TCLink
# from mininet.util import dumpNodeConnections
# from mininet.log import setLogLevel
# from mininet.node import Controller, RemoteController, OVSController
# from mininet.cli import CLI
# from sys import argv

# def Topology():
# 	net = Mininet(controller= Controller)#, switch = OVSSwitch)
	
# 	print("******** Creating controller")
# 	c1= net.addController ('c1', ip='127.0.0.1', port = 6633)
	
# 	print("******** Creating switches")
# 	s1 = net.addSwitch( 's1' )
# 	s2 = net.addSwitch( 's2' )

# 	print("******** Creating host")
# 	h1 = net.addHost( 'h1' )
# 	h2 = net.addHost( 'h2' )
	
# 	print("******** Creating links")
# 	net.addLink (h1,s1)
# 	net.addLink (h2,s2)
# 	net.addLink (s1,s2)

# 	print("******* Starting network")
# 	net.build()
    
# 	c1.start
# 	s1.start([c1])
# 	s2.start([c1])
	
# 	net.start()

# 	print("******* Testing network")
# 	net.pingAll()

# 	print("****** Running CLI")
# 	CLI(net)

# if __name__ == '__main__':
#     setLogLevel( 'info' )
#     # Prevent test_simpleperf from failing due to packet loss
#     Topology()


# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.node import CPULimitedHost
# from mininet.link import TCLink
# from mininet.util import dumpNodeConnections
# from mininet.log import setLogLevel
# from mininet.node import Controller, RemoteController, OVSController
# from sys import argv

# class SingleSwitchTopo(Topo):
#     "Single switch connected to n hosts."
#     def __init__(self, n=2, lossy=True, **opts):
#         Topo.__init__(self, **opts)
#         switch = self.addSwitch('s1')
#         for h in range(n):
#             # Each host gets 50%/n of system CPU
#             host = self.addHost('h%s' % (h + 1),
#                                 cpu=.5 / n)
#             if lossy:
#                 # 10 Mbps, 5ms delay, 10% packet loss
#                 self.addLink(host, switch,
#                              bw=10, delay='5ms', loss=10, use_htb=True)
#             else:
#                 # 10 Mbps, 5ms delay, no packet loss
#                 self.addLink(host, switch,
#                              bw=10, delay='5ms', loss=0, use_htb=True)


# def perfTest( lossy=True ):
#     "Create network and run simple performance test"
#     topo = SingleSwitchTopo( n=4, lossy=lossy )
#     net = Mininet( topo=topo,
#                    host=CPULimitedHost, link=TCLink,
#                    autoStaticArp=True , controller = RemoteController)
#     net.start()
#     print("Dumping host connections")
#     dumpNodeConnections(net.hosts)
#     print("Testing bandwidth between h1 and h4")
#     h1, h4 = net.getNodeByName('h1', 'h4')
#     #net.iperf( ( h1, h4 ), l4Type='UDP' )
#     net.pingAll()
#     net.stop()

# if __name__ == '__main__':
#     setLogLevel( 'info' )
#     # Prevent test_simpleperf from failing due to packet loss
#     perfTest( lossy=( 'testmode' not in argv ) )





# from mininet.net import Mininet
# from mininet.node import CPULimitedHost #cpu Related settings
# from mininet.link import TCLink # addLink Related settings
# from mininet.util import dumpNodeConnections 
# from mininet.log import setLogLevel 
# from mininet.node import OVSSwitch, Controller, RemoteController


# def IperfTest():  
#     net = Mininet(host=CPULimitedHost, link=TCLink)
#     # Create network node
#     # c0 = net.addController()
#     c0 = Controller( 'c0', port=6633 )
#     # c1 = Controller( 'c1', port=6634 )

#     # Add hosts
#     h1 = net.addHost( 'h1' )
#     # h2 = net.addHost( 'h2' )
#     h3 = net.addHost( 'h3' )
#     h4 = net.addHost( 'h4' )

#     # Add switchs
#     # s1 = net.addSwitch('s1')
#     # s2 = net.addSwitch('s2')
#     s3 = net.addSwitch('s3')
#     s4 = net.addSwitch('s4')

#     # Add links
#     # net.addLink( h1, s1 )#, bw = 100 , delay='0.1ms')
#     net.addLink( h1, s3 )#, bw = 100 , delay='0.1ms')
#     net.addLink( h3, s3 )#, bw = 100 , delay='0.1ms')
#     # net.addLink( s1, s2 )#, bw = 10 ) #A
#     net.addLink( s3, s4 )#, bw = 20 ) #B
#     # net.addLink( s2, h2 )#, bw = 100 , delay='0.1ms')
#     # net.addLink( s4, h2 )#, bw = 100 , delay='0.1ms')
#     net.addLink( s4, h4 )#, bw = 100 , delay='0.1ms')

#     net.addController(c0)
#     # Configure host ip
#     # h1.setIP('10.0.0.1', 24)
#     # h2.setIP('10.0.0.2', 24)
#     # h3.setIP('10.0.0.3', 24)
#     # h4.setIP('10.0.0.4', 24)
#     net.build()
#     net.start()
#     print("Dumping host connections")
#     dumpNodeConnections(net.hosts)
#     print("Testing network connectivity")
#     net.pingAll()
#     print(h1.cmd('ping -c1 %s' % h2.IP()))
#     # print("Testing bandwidth")
#     # h1, h2, h3 = net.get('h1', 'h2', 'h3')
#     # net.iperf((h1,h2))
#     # net.iperf((h2,h3))
#     # net.iperf((h1,h3))
#     # net.pingAll()
#     net.stop()

# if __name__=='__main__':
#     setLogLevel('info') #print the log when Configuring hosts, starting switches and controller     
#     IperfTest()
