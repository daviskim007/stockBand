import re
import time
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


def heavy_work(name):
    result = 0
    for i in trange(4000000,file=desc,desc="Y"):
        result += i
    print('%s done' % name)

rng_a = trange(4)
desc = DescStr()
for i in rng_a:
    result = 0
    for i in trange(4000000, file=desc, desc="Y"):
        rng_a.set_description(desc.read())
        time.sleep(0.1)
