import threading
import requests
import queue
from loguru import logger




class tLineNotify(threading.Thread):

    def __init__(self, channel, name=None):
        threading.Thread.__init__(self)
        self.channel = channel
        self.queue = queue.Queue()
        self.start()

    def send(self, message):
        self.queue.put(message)

    def run(self):
        while True:
            try:
                message = self.queue.get(timeout=1)
            except queue.Empty:
                pass
            else:
                if message is None:
                    break
                try:
                    response = requests.post(f'https://ntfy.sh/{self.channel}', data=message)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f'Error sending message to ntfy.sh: {message}')
                    logger.error(e)

    def stop(self):
        self.queue.put(None)


if __name__ == '__main__':

    tline = tLineNotify(channel='putdaily')
    tline.send('測試')
    tline.stop()
