from protocolos.linkprotocol import LinkProtocol
from modelos.networklayer import NetworkLayer
from capas.physicallayer import PhysicalLayer
from simulador.simulator import Simulator

if __name__ == "__main__":
    # Crea instancias de tus componentes
    link_protocol = LinkProtocol()
    network_layer = NetworkLayer()
    physical_layer = PhysicalLayer(error_rate=0.1)
    
    # Inicializa el simulador con los componentes
    simulator = Simulator(link_protocol, network_layer, physical_layer)
    
    # Iniciar la simulación
    simulator.run_simulation()
