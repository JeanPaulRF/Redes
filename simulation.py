from clases import *

if __name__ == "__main__":
    network_layer = NetworkLayer()
    physical_layer = PhysicalLayer(error_rate=0.1)
    protocol = LinkProtocol()
    simulator = Simulator(protocol, network_layer, physical_layer)
    
    # Iniciar la simulación en un hilo separado
    import threading
    simulation_thread = threading.Thread(target=simulator.run_simulation)
    simulation_thread.start()
    
    # Generar paquetes de prueba en la capa de red
    for i in range(10):
        packet = Packet(f"Datos del paquete {i}")
        network_layer.send_packet(packet)
        time.sleep(1)