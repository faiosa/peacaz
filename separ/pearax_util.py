import time

from PyQt5.QtCore import QTimer
from pearax import HEART_BEAT_INDEX
from pearax.client import PearaxClient
from pearax.mail import STANDARD_TTL


def method_inspect(client, method_name):
    method = getattr(client, method_name, None)
    if method is None:
        return False
    else:
        return callable(method)

def _inspect_client(client):
    assert method_inspect(client, "on_serial_disconnect")
    assert method_inspect(client, "on_serial_connect")

class SerialMonitor(PearaxClient):
    def __init__(self, mail_agent, listeners):
        super().__init__(mail_agent)
        self.connected = False
        self.disconnected_count = 0
        self.disconnected_limit = 7
        self.rate_ms = 25
        self.is_running = False
        for waiter in listeners:
            _inspect_client(waiter)
        self.listeners = listeners

    def stop_monitor(self):
        self.is_running = False

    def start_monitor(self):
        self.is_running = True
        self.__monitor()

    def __monitor(self):
        if not self.is_running:
            return
        cur_time = time.time()
        connected = False
        while True:
            data = self.receive(cur_time)
            if data is None:
                break
            else:
                connected = True
        if connected:
            if not self.connected:
                self.connected = True
                for listener in self.listeners:
                    listener.on_serial_connect()
            self.disconnected_count = 0
        elif self.connected:
            if self.disconnected_count < self.disconnected_limit:
                self.disconnected_count += 1
            else:
                self.connected = False
                for listener in self.listeners:
                    listener.on_serial_disconnect()

        self.send(str(cur_time).encode("utf-8"), cur_time, STANDARD_TTL)
        QTimer.singleShot(
            self.rate_ms,
            lambda: self.__monitor()
        )
