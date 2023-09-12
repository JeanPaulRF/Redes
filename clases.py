import random
import time

class LinkProtocol:
    def __init__(self):
        self.sequence_number = 0
        self.ack_number = 0
    
    def send(self, packet):
        pass
    
    def receive(self):
        pass


class Packet:
    def __init__(self, content):
        self.content = content


class Frame:
    def __init__(self, frame_type, sequence_number, ack_number, packet_data):
        self.frame_type = frame_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.packet_data = packet_data


class NetworkLayer:
    def __init__(self):
        self.packets = []
    
    def get_packet(self):
        if self.packets:
            return self.packets.pop(0)
        return None
    
    def send_packet(self, packet):
        self.packets.append(packet)


class PhysicalLayer:
    def __init__(self, error_rate):
        self.frames = []
        self.error_rate = error_rate
    
    def get_frame(self):
        if self.frames:
            return self.frames.pop(0)
        return None
    
    def send_frame(self, frame):
        if random.random() > self.error_rate:
            self.frames.append(frame)


class Simulator:
    def __init__(self, protocol, network_layer, physical_layer):
        self.protocol = protocol
        self.network_layer = network_layer
        self.physical_layer = physical_layer
    
    def run_simulation(self):
        while True:
            # Obtener un paquete de la capa de red
            packet = self.network_layer.get_packet()
            if packet:
                # Enviar el paquete al protocolo de enlace
                self.protocol.send(packet)

            # Obtener un frame de la capa física
            frame = self.physical_layer.get_frame()
            if frame:
                # Enviar el frame al protocolo de enlace
                self.protocol.receive(frame)
            
            # Simular un temporizador (timeout) en el protocolo
            self.protocol.handle_timeout()
            
            # Simular una espera antes de la próxima iteración
            time.sleep(0.1)