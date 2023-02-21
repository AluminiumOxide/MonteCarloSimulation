import numpy as np


class Probe:   # position : [x,y,hh]  scale : [width,height]
    def __init__(self, position, scale):
        self.position = np.array(position)
        self.scale = np.array(scale)


class Probe_list:
    def __init__(self):
        self.p_1 = Probe([0.05, 0, 0.122], [0.02, 0.036])
        self.p_2 = Probe([-0.05, 0, 0.122], [0.02, 0.036])
        self.p_3 = Probe([0, 0.05, 0.122], [0.036, 0.02])
        self.p_4 = Probe([0, -0.05, 0.122], [0.036, 0.02])

        # self.p_1 = Probe([-0.6 + 0.0945, -0.1675, 1.22], [0.189, 0.355])
        # self.p_2 = Probe([0.6 - 0.0945, -0.1675, 1.22], [0.189, 0.355])
        # self.p_3 = Probe([0, -0.6, 1.22], [0.355, 0.189])
        # self.p_4 = Probe([0, 0.6 - 0.189, 1.22], [0.355, 0.189])