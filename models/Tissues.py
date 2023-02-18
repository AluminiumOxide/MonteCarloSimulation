import os
import struct

import numpy as np


class Tissue:
    def __init__(self,opts):

        path_file = os.path.join(opts.path_input, opts.prefix + '_T.bin')
        bin_size = os.path.getsize(path_file)
        matrix_v = []
        with open(path_file, 'rb') as file:
            for _ in range(bin_size):
                bin_info = file.read(1)
                bin_info = struct.unpack('B', bin_info)
                matrix_v.append(bin_info[0])
        matrix_v = np.array(matrix_v)
        Nx, Ny, Nz = opts.space_N[0], opts.space_N[1], opts.space_N[2]
        matrix_v = matrix_v.reshape((Nz, Ny, Nx))  # 默认按照reshape计算是反的，因此需要transpose
        # matrix_v = matrix_v.transpose(2, 1, 0)  # 当前空间按照 x y z 进行计算 会造成后面各种画图很费劲，算了算了
        matrix_f = np.zeros(shape=(Nz, Ny, Nx))
        matrix_r = np.zeros(shape=(Nz, Ny, Nx))

        self.mat_f=matrix_f
        self.mat_r=matrix_r
        self.mat_v=matrix_v
        self.v_g=opts.v_g
        self.v_mua=opts.v_mua
        self.v_mus=opts.v_mus
        self.vox_N=opts.space_N
        self.vox_d=opts.space_d


def save_tissue(path_output, prefix, optical_flux):
    save_path = os.path.join(path_output, prefix + '_F.bin')
    # 估计得改
    length = optical_flux.shape[0] * optical_flux.shape[1] * optical_flux.shape[2]
    optical_flux = optical_flux.reshape(length)
    optical_flux = optical_flux.astype(np.float32)
    optical_flux.tofile(save_path)
    # with open(save_path,'wb') as file:
    #     data = struct.pack(('%df' % len(list)), *optical_flux)
    #     file.write(data)