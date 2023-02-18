import os

import numpy as np


class Light:
    def __init__(self, opt):
        path_file = os.path.join(opt.path_input, 'data.txt')
        lines = []
        for line in open(path_file, "r", encoding="utf-8"):
            line = [float(temp) for temp in line.split()]
            lines.append(line)
        self.data = np.array(lines)
