from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue

class StopAndWait:
    def __init__(self, client):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 5  # Duración del temporizador en segundos
        self.timeout_event = None  # Evento de timeout
        self.packet = None  # Variable para almacenar el último paquete enviado
        self.physical_layer = None  # Asigna la capa física
        self.events = Queue()  # Cola de eventos

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
            
            frame = Frame("data", self.sequence_number, 0, packet)# Crea un frame de datos con el número de secuencia actual
            
            print(f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")# Imprime información sobre el frame de datos que se envía
            
           
            self.physical_layer.send_frame(frame)#Envía el frame de datos a través de la capa física
            
            timeout_event = TimeoutEvent(self.timeout_duration) #Configura un temporizador (timeout) para esperar la confirmación
            self.schedule_event(timeout_event)# Agrega el evento de timeout a la cola de eventos del protocolo de enlace
            self.waiting_for_ack = True#Marca que estamos esperando un ACK

    def receive(self, frame):
        if self.client == "B":
            if frame.frame_type == "data" and frame.sequence_number == self.sequence_number:
                #Imprime información sobre el frame de datos recibido
                print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
                
                packet = frame.packet_data#Extrae los datos del paquete contenido en el frame de datos
                
                ack_frame = Frame("ack", frame.sequence_number, 0, packet)#Crea un frame de ACK con el mismo número de secuencia y envía el ACK
                #Imprime información sobre el ACK que se envía
                print(f"Enviando ACK: Tipo: {ack_frame.frame_type} - Número de secuencia: {ack_frame.sequence_number} - Número de ACK: {ack_frame.ack_number}")
                self.physical_layer.send_frame(ack_frame)
                
                self.sequence_number += 1#Incrementa el número de secuencia esperado para el siguiente paquete

                # Marca que ya no estamos esperando un ACK
                self.waiting_for_ack = False


    def handle_timeout(self):
        print("Timeout expirado. Retransmitiendo...")
        # Se ha agotado el temporizador, se reenvía el paquete
        frame = Frame("data", self.sequence_number - 1, 0, self.packet)
        # Simular la retransmisión del paquete a través de la capa física
        self.physical_layer.send_frame(frame)
        # Configura un nuevo temporizador
        timeout_event = TimeoutEvent(self.timeout_duration)
        # Agregar el evento de timeout a la cola de eventos del protocolo de enlace
        self.schedule_event(timeout_event)

    def schedule_event(self, event):
        self.events.put(event)

    def cancel_event(self):
        try:
            event = self.events.get()  # Extrae el evento de la cola si está disponible
        except Queue.Empty:
            pass  # La cola está vacía, no hay eventos para cancelar