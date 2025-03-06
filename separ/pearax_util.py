from PyQt5.QtCore import QTimer
from pearax.core import Pearax


def method_inspect(client, method_name):
    method = getattr(client, method_name, None)
    if method is None:
        return False
    else:
        return callable(method)

def _inspect_client(client):
    assert method_inspect(client, "on_serial_disconnect")
    assert method_inspect(client, "on_serial_connect")

class SerialMonitor:
    def __init__(self, pearax: Pearax):
        self.pearax = pearax
        self.waiters = {}
        self.serial_alive = True

    def check_serial_connect(self, client):
        _inspect_client(client)
        if self.serial_alive:
            assert len(self.waiters) == 0
            if self.pearax.is_serial_alive():
                return True
            else:
                client.on_serial_disconnect()
                self.waiters[id(client)] = client
                self.serial_alive = False
                self.__check_connection_regain()
                return self.serial_alive
        else:
            client_id = id(client)
            if not client_id in self.waiters:
                client.on_serial_disconnect()
                self.waiters[client_id] = client
            return False

    def __check_connection_regain(self):
        assert self.serial_alive is False
        if self.pearax.is_serial_alive():
            self.serial_alive = True
            old_waiters = self.waiters
            self.waiters = {}
            for key in old_waiters:
                old_waiters[key].on_serial_connect()
        else:
            QTimer.singleShot(
                10,
                lambda: self.__check_connection_regain()
            )

