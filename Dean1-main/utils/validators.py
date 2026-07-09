"""Input validation helper functions."""

def validate_non_empty(value: str, field_name: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError(f"{field_name} cannot be empty.")
    return value

def validate_unique_id(value: str, existing_ids: list, field_name: str) -> str:
    if value in existing_ids:
        raise ValueError(f"{field_name} '{value}' already exists.")
    return value

def validate_client_name(value: str) -> str:
    value = str(value).strip()
    if not value:
        raise ValueError("Client name cannot be empty.")
    return value
