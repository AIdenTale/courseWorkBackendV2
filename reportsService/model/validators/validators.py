def required_int(v: int):
    assert v is not None
    assert v > 0
    return v

def required_list(v: int):
    assert v is not None
    assert len(v) > 0
    return v
