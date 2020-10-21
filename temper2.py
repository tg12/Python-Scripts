'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



from __future__ import division
import sys
import time
import hid


class Temper2:

    vendor_id = 0x413D
    product_id = 0x2107
    name_query = [0x01, 0x86, 0xFF, 0x01, 0x00, 0x00, 0x00, 0x00]
    temp_query = [0x01, 0x80, 0x33, 0x01, 0x00, 0x00, 0x00, 0x00]
    max_open_tries = 10
    read_timeout = 500

    def __init__(self):
        self.h = hid.device()
        is_open = False
        tries = 0
        while not is_open:
            try:
                tries += 1
                self.h.open(self.vendor_id, self.product_id)
            except BaseException:
                if tries >= self.max_open_tries:
                    raise IOError("could not open device")
                time.sleep(0.1)
                continue
            is_open = True

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.h.close()

    def get_name(self):
        self.write(self.name_query)
        resp1 = self.read(8, self.read_timeout)
        resp2 = self.read(8, self.read_timeout)
        resp1_chars = self._read_string(resp1)
        resp2_chars = self._read_string(resp2)
        return resp1_chars + resp2_chars

    def get_temp(self):
        self.write(self.temp_query)
        resp1 = self.read(8, self.read_timeout)
        resp2 = self.read(8, self.read_timeout)
        if not resp1:
            return None, None
        int_temp = self._read_temp(resp1)
        if not resp2:
            ext_temp = None
        else:
            ext_temp = self._read_temp(resp2)
            if ext_temp == 200:
                # No external temperature recorded
                ext_temp = None
        return int_temp, ext_temp

    def write(self, data):
        self.h.write(data)

    def read(self, size, timeout=0):
        return self.h.read(size, timeout)

    @staticmethod
    def _read_string(b):
        return "".join([chr(r) for r in b])

    @staticmethod
    def _read_temp(b):
        return ((b[2] << 8) + b[3]) / 100


if __name__ == "__main__":
    with Temper2() as t:
        name = t.get_name()
        print(name)
        while True:
            int_temp, ext_temp = t.get_temp()
            print(int_temp, ext_temp)
            time.sleep(1)
