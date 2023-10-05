from simulador.eventos import FrameArrivalEvent, TimeoutEvent, AckTimeoutEvent, NetworkLayerReadyEvent, \
    ChecksumErrorEvent
from modelos.frame import Frame
from queue import Queue


class SelectiveRepeatProtocol:
    def __init__(self, client, packageLimit, senderWindowSize, receiverWindowSize):
        self.client = client
        self.sequence_number = 0
        self.timeout_duration = 5#Duración del temporizador en segundos
        self.timeout_event = None#Evento de timeout
        self.packet = None#Variable para almacenar el último paquete enviado
        self.physical_layer = None #Asigna la capa física
        self.events = Queue()#Cola de eventos
        # No hay paquetes ilimitados
        self.packageLimit = int(packageLimit)
        self.amountPackages = 0
        #la ventana de tamaño N para el emisor
        self.senderWindowSize = int(senderWindowSize)
        self.amountSenderPackages = 0
        #ventana de tamaño N para el receptor
        self.receiverWindowSize = int(receiverWindowSize)
        self.amountReceiverPackages = 0

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
        #enviamos los paquetes hasta que se llegue al límite
        if self.amountPackages < self.packageLimit:
            if self.client == "A" or self.client == "B":
                if self.amountSenderPackages < self.senderWindowSize:
                    #luego actualiza la cantidad de paquetes enviados
                    self.amountSenderPackages += 1
                    print(f"Enviando paquete: {packet}")
                    
                    frame = Frame("data", self.sequence_number, 0, packet)#se envia el paquete a través del canal de comunicación
                    #empezamos a simlar la transmisión del frame a través de la capa física
                    print(
                        f"Enviando frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
                    self.physical_layer.send_frame(frame)
                    self.packet = packet


                    #despues se congigura un temporizador (timeout) para esperar la confirmación
                    timeout_event = TimeoutEvent(self.timeout_duration)
                    
                    self.schedule_event(timeout_event)#se agrega el evento de timeout a la cola de eventos del protocolo de enlace
                    #indica que el receptor puede recibir
                    self.amountReceiverPackages -= 1
                    #he incrementamos el número de paquetes enviados
                    self.amountPackages += 1

                else:
                    print("No se puede enviar el paquete, se ha llegado al límite de la ventana de envio. Espete un momento")

        else:
            print("No se puede enviar el paquete, se ha llegado al límite de paquetes enviados")

    def receive(self, frame):
        if self.amountReceiverPackages < self.receiverWindowSize:
            self.amountReceiverPackages += 1
            print(f"Recibiendo frame: Tipo: {frame.frame_type} - Número de secuencia: {frame.sequence_number} - Número de ACK: {frame.ack_number} - Datos: {frame.packet_data}")
            if frame.frame_type == "ack" and frame.ack_number == self.sequence_number:
                
                self.cancel_event()#quita el evento de timeout de la cola de eventos
                frame2 = Frame("data", self.sequence_number - 1, 0, self.packet) #recibió un ACK válido, se confirma la recepción
                #le indica al emisor que se recibio el paquete
                self.amountSenderPackages -= 1

                #se simula el envío del ACK a través de la capa física
                return frame2
            elif frame.frame_type == "data":
                #si see recibió un frame de datos, se procesa y envía un ACK
                packet = frame.packet_data

                #se cea un evento FrameArrivalEvent para señalar la llegada del paquete
                frame_arrival_event = FrameArrivalEvent(frame)
                
                self.schedule_event(frame_arrival_event)#Agregamos el evento a la cola de eventos del protocolo de enlace
                #procesamos el paquete y enviamos el ack
                ack_frame = Frame("ack", frame.sequence_number, 0, packet)
                #le indica al emisor que se recibio el paquete
                self.amountSenderPackages -= 1
                #simulamos el envío del ACK a través de la capa física
                return ack_frame

        else:
            print("No se puede recibir el paquete, se ha llegado al límite de la ventana de recepción. Espere un momento")
            return None


    def handle_timeout(self):
        print("Timeout expirado. Retransmitiendo...")
        #se agotóel temporizador, se reenvía el paquete
        frame = Frame("data", self.sequence_number - 1, 0, self.packet)
       
        self.physical_layer.send_frame(frame) #simulamos la retransmisión del paquete a través de la capa física
        #se configura un nuevo temporizador
        timeout_event = TimeoutEvent(self.timeout_duration)
        
        self.schedule_event(timeout_event)#agregamos el evento de timeout a la cola de eventos del protocolo de enlace

    def schedule_event(self, event):
        self.events.put(event)

    def cancel_event(self):
        try:
            event = self.events.get()#extrae el evento de la cola si está disponible
        except Queue.Empty:
            pass #la cola está vacía, no hay eventos para cancelar