import time
import uuid
from secrets import randbits


def uuidv7() -> uuid.UUID:
    ts_ms = int(time.time() * 1000) & ((1 << 48) - 1)
    rand_a = randbits(12)
    rand_b = randbits(62)

    value = ts_ms << 80
    value |= 0x7 << 76
    value |= (rand_a & ((1 << 12) - 1)) << 64
    value |= 0x2 << 62
    value |= rand_b & ((1 << 62) - 1)

    return uuid.UUID(int=value)

