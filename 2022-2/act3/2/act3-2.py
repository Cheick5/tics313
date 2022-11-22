from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def actividad():
    net = Mininet( controller=Controller )

    # Se agrega controlador, no requiere configuración adicional.
    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    # Se agregan los hosts.
    info( '*** Adding hosts\n' )
    h1 = net.addHost('h1', ip='10.10.1.2/24')
    h2 = net.addHost('h2', ip='10.10.1.3/24')
    h3 = net.addHost('h3', ip='10.10.2.2/24')
    h4 = net.addHost('h4', ip='10.10.2.3/24')
    h5 = net.addHost('h5', ip='10.10.3.2/24')
    h6 = net.addHost('h6', ip='10.10.3.3/24')

    # Se agregan los routers, que a su vez también son hosts, no es una clase especial.
    info( '*** Adding routers\n' )
    r1 = net.addHost( 'r1', ip='10.10.1.1/24')
    r2 = net.addHost( 'r2', ip='10.10.2.1/24')
    r3 = net.addHost( 'r3', ip='10.10.3.1/24')
 
    # Se agregan switches.
    info( '*** Adding switch\n' )
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Se crea enlaces entre dispositivos.
    info( '*** Creating links\n' )
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    net.addLink(h5, s3)
    net.addLink(h6, s3)

    net.addLink(r1, s1)
    net.addLink(r2, s2)
    net.addLink(r3, s3)

    # Para conexión directa entre routers, se le puede asignar IP en ambos lados en su enlace.
    info( '*** Connecting between routers \n' )     
    net.addLink(r1, r3, intfName="r1-r3", params1={'ip': '172.16.1.1/24'}, params2={'ip': '172.16.1.2/24'})
    # Router 1-3 ip = 172.16.1.1
    # Router 3-1 ip = 172.16.1.2
    net.addLink(r2, r3, intfName="r2-r3", params1={'ip': '172.16.2.1/24'}, params2={'ip': '172.16.2.2/24'})
    # Router 2-3 ip = 172.16.2.1
    # Router 3-2 ip = 172.16.2.2

    # Iniciando red
    info( '*** Starting network\n')
    net.start()

    # Rutas manuales en router.
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r1.cmd("ip route add 10.10.3.0/24 via 172.16.1.2") #Añadimos S3 via router ip 3
    r1.cmd("ip route add 10.10.2.0/24 via 172.16.1.2") #Añadimos S2 via router ip 2

    r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("ip route add 10.10.3.0/24 via 172.16.2.2")
    r2.cmd("ip route add 10.10.1.0/24 via 172.16.2.2")
    # r2.cmd("ip route add 10.10.1.0/24 via 10.10.2.254")
    # r1.cmd("ip route add 10.10.3.0/24 via 10.10.1.254")
    

    r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("ip route add 10.10.1.0/24 via 172.16.1.1")
    r3.cmd("ip route add 10.10.2.0/24 via 172.16.2.1")
    # r3.cmd("ip route add 10.10.1.0/24 via 10.10.3.254")
    # r1.cmd("ip route add 10.10.2.0/24 via 10.10.1.254")


    # Rutas manuales en host.
    h1.cmd("ip route add default via 10.10.1.1")
    h2.cmd("ip route add default via 10.10.1.1")
    h3.cmd("ip route add default via 10.10.2.1")
    h4.cmd("ip route add default via 10.10.2.1")
    h5.cmd("ip route add default via 10.10.3.1")
    h6.cmd("ip route add default via 10.10.3.1")

    # Para poder mostrar la interfaz de comandos
    info( '*** Running CLI\n' )
    CLI( net )

    # Detener red al salir
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    actividad()