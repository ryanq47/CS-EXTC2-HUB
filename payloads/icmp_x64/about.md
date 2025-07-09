#### ICMP_X64

>> BUSTED - crashes after getting payload. something is up

An ICMP channel for Beacons, implemented using Cobalt Strike’s External C2 framework.

#### Key Concepts

- **ICMP Echo Request (Type 8)**: Used by the client (“agent”) to signal the server (“controller”) and request data.
<br><br> 
- **ICMP Echo Reply (Type 0)**: Used by the controller to embed and send replies (including large payloads) back to the client.
<br><br> 
- **TAG (4 bytes)**: A fixed 4‐byte marker (e.g. `RQ47`) prepended to every ICMP payload, so that unrelated OS pings or network noise are ignored.
<br><br> 
- **Chunking**: When the controller needs to send more data than fits in a single ICMP payload (1000 bytes), it splits the payload into fragments of up to **996** bytes each (ICMP_PAYLOAD_SIZE – TAG_SIZE = 1000 – 4). Each fragment still carries the same 4‐byte tag.
