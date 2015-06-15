from abc import abstractmethod

__author__ = 'ktulhy'


class TokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self._get_error_msg().format(str(self.token))

    @abstractmethod
    def _get_error_msg(self):
        return ""


class TokenQuotedError(TokenError):
    def _get_error_msg(self):
        return "Ошибка в кавычках в токене {}"


# AST errors

class TokenOutsideBlock(TokenError):
    def _get_error_msg(self):
        return "Токен {} находится вне блока"


class UnknownBlock(TokenError):
    def _get_error_msg(self):
        return "Неизвестное имя блока: {}"


class NeedNewLine(TokenError):
    def _get_error_msg(self):
        return "Ожидается NEWLINE, а тут {}"


class NeedBlockOrSubBlock(TokenError):
    def _get_error_msg(self):
        return "Ожидается '.' или '..', а тут {}"
