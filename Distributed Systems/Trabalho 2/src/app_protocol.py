import struct
import uuid
from typing import Tuple

# application-layer opcodes
OP_START = 0x10
OP_CHUNK = 0x20
OP_COMMIT = 0x30
OP_DELETE_FILE = 0x40
OP_READ_REQUEST = 0x50
OP_READ_RESPONSE = 0x51
OP_LIST_REQUEST = 0x60
OP_LIST_RESPONSE = 0x61


# ---------- start / chunk (raw uuid, no length prefix needed) ----------

def pack_app_start(session_uuid: uuid.UUID) -> bytes:
    return session_uuid.bytes

def unpack_app_start(data: bytes) -> uuid.UUID:
    return uuid.UUID(bytes=data[:16])

def pack_app_chunk(session_uuid: uuid.UUID, chunk_data: bytes) -> bytes:
    # uuid up front, then the raw file bytes for this chunk
    return session_uuid.bytes + chunk_data

def unpack_app_chunk(data: bytes) -> Tuple[uuid.UUID, bytes]:
    session_uuid = uuid.UUID(bytes=data[:16])
    chunk_data = data[16:]
    return session_uuid, chunk_data


# ---------- commit (uuid + the final filename) ----------

def pack_app_commit(session_uuid: uuid.UUID, filename: str) -> bytes:
    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)
    header = struct.pack("!16sH", session_uuid.bytes, filename_len)
    return header + filename_bytes

def unpack_app_commit(data: bytes) -> Tuple[uuid.UUID, str]:
    session_uuid_bytes, filename_len = struct.unpack("!16sH", data[:18])
    session_uuid = uuid.UUID(bytes=session_uuid_bytes)
    filename = data[18:18 + filename_len].decode('utf-8')
    return session_uuid, filename


# ---------- delete / read request (just a filename) ----------

def pack_app_delete(filename: str) -> bytes:
    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)
    return struct.pack("!H", filename_len) + filename_bytes

def unpack_app_delete(data: bytes) -> str:
    filename_len, = struct.unpack("!H", data[:2])
    return data[2:2 + filename_len].decode('utf-8')

def pack_app_read_request(filename: str) -> bytes:
    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)
    return struct.pack("!H", filename_len) + filename_bytes

def unpack_app_read_request(data: bytes) -> str:
    filename_len, = struct.unpack("!H", data[:2])
    return data[2:2 + filename_len].decode('utf-8')


# ---------- read / list responses ----------

def pack_app_read_response(status: int, chunk_data: bytes) -> bytes:
    # 1-byte status (0 = ok) then the file bytes
    return struct.pack("!B", status) + chunk_data

def unpack_app_read_response(data: bytes) -> Tuple[int, bytes]:
    status, = struct.unpack("!B", data[:1])
    return status, data[1:]

def pack_app_list_response(json_str: str) -> bytes:
    # list dump can be big, so it gets a wider 4-byte length prefix
    json_bytes = json_str.encode('utf-8')
    return struct.pack("!I", len(json_bytes)) + json_bytes

def unpack_app_list_response(data: bytes) -> str:
    json_len, = struct.unpack("!I", data[:4])
    return data[4:4 + json_len].decode('utf-8')
