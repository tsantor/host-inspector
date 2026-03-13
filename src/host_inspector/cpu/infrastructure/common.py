def clean_processor_name(name: str) -> str:
    """Return a clean processor name."""
    cleaned = name.replace("(R)", "").replace("(TM)", "")
    return cleaned.split("CPU @")[0].strip()
