import zmq

class ZeroMQTransport:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind(address)

    def send(self, message):
        """Отправляет сообщение в ZeroMQ"""
        self.socket.send_json(message)
