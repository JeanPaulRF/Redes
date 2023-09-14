from simulador.eventos import *
from modelos.frame import Frame
from capas.physicallayer import PhysicalLayer

class LinkProtocol:
    def __init__(self):
        self.sequence_number = 0
        self.timeout_duration = 5  # Duración del temporizador en segundos
        self.timeout_event = None  # Evento de timeout
        self.packet = None  # Variable para almacenar el último paquete enviado
        self.physical_layer = PhysicalLayer(0.1)  # Asigna la capa física
    
    def send(self, packet):
        print(f"Enviando paquete: {packet}")
        # Envía el paquete a través del canal de comunicación
        frame = Frame("data", self.sequence_number, 0, packet)
        # Simular la transmisión del frame a través de la capa física
        self.physical_layer.send_frame(frame)
        self.packet = packet  # Guarda el último paquete enviado
        # Configura un temporizador (timeout) para esperar la confirmación
        self.timeout_event = TimeoutEvent(self.timeout_duration)
        self.schedule_event(self.timeout_event, self.timeout_duration)
    
    def receive(self, frame):
        print(f"Recibiendo frame: {frame}")
        if frame.frame_type == "ack" and frame.ack_number == self.sequence_number:
            # Se recibió un ACK válido, se confirma la recepción
            self.cancel_event(self.timeout_event)  # Cancela el temporizador
            self.sequence_number += 1  # Incrementa el número de secuencia
        elif frame.frame_type == "data":
            # Se recibió un frame de datos, se procesa y envía un ACK
            packet = frame.packet_data
            # Procesa el paquete
            # Envía un ACK
            ack_frame = Frame("ack", frame.sequence_number, 0, None)
            # Simular el envío del ACK a través de la capa física
            self.physical_layer.send_frame(ack_frame)
    
    def handle_timeout(self):
        if self.timeout_event and self.timeout_event.is_expired():
            print("Timeout expirado. Retransmitiendo...")
            # Se ha agotado el temporizador, se reenvía el paquete
            self.cancel_event(self.timeout_event)  # Cancela el temporizador
            # Reenvía el último paquete
            # Simular la retransmisión del paquete a través de la capa física
            frame = Frame("data", self.sequence_number - 1, 0, self.packet)
            self.physical_layer.send_frame(frame)
            # Configura un nuevo temporizador
            self.timeout_event = TimeoutEvent(self.timeout_duration)
            self.schedule_event(self.timeout_event, self.timeout_duration)
    
    def schedule_event(self, event, duration):
        # Lógica para programar eventos (timeout) en el simulador
        pass
    
    def cancel_event(self, event):
        # Lógica para cancelar eventos programados en el simulador
        pass
