from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, \
    ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue


class SelectiveRepeatProtocol:
    def __init__(self, client, packageLimit):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 5  # Duración del temporizador en segundos
        self.timeout_event = None  # Evento de timeout
        self.packet = None  # Variable para almacenar el último paquete enviado
        self.physical_layer = None  # Asigna la capa física
        self.events = Queue()  # Cola de eventos
        # No hay paquetes ilimitados
        self.packageLimit = packageLimit
        self.amountPackages = 0

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
        # Se envían los paquetes hasta que se llegue al límite
        while self.amountPackages < self.packageLimit:
            if self.client == "A" or self.client == "B":
                print(f"Enviando paquete: {packet}")
                # Envía el paquete a través del canal de comunicación
                frame = Frame("data", self.sequence_number, 0, packet)
                # Simular la transmisión del frame a través de la capa física
                print(
                    f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
                self.physical_layer.send_frame(frame)
                self.packet = packet
                # Configura un temporizador (timeout) para esperar la confirmación
                timeout_event = TimeoutEvent(self.timeout_duration)
                # Agregar el evento de timeout a la cola de eventos del protocolo de enlace
                self.schedule_event(timeout_event)
                # Se incrementa el número de paquetes enviados
                self.amountPackages += 1

    def receive(self, frame):
        print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
        if frame.frame_type == "ack" and frame.ack_number == self.sequence_number:
            # Quita el evento de timeout de la cola de eventos
            self.cancel_event()
            # Se recibió un ACK válido, se confirma la recepción
            frame2 = Frame("data", self.sequence_number - 1, 0, self.packet)
            # Simular el envío del ACK a través de la capa física
            return frame2
        elif frame.frame_type == "data":
            # Se recibió un frame de datos, se procesa y envía un ACK
            packet = frame.packet_data

            # Crear un evento FrameArrivalEvent para señalar la llegada del paquete
            frame_arrival_event = FrameArrivalEvent(frame)
            # Agregar el evento a la cola de eventos del protocolo de enlace
            self.schedule_event(frame_arrival_event)
            # Procesa el paquete
            # Envía un ACK
            ack_frame = Frame("ack", frame.sequence_number, 0, packet)
            # Simular el envío del ACK a través de la capa física
            return ack_frame


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