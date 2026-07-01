# Wire protocol

The protocol is layered: framing at the bottom, replication in the middle, and
the filesystem (application) on top. Each layer wraps the one above it.

## Layer 1: framing (the Communicator)

Everything on a TCP socket goes through length-prefixed framing, because TCP is
a byte stream with no message boundaries.

- Every payload is prefixed with a 4-byte unsigned integer `N` = the length of
  what follows.
- The receiver reads exactly 4 bytes, allocates an `N`-byte buffer, and loops
  on `recv` until it's full.

## Layer 2: replication (SMR)

These opcodes manage the state machine and cluster health. They ride inside the
replication header: `[Epoch ID (4 bytes)] [Sequence ID (4 bytes)] [OpCode (1 byte)]`.

- `0x01` APP_DATA -- opaque payload from the application layer. Broadcast by the leader.
- `0x02` HEARTBEAT -- broadcast by the leader every few seconds to prove it's alive.
- `0x03` REPLICATION_ACK -- sent by followers to confirm they persisted an
  `0x01` payload (or received a heartbeat). Unblocks the synchronous wait.
- `0x04` CATCHUP_REQUEST -- sent by a recovering follower on connect. Carries its
  last known sequence ID.
- `0x05` SNAPSHOT_TRANSMIT -- leader's reply to a catch-up when the requested
  sequence was already compacted away. Carries a `.tar.gz` payload.
- `0x06` WRONG_LEADER -- a follower's reply to a client that connected to it by
  mistake. Carries the `host:port` of the real leader so the client can reconnect.
- `0x07` I_AM_FOLLOWER -- identity handshake from a follower. Tells the leader to
  add this socket to the broadcast list.
- `0x08` I_AM_CLIENT -- identity handshake from a client. Tells the leader to
  treat the socket as a command connection and not blast SMR traffic at it.
- `0x09` WHO_IS_LEADER -- one-byte discovery probe a follower sends to each peer
  while hunting for the current leader. Only a leader replies (`0x0A`); the rest
  stay quiet and get skipped.
- `0x0A` LEADER_ANNOUNCE -- a leader's reply to a `0x09` probe (and the ack to a
  `0x0B`). The header carries the responder's epoch; the prober keeps the
  highest-epoch one, so a freshly promoted leader beats a ghost.
- `0x0B` PROMOTE -- one-byte admin command (operator/script -> one chosen
  follower). Flips that node to leader at runtime, no restart, bumping its epoch
  to N+1. The other followers rediscover it on their own via `0x09`/`0x0A`.

## Layer 3: application (filesystem)

These define user intent. They travel as opaque bytes inside an `0x01 APP_DATA`
replication payload, or are sent directly by clients for reads.

### Writes (sequenced by the leader)

- `0x10` START -- begin an upload. Carries a 16-byte session UUID. Creates a
  `.UUID.part` temp file.
- `0x20` CHUNK -- a 4MB slice of file data, keyed by the session UUID. Appended
  to `.UUID.part`.
- `0x30` COMMIT -- finish the upload. Carries the UUID and target filename. Does
  an atomic `os.rename('.UUID.part', 'filename')`. On a name clash the leader
  appends a `(1)` suffix.
- `0x40` DELETE_FILE -- delete a file. Removes it from disk and from the in-memory
  metadata.

### Reads (served by the leader, don't bump the sequence)

- `0x50` READ_REQUEST -- client asks for a file. Carries the filename.
- `0x51` READ_RESPONSE -- leader streams the file back.
- `0x60` LIST_REQUEST -- client asks for the directory listing.
- `0x61` LIST_RESPONSE -- leader replies with the JSON of the current
  `metadata.json`.
