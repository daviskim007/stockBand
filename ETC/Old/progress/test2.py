import re
from time import sleep
from tqdm import trange
class DescStr:
    def __init__(self):
        self._desc= ''
    def write(self, instr):
        self._desc += re.sub('\n|\x1b.*|\r', '', instr)
    def read(self):
        ret= self._desc
        self._desc= ''
        return ret
    def flush(self):
        pass

rng_a= trange(20)
desc= DescStr()
for x in rng_a:
    for y in trange(10, file=desc, desc="Y"):
        rng_a.set_description(desc.read())
        sleep(0.1)