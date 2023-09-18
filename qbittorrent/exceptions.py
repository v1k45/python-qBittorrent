class LoginRequired(Exception):
    def __str__(self):
        return "Please login first."


class WrongCredentials(Exception):
    def __str__(self):
        return "Please make sure the username and password are correct"
