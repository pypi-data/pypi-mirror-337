from datetime import datetime
from time import time


def generate_unix_ts_in_ms(timestamp: float | datetime | None = None) -> int:
    # Get current Unix timestamp in milliseconds (48 bits)
    if isinstance(timestamp, float | int):
        unix_ts_ms = int(timestamp * 1000) & 0xFFFFFFFFFFFF
    elif isinstance(timestamp, datetime):
        unix_ts_ms = int(timestamp.timestamp() * 1000) & 0xFFFFFFFFFFFF
    else:
        unix_ts_ms = int(time() * 1000) & 0xFFFFFFFFFFFF

    if unix_ts_ms > 0xFFFFFFFFFFFF:
        err_msg = f"Timestamp exceeds 48-bit limit: {unix_ts_ms}"
        raise ValueError(err_msg)

    return unix_ts_ms
