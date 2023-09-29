from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue

class UtopiaProtocol:
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
            # Verifica si el cliente es "A". Solo A puede enviar paquetes en el protocolo Utopía.
            
            print(f"Enviando paquete: {packet}")
            # Imprime un mensaje para mostrar que se está enviando un paquete.
            
            frame = Frame("data", self.sequence_number, 0, packet)
            # Crea un objeto Frame con los siguientes atributos:
            # - Tipo: "data" (indicando que es un frame de datos).
            # - Número de secuencia: self.sequence_number (número de secuencia actual).
            # - Número de ACK: 0 (ya que no se espera un ACK en Utopía).
            # - Datos: packet (el paquete que se pasa como argumento).
            
            print(f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            #Imprime información sobre el frame que se está enviando.
            
            self.physical_layer.send_frame(frame)
            #Llama al método send_frame de la capa física para simular el envío del frame.
            
            self.sequence_number += 1
            #Aumenta el número de secuencia en 1 para el siguiente paquete que se envíe.


    def receive(self, frame):
        if self.client == "B" and frame.frame_type == "data":
            # Verifica si el cliente es "B" y si el frame recibido es de tipo "data".
            # Solo B puede recibir frames de datos en Utopía.

            print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            #Imprime información sobre el frame que se ha recibido.

            packet = frame.packet_data
            #Extrae los datos del paquete contenido en el frame.

            ack_frame = Frame("ack", frame.sequence_number, 0, packet)
            # Crea un objeto Frame de tipo "ack" con los siguientes atributos:
            # - Tipo: "ack" (indicando que es un frame de confirmación).
            # - Número de secuencia: frame.sequence_number (el número de secuencia del frame de datos recibido).
            # - Número de ACK: 0 (ya que no se espera un ACK en Utopía).
            # - Datos: packet (los datos del paquete recibido).

            print(f"Enviando ACK: Tipo: {ack_frame.frame_type} - Número de secuencia: {ack_frame.sequence_number} - Número de ACK: {ack_frame.ack_number} - Datos: {ack_frame.packet_data}")
            #Imprime información sobre el ACK que se está enviando.

            self.physical_layer.send_frame(ack_frame)
            #Llama al método send_frame de la capa física para simular el envío del ACK.


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