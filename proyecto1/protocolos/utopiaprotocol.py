from simulador.eventos import *
from modelos.frame import Frame
from capas.physicallayer import PhysicalLayer

class UtopiaProtocol:
    def __init__(self):
        self.sequence_number = 0
        self.timeout_duration = 5  # Duración del temporizador en segundos
        self.timeout_event = None  # Evento de timeout
        self.packet = None  # Variable para almacenar el último paquete enviado
        self.physical_layer = None

    def set_physical_layer(self, physical_layer):
        self.physical_layer = physical_layer

    def send(self, packet):
        pass

    def receive(self, frame):
        pass

    