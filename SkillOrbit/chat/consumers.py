from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print("WebSocket Connected")
        self.accept()

    def disconnect(self, close_code):
        print("WebSocket Disconnected")

    def receive(self, text_data):
        print(text_data)