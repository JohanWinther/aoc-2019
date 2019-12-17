from websocket_server import WebsocketServer
from threading import Thread
from time import sleep
import webbrowser, os

class Screen():
    def __init__(self, PORT=5300):
        self.server = WebsocketServer(PORT)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.arcade = None

    def new_client(self, client, server):
        print("New client connected and was given id %d" % client['id'])

    def client_left(self, client, server):
        os._exit(1)

    # Called when a client sends a message
    def message_received(self, client, server, message):
        direction = int(message)
        if self.arcade and direction <= 1 and direction >= -1:
            self.arcade.brain.set_input(direction)

    def send_message(self, message):
        self.server.send_message_to_all(message)

    def run(self):
        url = os.path.abspath(__file__).replace('.py', '.html').replace('/mnt/c/', 'file:///C:/')
        webbrowser.open(url, new=2)
        #song_uri = "spotify:track:43DnalVz4tL1pR1GWCpfCj"
        #webbrowser.open(song_uri, new=2)
        Thread(target=self.server.run_forever).start()
