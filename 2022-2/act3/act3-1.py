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
    h1 = net.addHost('h1', ip='10.10.1.1')
    h2 = net.addHost('h2', ip='10.10.1.2')
    h3 = net.addHost('h3', ip='10.10.1.3')
    h4 = net.addHost('h4', ip='10.10.1.4')

    # Se agregan los routers, que a su vez también son hosts, no es una clase especial.
    info( '*** Adding routers\n' )
    # r1 = net.addHost( 'r1', ip='')
 
    # Se agregan switches.
    info( '*** Adding switch\n' )
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Se crea enlaces entre dispositivos.
    info( '*** Creating links\n' )
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, s3)
    net.addLink(s3, s2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)

    # Para conexión directa entre routers, se le puede asignar IP en ambos lados en su enlace.
    # info( '*** Connecting between routers \n' )
    # net.addLink(r1, r2, intfName="r1-r2", params1={'ip': ''}, params2={'ip': ''})

    # Iniciando red
    info( '*** Starting network\n')
    net.start()

    # # Rutas manuales en router.
    # r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    # r1.cmd("ip route add X.X.X.X/24 via X.X.X.X")
    # r1.cmd("ip route add X.X.X.X/24 via X.X.X.X")

    # Rutas manuales en host.
    h1.cmd("ip route add default via X.X.X.X")

    # Para poder mostrar la interfaz de comandos
    info( '*** Running CLI\n' )
    CLI( net )

    # Detener red al salir
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    actividad()
