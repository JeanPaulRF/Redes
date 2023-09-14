class NetworkLayer:
    def __init__(self):
        self.packets = []
    
    def get_packet(self):
        if self.packets:
            return self.packets.pop(0)
        return None
    
    def send_packet(self, packet):
        self.packets.append(packet)