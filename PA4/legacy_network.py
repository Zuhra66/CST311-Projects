#!/usr/bin/python

import subprocess
from mininet.net import Mininet
from mininet.node import Controller, Node, Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

# Step 1: Generate certificates using the certificate_generation.py script
subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"])

def myNetwork():

    net = Mininet(topo=None,
                  build=False,
                  ipBase='10.0.0.0/24')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info('*** Add routers\n')
    r5 = net.addHost('r5', cls=Node, ip='10.0.1.2/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r3 = net.addHost('r3', cls=Node, ip='10.0.0.254/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.254')
    h3 = net.addHost('h3', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.2')
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.3/24', defaultRoute='via 10.0.1.2')

    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    
    # Link between switches and routers
    net.addLink(s1, r3)
    net.addLink(s2, r5)

    # Link between routers with IP configuration
    net.addLink(r3, r4, intfName1='r3-eth1', params1={'ip': '192.168.1.1/30'}, intfName2='r4-eth0', params2={'ip': '192.168.1.2/30'})
    net.addLink(r4, r5, intfName1='r4-eth1', params1={'ip': '192.168.2.1/30'}, intfName2='r5-eth1', params2={'ip': '192.168.2.2/30'})

    info('*** Starting network\n')
    net.build()
    
    # Add static routes for routers
    r3.cmd('ip route add 10.0.1.0/24 via 192.168.1.2 dev r3-eth1')   # Route to subnet behind r5 via r4
    r3.cmd('ip route add 192.168.2.0/30 via 192.168.1.2 dev r3-eth1') # Route to the link between r4 and r5
    
    r4.cmd('ip route add 10.0.0.0/24 via 192.168.1.1 dev r4-eth0')    # Route to subnet behind r3
    r4.cmd('ip route add 10.0.1.0/24 via 192.168.2.2 dev r4-eth1')    # Route to subnet behind r5
    
    r5.cmd('ip route add 10.0.0.0/24 via 192.168.2.1 dev r5-eth1')    # Route to subnet behind r3 via r4
    r5.cmd('ip route add 192.168.1.0/30 via 192.168.2.1 dev r5-eth1') # Route to the link between r3 and r4

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info('*** Post configure switches and hosts\n')

    # Run the TLS-enabled chat server on h4
    makeTerm(h4, title='Chat Server', term='xterm', cmd='python3 tpa4_chat_server.py --tls; bash')
    
    # Run the chat clients on h1, h2, and h3
    makeTerm(h1, title='Chat Client 1', term='xterm', cmd='python3 tpa4_chat_client.py; bash')
    makeTerm(h2, title='Chat Client 2', term='xterm', cmd='python3 tpa4_chat_client.py; bash')
    makeTerm(h3, title='Chat Client 3', term='xterm', cmd='python3 tpa4_chat_client.py; bash')

    # Open Xterms for all hosts and routers for testing purposes
    CLI(net)
    
    # Stop all Xterms
    net.stopXterms()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()