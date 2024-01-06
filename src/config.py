class Configuration:

    def __init__(self, static, dynamic, settings):
        self.settings = settings
        self.static = static
        self.dynamic = dynamic

    def __repr__(self):
        return str(len(self.static))+" static bodies, "+str(len(self.dynamic))+" dynamic bodies"

    def short(self):
        s = "|".join(str(body) for body in self.static)
        if s == "":
            s = "0"
        d = "|".join(str(body) for body in self.dynamic)
        if d == "":
            d = "0"
        t = ",".join(str(s) for s in self.settings)
        return " ".join([s, d, t])

    def unpack(self):
        return self.static, self.dynamic, self.settings
