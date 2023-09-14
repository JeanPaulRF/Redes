class Frame:
    def __init__(self, frame_type, sequence_number, ack_number, packet_data):
        self.frame_type = frame_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.packet_data = packet_data