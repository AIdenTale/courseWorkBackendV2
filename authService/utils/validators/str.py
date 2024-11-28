def required(v: str):
    assert len(v) > 0
    return v

def gte(v: str, number):
    assert len(v) >= number or number < 0
    return v

def email_required(v: str):
    from email_validator import validate_email

    try:
        emailinfo = validate_email(v, check_deliverability=False)
    except Exception as e:
        print(f"EMAIL VALIDATION FAILED: {v}, {e}")
        raise AssertionError("email incorrect")
    return emailinfo.normalized