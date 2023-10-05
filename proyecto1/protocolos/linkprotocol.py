from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue

class LinkProtocol:
    def __init__(self, client):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 5 #Duración del temporizador en segundos
        self.timeout_event = None #Evento de timeout
        self.packet = None #Variable para almacenar el último paquete enviado
        self.physical_layer = None #Asigna la capa física
        self.events = Queue() #Cola de eventos

    def set_physical_layer(self, physical_layer):
        self.physical_layer = physical_layer

    def print_events(self):
        for event in self.events.queue:
            if isinstance(event, FrameArrivalEvent):
                print("Evento: FrameArrivalEvent Packet: " + event.frame.packet_data)
            elif isinstance(event, TimeoutEvent):
                print("Evento: TimeoutEvent")
            elif isinstance(event, AckTimeoutEvent):
                print("Evento: AckTimeoutEvent")
            elif isinstance(event, NetworkLayerReadyEvent):
                print("Evento: NetworkLayerReadyEvent Packet: " + event.packet)
            elif isinstance(event, ChecksumErrorEvent):
                print("Evento: ChecksumErrorEvent Packet: " + event.frame.packet_data)

    
    def send(self, packet):
        if self.client == "A" or self.client == "B":
            print(f"Enviando paquete: {packet}")
            #Envía el paquete a través del canal de comunicación
            frame = Frame("data", self.sequence_number, 0, packet)
            #Simular la transmisión del frame a través de la capa física
            print(f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            self.physical_layer.send_frame(frame)
            self.packet = packet
            #Configura un temporizador (timeout) para esperar la confirmación
            timeout_event = TimeoutEvent(self.timeout_duration)
            #Agregar el evento de timeout a la cola de eventos del protocolo de enlace
            self.schedule_event(timeout_event)

    def receive(self, frame):
        print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
        if frame.frame_type == "ack" and frame.ack_number == self.sequence_number:
            self.cancel_event()#Quita el evento de timeout de la cola de eventos
            #Se recibió un ACK válido, se confirma la recepción
            frame2 = Frame("data", self.sequence_number - 1, 0, self.packet)
            return frame2 #Simular el envío del ACK a través de la capa física
        elif frame.frame_type == "data":
            packet = frame.packet_data #Se recibió un frame de datos, se procesa y envía un ACK
            #Se crea un evento FrameArrivalEvent para señalar la llegada del paquete
            frame_arrival_event = FrameArrivalEvent(frame)
            #Se agrega el evento a la cola de eventos del protocolo de enlace
            self.schedule_event(frame_arrival_event)
            ack_frame = Frame("ack", frame.sequence_number, 0, packet)#Procesamos el paquete y enviamos un ack
            return ack_frame #Simulamos el envío del ACK a través de la capa física

    def handle_timeout(self):
        print("Timeout expirado. Retransmitiendo...")
        frame = Frame("data", self.sequence_number - 1, 0, self.packet)#Se ha agotado el temporizador, se reenvía el paquete
        self.physical_layer.send_frame(frame)#Simulamos la retransmisión del paquete a través de la capa física
        timeout_event = TimeoutEvent(self.timeout_duration)#Configura un nuevo temporizador
        self.schedule_event(timeout_event)#Agregar el evento de timeout a la cola de eventos del protocolo de enlace

    def schedule_event(self, event):
        self.events.put(event)

    def cancel_event(self):
        try:
            event = self.events.get()#Extrae el evento de la cola si está disponible
        except Queue.Empty:
            pass  #La cola está vacía, no hay eventos para cancelar

