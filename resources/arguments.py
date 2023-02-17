import argparse
import os
import numpy as np
import struct


class Arguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def init_mci(self, path_input, prefix, save_prop=False, path_output=None):
        path_file = os.path.join(path_input, prefix + '_H.mci')

        with open(path_file, 'r', encoding='UTF-8') as file:
            infos = file.readlines()

        infos = [float(x.strip('\n')) for x in infos]  # 不知道为啥正常读取全是带\n的str，全部整理成浮点的
        # int(float(file_info[0].strip('\n')))
        # 先把xyz的按照space前缀来表示了，之后慢慢改
        self.parser.add_argument('--time', type=float, default=infos[0], help='simulation time')
        self.parser.add_argument('--space_N', type=list, default=[int(infos[1]), int(infos[2]), int(infos[3])],
                                 help='bins number Nx Ny Nz')
        self.parser.add_argument('--space_d', type=list, default=[infos[4], infos[5], infos[6]],
                                 help='bins size Nx Ny Nz (cm)')

        self.parser.add_argument('--flag_mc', type=int, default=int(infos[7]), help='Light source mode set by matlab')
        self.parser.add_argument('--flag_launch', type=int, default=int(infos[8]), help='Launch mode set by matlab')
        self.parser.add_argument('--flag_boundary', type=int, default=int(infos[9]), help='Boundary set by matlab')

        self.parser.add_argument('--space_s', type=list, default=[infos[10], infos[11], infos[12]],
                                 help='The position of photon init xs,ys,zs')
        self.parser.add_argument('--space_focus', type=list, default=[infos[13], infos[14], infos[15]],
                                 help='The position of light source xfocus，yfocus，zfocus')
        self.parser.add_argument('--space_u0', type=list, default=[infos[16], infos[17], infos[18]],
                                 help='The proportion of the angle of photon movement on xyz, Sum of squares == 1')
        self.parser.add_argument('--radius_waist', type=list, default=[infos[19], infos[20]],
                                 help='waitting')  # 光源在皮肤表面的半径 & 光源在光子启动处的半径
        # 组织的光学性质,先按照都是 v_前缀 Optical properties
        self.parser.add_argument('--v_Nt', type=int, default=int(infos[21]), help='Categories number of organization')
        properties = infos[22:]
        v_mua, v_mus, v_g = [], [], []
        for i in range(0, int(infos[21] * 3), 3):
            v_mua.append(properties[i])
            v_mus.append(properties[i + 1])
            v_g.append(properties[i + 2])
        # print('ua: {}\nus: {}\ng : {}'.format(v_mua, v_mus, v_g))
        self.parser.add_argument('--v_mua', type=list, default=v_mua, help='Optical absorption coefficient')
        self.parser.add_argument('--v_mus', type=list, default=v_mus, help='Optical scattering coefficient')
        self.parser.add_argument('--v_g', type=list, default=v_g, help='Anisotropy parameter')

        # 后面这一部分是添加的其他参数
        self.parser.add_argument('--photon_number', type=int, default=10000, help='total simulation photon number')

        args = self.parser.parse_args()

        if save_prop:
            path_file = os.path.join(path_output, prefix + '_prop.m')
            with open(path_file, "w", encoding='UTF-8') as file:
                for i in range(args.v_Nt):
                    file.write('muav({0:.0f})={1:.4f};\nmusv({0:.0f})={2:.4f};\nmusv({0:.0f})={3:.4f};\n\n'.format(
                        i + 1, args.v_mua[i], args.v_mus[i], args.v_g[i]))

        return args


class Probe:   # position : [x,y,hh]  scale : [width,height]
    def __init__(self, position, scale):
        self.position = position
        self.scale = scale


class Probes:
    def __init__(self):
        self.p_1 = Probe([-0.6 + 0.0945, -0.1675, 1.22], [0.189, 0.355])
        self.p_2 = Probe([0.6 - 0.0945, -0.1675, 1.22], [0.189, 0.355])
        self.p_3 = Probe([0, -0.6, 1.22], [0.355, 0.189])
        self.p_4 = Probe([0, 0.6 - 0.189, 1.22], [0.355, 0.189])


class Photon:
    def __init__(self):
        self.flag_b = False
        self.move_cnt = 0
        self.move_pos = [0, 0, 0]
        self.move_sleft = 0
        self.move_step = 0   # 反正是跟着sleft变的，是不是可以删了
        self.num_index = 0
        self.pho_index = [0, 0, 0]
        self.pho_pos = [0, 0, 0]
        self.pho_radiu = [0, 0, 0]
        self.pho_status = True
        self.pho_w = 1
        self.tis_g = 0.0
        self.tis_mua = 0.0
        self.tis_mus = 0.0


class Tissue:
    def __init__(self,opts,path_input,prefix):

        path_file = os.path.join(path_input, prefix + '_T.bin')
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


class Lights:
    def __init__(self, path_input):
        path_file = os.path.join(path_input, 'data.txt')
        lines = []
        for line in open(path_file, "r", encoding="utf-8"):
            line = [float(temp) for temp in line.split()]
            lines.append(line)
        self.data = np.array(lines)



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

