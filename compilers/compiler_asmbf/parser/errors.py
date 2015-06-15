__author__ = 'ktulhy'

class TokenQuotedError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Ошибка в кавычках в токене {}".format(str(self.token))

# AST errors

class TokenOutsideBlock(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Токен {} находится вне блока".format(str(self.token))

class UnknownBlock(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Неизвестное имя блока: {}".format(str(self.token))

