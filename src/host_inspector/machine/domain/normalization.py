import uuid


def normalize_machine_id(value: str) -> str:
    """Normalize machine id to canonical UUID string."""
    return str(uuid.UUID(value.strip()))
