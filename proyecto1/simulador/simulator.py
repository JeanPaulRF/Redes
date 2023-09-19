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
            if not self.pause:
                # Enviar
                # Obtener un paquete de la capa de red
                packet = self.network_layer.send_packet(self.client)         

                if packet:
                    # Enviar el paquete al protocolo de enlace
                    self.link_protocol.send(packet)

                # Recibir
                # Obtener un frame de la capa física
                frame = self.physical_layer.get_frame()
                if frame:

                    # Recibir el frame en el protocolo de enlace
                    response_frame = self.link_protocol.receive(frame)

                    if response_frame:
                        # Enviar la respuesta a través de la capa física
                        self.physical_layer.send_frame(response_frame)

            # Simular una espera antes de la próxima iteración
            time.sleep(1)
