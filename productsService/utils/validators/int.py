def required_int(v: int):
    assert v is not None
    assert v > 0
    return v

def gte(v: int, number):
    assert v >= number
    return v

