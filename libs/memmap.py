__author__ = 'ktulhy'


class Register:
    def __init__(self, name, byte, dim):
        self.name = name
        self.byte = byte
        self.dim = dim

    def __str__(self):
        return "{byte:06X}: {name:5}/{dim}".format(byte=self.byte, name=self.name, dim=self.dim)


class MemMap:
    def __init__(self):
        self.regs = {}
        self.byte = 0

        one_byte_regs = 16
        one_byte_support = 8
        two_byte_regs = 16
        two_byte_support = 16
        memory = 64 * 1024

        self._add_reg(Register("FN", self.byte, 1))
        self.byte += 1
        self._add_reg(Register("FZ", self.byte, 1))
        self.byte += 1
        self._add_reg(Register("FC", self.byte, 1))
        self.byte += 1
        self._add_reg(Register("FV", self.byte, 1))
        self.byte += 1
        self._add_reg(Register("FE", self.byte, 1))
        self.byte += 1

        self._gen_reg1_arr(one_byte_support, "_B{count:1X}")
        self._gen_reg1_arr(one_byte_regs, "B{count:1X}")
        self._gen_reg1_arr(1, "BR")

        self._gen_reg2_arr(two_byte_support, "_R{count:1X}{byte}")
        self._gen_reg2_arr(two_byte_regs, "R{count:1X}{byte}")
        self._gen_reg2_arr(1, "RR{byte}")

        for i in range(memory):
            self._gen_reg1(i, "DM{count:1X}")
            self._gen_reg2(i, "M{count:1X}{byte}")

    def __getitem__(self, item):
        return self.regs[item]

    def __str__(self):
        s = ""
        for k in sorted(self.regs.keys()):
            s += "{reg}\n".format(reg=self[k])

        return s

    def _gen_reg1_arr(self, count, name):
        for i in range(count):
            self._gen_reg1(i, name)

    def _gen_reg1(self, num, name):
        name = name.format(count=num)
        self._add_reg(Register(name, self.byte, 1))
        self.byte += 1

    def _gen_reg2_arr(self, count, name):
        for i in range(count):
            self._gen_reg2(i, name)

    def _gen_reg2(self, num, name):
        byte = self.byte

        nm = name.format(count=num, byte="H")
        self._add_reg(Register(nm, byte, 1))

        nm = name.format(count=num, byte="L")
        self._add_reg(Register(nm, byte + 1, 1))

        nm = name.format(count=num, byte="")
        self._add_reg(Register(nm, byte, 2))

        self.byte += 2

    def _add_reg(self, reg):
        self.regs[reg.name] = reg
