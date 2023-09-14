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

class TimeoutEvent(Event):
    def __init__(self):
        super().__init__("timeout")

class AckTimeoutEvent(Event):
    def __init__(self):
        super().__init__("ack_timeout")

class NetworkLayerReadyEvent(Event):
    def __init__(self, packet):
        super().__init__("network_layer_ready")
        self.packet = packet
