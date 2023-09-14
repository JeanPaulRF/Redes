import time

class Event:
    def __init__(self, event_type):
        self.event_type = event_type

class FrameArrivalEvent(Event):
    def __init__(self, frame):
        super().__init__("frame_arrival")
        self.frame = frame

class ChecksumErrorEvent(Event):
    def __init__(self, frame):
        super().__init__("cksum_err")
        self.frame = frame

class TimeoutEvent:
    def __init__(self, duration):
        self.duration = duration  # Duración en segundos
        self.start_time = time.time()  # Tiempo de inicio
    
    def is_expired(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        return elapsed_time >= self.duration

class AckTimeoutEvent(Event):
    def __init__(self):
        super().__init__("ack_timeout")

class NetworkLayerReadyEvent(Event):
    def __init__(self, packet):
        super().__init__("network_layer_ready")
        self.packet = packet
