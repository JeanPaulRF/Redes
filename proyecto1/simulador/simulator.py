import time

class Simulator:
    def __init__(self, link_protocol, network_layer, physical_layer):
        self.link_protocol = link_protocol
        self.network_layer = network_layer
        self.physical_layer = physical_layer
        self.running = True
        self.pause = False
        self.client = self.link_protocol.client
    
    def run_simulation(self):
        while self.running:
            if self.pause:
                time.sleep(1)
                continue

            # Enviar
            # Obtener un paquete de la capa de red
            packet = self.network_layer.send_packet(self.client)         

            # Enviar el paquete al protocolo de enlace
            frame = self.link_protocol.send(packet)

            # Enviar el frame a la capa fisica
            self.physical_layer.send_frame(frame)

            # Recibir
            # Obtener un frame de la capa física
            frame = self.physical_layer.get_frame()
            if frame:
                # Recibir el frame en el protocolo de enlace
                packet = self.link_protocol.receive(frame)

                if packet:
                    # Recibir el packet en la capa de red
                    self.network_layer.receive_packet(packet)
            
            # Simular una espera antes de la próxima iteración
            time.sleep(0.5)
