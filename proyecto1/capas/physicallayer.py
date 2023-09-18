import random

class PhysicalLayer:
    def __init__(self, error_rate):
        self.frames = []
        self.error_rate = error_rate
        self.receptor = None

    def set_receptor(self, receptor):
        self.receptor = receptor
    
    def get_frame(self):
        if self.frames:
            return self.frames.pop(0)
        return None
    
    def receive_frame(self, frame):
        if random.random() > self.error_rate:
            self.frames.append(frame)

    def send_frame(self, frame):
        self.receptor.receive_frame(frame)