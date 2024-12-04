def required(v: str):
    assert v is not None
    assert len(v) > 0
    return v
