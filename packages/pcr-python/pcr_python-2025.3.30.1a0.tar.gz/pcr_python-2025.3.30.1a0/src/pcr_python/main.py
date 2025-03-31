import socket
import json


class Checkpoint:
    _instance = None
    socketPath = "/tmp/pcr"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.called = False
            self.initialized = True

    def create_checkpoint(self):
        if self.called:
            raise Exception("Checkpoint can only be created once.")

        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.connect(self.socketPath)

        message = json.dumps({"cmd": "create_checkpoint"})
        server_socket.sendall(message.encode("utf-8"))

        server_socket.close()

        print("Creating checkpoint...", flush=True)

        self.called = True
