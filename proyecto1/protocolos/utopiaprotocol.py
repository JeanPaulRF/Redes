from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue

class UtopiaProtocol:
    def __init__(self, client):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 5#duración del temporizador en segundos
        self.timeout_event = None #evento de timeout
        self.packet = None #variable para almacenar el último paquete enviado
        self.physical_layer = None #asigna la capa física
        self.events = Queue()#cola de eventos

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
        if self.client == "A":
            print(f"Enviando paquete: {packet}")
            #senvía el paquete a través del canal de comunicación
            frame = Frame("data", self.sequence_number, 0, packet)
            #simulamos la transmisión del frame a través de la capa física
            print(f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            self.physical_layer.send_frame(frame)
            self.packet = packet
            timeout_event = TimeoutEvent(self.timeout_duration) #se configura un temporizador (timeout) para esperar la confirmación
            #se agrega el evento de timeout a la cola de eventos del protocolo de enlace
            self.schedule_event(timeout_event)

    def receive(self, frame):
        print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
        if frame.frame_type == "ack" and frame.ack_number == self.sequence_number and self.client == "A":
        
            self.cancel_event()#quita el evento de timeout de la cola de eventos
            #se recibió un ACK válido, se confirma la recepción
            frame2 = Frame("data", self.sequence_number - 1, 0, self.packet)
            #simulamos el envío del ACK a través de la capa física
            return frame2
        elif frame.frame_type == "data" and self.client == "B":
            #se recibió un frame de datos, se procesa y envía un ACK
            packet = frame.packet_data
            #creamos un evento FrameArrivalEvent para señalar la llegada del paquete
            frame_arrival_event = FrameArrivalEvent(frame)
           
            self.schedule_event(frame_arrival_event) #se agrega el evento a la cola de eventos del protocolo de enlace
            #procesa el paquete y se envia el ack
            ack_frame = Frame("ack", frame.sequence_number, 0, packet)
            #soimulamos el envío del ACK a través de la capa física
            return ack_frame


    def handle_timeout(self):
        print("Timeout expirado. Retransmitiendo...")
        #se agotó el temporizador, se reenvía el paquete
        frame = Frame("data", self.sequence_number - 1, 0, self.packet)
        #simulamos la retransmisión del paquete a través de la capa física
        self.physical_layer.send_frame(frame)
       
        timeout_event = TimeoutEvent(self.timeout_duration) #config un nuevo temporizador
        self.schedule_event(timeout_event)#se agrega el evento de timeout a la cola de eventos del protocolo de enlace

    def schedule_event(self, event):
        self.events.put(event)

    def cancel_event(self):
        try:
            event = self.events.get()#extrae el evento de la cola si está disponible
        except Queue.Empty:
            pass#la cola está vacía, no hay eventos para cancelar