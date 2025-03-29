from datetime import UTC, datetime


def current_timestamp() -> float:
    return datetime.now(UTC).timestamp()
