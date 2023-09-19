class NetworkLayer:
    def __init__(self):
        self.packets = []
        self.sents = 0
    
    def send_packet(self, client):
        self.sents += 1
        return "Mensaje {" + str(self.sents-1) + "} del cliente " + client
    
    def receive_packet(self, packet):
        #print(f"Recibiendo paquete: {packet}")
        self.packets.append(packet)