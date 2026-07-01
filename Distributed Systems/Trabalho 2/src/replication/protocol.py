# ===================== protocol.py (replication) =====================
# replication-layer (SMR) wire protocol: the opcodes nodes swap between
# each other and the header that rides in front of every frame.
#
# SMR header = 9 fixed bytes -> epoch (4) + sequence id (4) + opcode (1),
# packed as struct "!IIB" (big-endian). the app payload follows as opaque
# bytes; the replication layer never looks at what's inside.
# ====================================================================

import struct
from typing import Tuple

# replication-layer opcodes
OP_APP_DATA = 0x01
OP_HEARTBEAT = 0x02
OP_REPLICATION_ACK = 0x03
OP_CATCHUP_REQUEST = 0x04
OP_SNAPSHOT_TRANSMIT = 0x05
OP_WRONG_LEADER = 0x06
OP_I_AM_FOLLOWER = 0x07
OP_I_AM_CLIENT = 0x08
# leader discovery + runtime reconfiguration: followers find the current leader
# on their own, and an operator can flip one node to leader without restarts
OP_WHO_IS_LEADER = 0x09    
OP_LEADER_ANNOUNCE = 0x0A  
OP_PROMOTE = 0x0B         

# header layout: epoch (uint32), sequence id (uint32), opcode (uint8)
REPLICATION_HEADER_FORMAT = "!IIB"
REPLICATION_HEADER_SIZE = struct.calcsize(REPLICATION_HEADER_FORMAT)

def pack_replication_header(epoch_id: int, sequence_id: int, opcode: int) -> bytes:
    return struct.pack(REPLICATION_HEADER_FORMAT, epoch_id, sequence_id, opcode)

def unpack_replication_header(data: bytes) -> Tuple[int, int, int]:
    return struct.unpack(REPLICATION_HEADER_FORMAT, data)

def pack_wrong_leader(leader_host: str, leader_port: int) -> bytes:
    # packs the real leader's "host:port" so the client can bounce over to it
    addr_str = f"{leader_host}:{leader_port}"
    addr_bytes = addr_str.encode('utf-8')
    return struct.pack("!H", len(addr_bytes)) + addr_bytes

def unpack_wrong_leader(data: bytes) -> Tuple[str, int]:
    addr_len, = struct.unpack("!H", data[:2])
    addr_str = data[2:2 + addr_len].decode('utf-8')
    parts = addr_str.split(":")
    return parts[0], int(parts[1])
