__author__ = 'ktulhy'


class Command:
    def __str__(self):
        return ""

    def compile(self):
        return ""


class At(Command):
    def __init__(self, i):
        self.v = i

    def compile(self):
        return ">" * self.v if self.v > 0 else "<" * self.v

    def __str__(self):
        return "@({})".format(self.v)


class Add(Command):
    def __init__(self, i):
        self.v = i

    def compile(self):
        return "+" * self.v if self.v > 0 else "-" * self.v

    def __str__(self):
        return ("+" if self.v > 0 else "-") + "({})".format(self.v)


class CycleStart(Command):
    def compile(self):
        return "["

    def __str__(self):
        return "["


class CycleEnd(Command):
    def compile(self):
        return "]"

    def __str__(self):
        return "]"


class Print(Command):
    def compile(self):
        return "."

    def __str__(self):
        return "."


class Read(Command):
    def compile(self):
        return ","

    def __str__(self):
        return ","


class Zero(Command):
    def compile(self):
        return "[-]"

    def __str__(self):
        return "0"