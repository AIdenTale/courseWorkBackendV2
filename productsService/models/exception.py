class ServiceUnavailableException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class TokenVerifyException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ForeignKeyViolation(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class ZeroLinesUpdated(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
