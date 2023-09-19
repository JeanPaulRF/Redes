from simulador.eventos import *
from modelos.frame import Frame

class LinkProtocol:
    def __init__(self, client):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 2  # Duración del temporizador en segundos
        self.timeout_event = None  # Evento de timeout
        self.packet = None  # Variable para almacenar el último paquete enviado
        self.physical_layer = None  # Asigna la capa física

    def set_physical_layer(self, physical_layer):
        self.physical_layer = physical_layer
    
    def send(self, packet):
        if self.client == "A" or self.client == "B":
            print(f"Enviando paquete: {packet}")
            # Envía el paquete a través del canal de comunicación
            frame = Frame("data", self.sequence_number, 0, packet)
            # Simular la transmisión del frame a través de la capa física
            print(f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            self.physical_layer.send_frame(frame)
            self.packet = packet
            # Configura un temporizador (timeout) para esperar la confirmación
            self.timeout_event = TimeoutEvent(self.timeout_duration)
            # self.schedule_event(self.timeout_event, self.timeout_duration)  # Elimina esta línea
    
    def receive(self, frame):
        print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
        if frame.frame_type == "ack" and frame.ack_number == self.sequence_number:
            # Se recibió un ACK válido, se confirma la recepción
            #self.cancel_event(self.timeout_event)  # Elimina esta línea
            frame2 = Frame("data", self.sequence_number - 1, 0, self.packet)
            frame2 = Frame("data", self.sequence_number - 1, 0, self.packet)
            self.physical_layer.send_frame(frame2)
            #self.sequence_number += 1  # Incrementa el número de secuencia
        elif frame.frame_type == "data":
            # Se recibió un frame de datos, se procesa y envía un ACK
            packet = frame.packet_data
            # Procesa el paquete
            # Envía un ACK
            ack_frame = Frame("ack", frame.sequence_number, 0, packet)
            # Simular el envío del ACK a través de la capa física
            return ack_frame
    
    def handle_timeout(self):
        if self.timeout_event and self.timeout_event.is_expired():
            print("Timeout expirado. Retransmitiendo...")
            # Se ha agotado el temporizador, se reenvía el paquete
            self.cancel_event(self.timeout_event)  # Elimina esta línea
            # Reenvía el último paquete
            # Simular la retransmisión del paquete a través de la capa física
            frame = Frame("data", self.sequence_number - 1, 0, self.packet)
            self.physical_layer.send_frame(frame)
            # Configura un nuevo temporizador
            self.timeout_event = TimeoutEvent(self.timeout_duration)
            # self.schedule_event(self.timeout_event, self.timeout_duration)  # Elimina esta línea
