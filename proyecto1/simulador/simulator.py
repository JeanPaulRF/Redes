import time
from simulador.eventos import NetworkLayerReadyEvent, ChecksumErrorEvent

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
                #enviar y btener un paquete de la capa de red
                packet = self.network_layer.send_packet(self.client)  
                new_event = NetworkLayerReadyEvent(packet)
                self.link_protocol.schedule_event(new_event)       

                if packet:
                    #enviar el paquete al protocolo de enlace
                    self.link_protocol.send(packet)

                frame = self.physical_layer.get_frame() #recibir y obtener un frame de la capa física
                if frame:
                    #se recibe el frame en el protocolo de enlace
                    response_frame = self.link_protocol.receive(frame)
                    if response_frame:
                        #se envia la respuesta a través de la capa física
                        result = self.physical_layer.send_frame(response_frame)
                        
                        if not result:#si el frame no se envió correctamente, se genera un evento de errort
                            new_event = ChecksumErrorEvent(response_frame)
                            self.link_protocol.schedule_event(new_event)

            #se simula una espera antes de la próxima iteración
            time.sleep(1)
