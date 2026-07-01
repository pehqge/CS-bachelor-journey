# ===================== communicator.py =====================
# wrapper over a TCP socket that does length-prefixed framing.
#
# raw TCP is a byte stream with no message boundaries, so two frames sent
# back to back can arrive glued together (or split apart). we fix that the
# usual way: a 4-byte big-endian length in front of every frame, and a recv
# loop that reads exactly that many bytes before handing the frame back.
#
# the socket timeout doubles as our failure detector -- a peer that goes
# silent eventually trips a timeout instead of hanging us forever.
# ===========================================================

import socket
import struct
from typing import Optional

class Communicator:
    def __init__(self, sock: socket.socket, timeout: Optional[float] = None):
        self.sock = sock
        if timeout is not None:
            self.sock.settimeout(timeout)

    def send_frame(self, data: bytes) -> None:
        # 4-byte length up front, then the payload
        length_prefix = struct.pack("!I", len(data))
        self.sock.sendall(length_prefix + data)

    def receive_frame(self) -> bytes:
        # read the length, then loop until we've got the whole frame
        length_data = self._read_exact(4)
        if not length_data:
            raise ConnectionAbortedError("Connection closed by peer while reading frame length.")

        frame_len, = struct.unpack("!I", length_data)
        frame_data = self._read_exact(frame_len)
        if len(frame_data) < frame_len:
            raise ConnectionAbortedError("Connection closed before frame content was fully read.")

        return frame_data

    def _read_exact(self, num_bytes: int) -> bytes:
        # recv can return fewer bytes than asked, so keep pulling until full
        data = bytearray()
        while len(data) < num_bytes:
            packet = self.sock.recv(num_bytes - len(data))
            if not packet:
                break
            data.extend(packet)
        return bytes(data)

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass
