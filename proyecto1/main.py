import time
from protocolos.linkprotocol import LinkProtocol
from modelos.networklayer import NetworkLayer
from capas.physicallayer import PhysicalLayer
from simulador.simulator import Simulator
from modelos.packet import Packet

if __name__ == "__main__":
    # Crea instancias de tus componentes
    link_protocol_A = LinkProtocol()
    network_layer_A = NetworkLayer()
    physical_layer_A = PhysicalLayer(error_rate=0.1)

    link_protocol_B = LinkProtocol()
    network_layer_B = NetworkLayer()
    physical_layer_B = PhysicalLayer(error_rate=0.1)
    
    # Inicializa el simulador con los componentes para A y B
    simulator_A = Simulator(link_protocol_A, network_layer_A, physical_layer_A)
    simulator_B = Simulator(link_protocol_B, network_layer_B, physical_layer_B)
    
    # Iniciar la simulación para A y B en hilos separados
    import threading
    thread_A = threading.Thread(target=simulator_A.run_simulation)
    thread_B = threading.Thread(target=simulator_B.run_simulation)
    thread_A.start()
    thread_B.start()
    
    # Generar paquetes de prueba en la capa de red de A y enviarlos a B
    for i in range(10):
        packet_data = f"Datos del paquete {i}"
        packet = Packet(packet_data)
        network_layer_A.send_packet(packet)
        print(f"Enviado desde A: {packet_data}")
        physical_layer_A.receive_frame()
        time.sleep(1)
