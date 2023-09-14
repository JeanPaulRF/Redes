import time

class Simulator:
    def __init__(self, link_protocol, network_layer, physical_layer):
        self.link_protocol = link_protocol
        self.network_layer = network_layer
        self.physical_layer = physical_layer
    
    def run_simulation(self):
        while True:
            # Obtener un paquete de la capa de red
            packet = self.network_layer.get_packet()
            if packet:
                # Enviar el paquete al protocolo de enlace
                self.link_protocol.send(packet)

            # Obtener un frame de la capa física
            frame = self.physical_layer.get_frame()
            if frame:
                # Enviar el frame al protocolo de enlace
                self.link_protocol.receive(frame)
            
            # Simular un temporizador (timeout) en el protocolo de enlace
            self.link_protocol.handle_timeout()
            
            # Simular una espera antes de la próxima iteración
            time.sleep(0.1)
