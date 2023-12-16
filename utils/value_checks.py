def is_positive_number(value):
    try:
        number = float(value)
    except Exception:
        return False
    return number > 0
