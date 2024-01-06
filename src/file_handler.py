# Imports
import os
from bodies import StaticBody, DynamicBody
from config import Configuration

def convert(txt):
    content = txt.split(" ")
    static = content[0].split("|")
    static_bodies = []
    if static != ["0"]:
        for info in static:
            mass, x, y = info.split(",")
            static_bodies.append(StaticBody(float(mass), [float(x), float(y)]))
    dynamic = content[1].split("|")
    dynamic_bodies = []
    if dynamic != ["0"]:
        for info in dynamic:
            mass, x, y, dx, dy = info.split(",")
            dynamic_bodies.append(DynamicBody(float(mass), [float(x), float(y)], [float(dx), float(dy)]))
    settings = content[2].split(",")
    for i in range(len(settings)):
        if i < 3:
            settings[i] = int(settings[i])
        elif i < 6:
            settings[i] = float(settings[i])
        else:
            settings[i] = settings[i]=="True"
    return Configuration(static_bodies, dynamic_bodies, settings)

class FileHandler:

    filedir = "configs/"

    def fwrite(self, history, name):
        file = open(self.filedir+name+".txt", "w")
        file.write("".join(config.short()+"\n" for config in history))
        file.close()

    def fdir(self):
        return os.listdir(self.filedir)

    def fread(self, name):
        return [convert(line) for line in open(self.filedir+name, "r").readlines()]

_inst = FileHandler()
fwrite = _inst.fwrite
fdir = _inst.fdir
fread = _inst.fread

if hasattr(os, "fork"):
    os.register_at_fork(after_in_child = _inst.__init__)

if __name__ == "__main__":
    fh = FileHandler()
    print(fh.fdir())
    print(fh.fread(input()))
