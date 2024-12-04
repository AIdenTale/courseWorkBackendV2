def required_float(v: float):
    assert v is not None
    if v <= 0:
        raise AssertionError("float must be positive")
    return v