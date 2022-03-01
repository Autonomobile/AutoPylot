import logging
import socket
import threading


class Telemetry:
    def __init__(self, mem, host="0.0.0.0", port=8080):
        assert isinstance(mem, dict)
        self.mem = mem

        assert isinstance(host, str)
        assert isinstance(port, int)
        self.address = (host, port)

        self.__stop_thread = False
        self.__thread = None

    def start_thread(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

        if not self.__thread:
            self.__thread = threading.Thread(target=self.__run_threaded__)
            logging.info("Started thread to send telemetry.")
        else:
            logging.warning("Thread already running.")

    def stop_thread(self):
        if self.__thread and self.__thread.is_alive():
            self.__stop_thread = True
            self.__thread.join()
            logging.info("Stopped thread.")
        else:
            logging.warning("Thread is not running.")

    def __run_threaded__(self):
        while True:

            self.send("some packet")

            if self.__stop_thread:
                self.__stop_thread = False
                break

    def send(self, packet):
        return
