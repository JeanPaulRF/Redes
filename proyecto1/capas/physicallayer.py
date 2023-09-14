import random

class PhysicalLayer:
    def __init__(self, error_rate):
        self.frames = []
        self.error_rate = error_rate
    
    def get_frame(self):
        if self.frames:
            return self.frames.pop(0)
        return None
    
    def send_frame(self, frame):
        if random.random() > self.error_rate:
            self.frames.append(frame)