class ServiceUnavailableException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class EmailAlreadyRegistered(Exception):
    def __init__(self, email):
        self.email = email

    def __str__(self):
        return self.email + " уже зарегистрирован"