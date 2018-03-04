
def is_string(token):
    if isinstance(token, str):
        return token

    return None


def datetime_to_string(value, format_="%Y-%m-%d %H:%M:%S"):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime(format_)


def to_int(value):
    try:
        return int(value)
    except TypeError:
        return False
