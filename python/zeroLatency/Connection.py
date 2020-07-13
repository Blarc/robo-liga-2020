import sys
from io import BytesIO
from time import time

import pycurl as pycurl
import ujson as ujson


class Connection:
    """
    Objekt za vzpostavljanje povezave s strežnikom.
    """

    def __init__(self, url_connection: str):
        """
        Inicializacija nove povezave.

        Argumenti:
        url_connection: pot do datoteke na strežniku (URL)
        """
        self._url = url_connection
        self._buffer = BytesIO()
        self._pycurlObj = pycurl.Curl()
        self._pycurlObj.setopt(self._pycurlObj.URL, self._url)
        self._pycurlObj.setopt(self._pycurlObj.CONNECTTIMEOUT, 10)
        self._pycurlObj.setopt(self._pycurlObj.WRITEDATA, self._buffer)

    def request(self, debug=False):
        """
        Nalaganje podatkov s strežnika.
        """
        # Počistimo pomnilnik za shranjevanje sporočila
        self._buffer.seek(0, 0)
        self._buffer.truncate()
        # Pošljemo zahtevek na strežnik
        self._pycurlObj.perform()
        # Dekodiramo sporočilo
        msg = self._buffer.getvalue().decode()
        # Izluščimo podatke iz JSON
        try:
            return ujson.loads(msg)
        except ValueError as val_err:
            if debug:
                print('Napaka pri razclenjevanju datoteke JSON: ' + str(val_err))
                print('Sporocilo streznika:')
                print(msg)
            return -1

    def testDelay(self, numOfIterations: int = 10):
        """
        Merjenje zakasnitve pri pridobivanju podatkov o tekmi s strežnika.
        Zgolj informativno.
        """
        sumTime = 0
        for _ in range(numOfIterations):
            startTime = time()
            if self.request() == -1:
                print('Napaka pri vzpostavljanju povezave s strežnikom.')
                sys.exit(0)
            elapsedTime = time() - startTime
            sumTime += elapsedTime
        return sumTime / numOfIterations
