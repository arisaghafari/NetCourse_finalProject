from mininet.net import Mininet
from mininet.node import CPULimitedHost #cpu Related settings
from mininet.link import TCLink # addLink Related settings
from mininet.util import dumpNodeConnections 
from mininet.log import setLogLevel 


def IperfTest():  
    net = Mininet(host=CPULimitedHost, link=TCLink)
    # Create network node
    #c0 = net.addController()

    # Add hosts
    h1 = net.addHost( 'h1' )
    h2 = net.addHost( 'h2' )
    h3 = net.addHost( 'h3' )
    h4 = net.addHost( 'h4' )

    # Add switchs
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    # Add links
    net.addLink( h1, s1 , bw = 100 , delay='0.1ms')
    net.addLink( h1, s3 , bw = 100 , delay='0.1ms')
    net.addLink( h3, s3 , bw = 100 , delay='0.1ms')
    net.addLink( s1, s2 , bw = 10 ) #A
    net.addLink( s3, s4 , bw = 20 ) #B
    net.addLink( s2, h2 , bw = 100 , delay='0.1ms')
    net.addLink( s4, h2 , bw = 100 , delay='0.1ms')
    net.addLink( s4, h4 , bw = 100 , delay='0.1ms')

    # Configure host ip
    h1.setIP('10.0.0.1', 24)
    h2.setIP('10.0.0.2', 24)
    h3.setIP('10.0.0.3', 24)
    h4.setIP('10.0.0.4', 24)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    h1.cmd('ping -c1 %s' % h2.IP())
    # print("Testing bandwidth")
    # h1, h2, h3 = net.get('h1', 'h2', 'h3')
    # net.iperf((h1,h2))
    # net.iperf((h2,h3))
    # net.iperf((h1,h3))
    # net.pingAll()
    net.stop()

if __name__=='__main__':
    setLogLevel('info') #print the log when Configuring hosts, starting switches and controller     
    IperfTest()
