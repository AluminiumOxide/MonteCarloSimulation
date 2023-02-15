import argparse
import os
import numpy as np
import struct


def init_light(path_input):  # 静态就不加在类里了
    path_file = os.path.join(path_input, 'data.txt')
    lines = []
    for line in open(path_file, "r", encoding="utf-8"):
        line = [float(temp) for temp in line.split()]
        lines.append(line)
    datas = np.array(lines)
    return datas


class Arguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def init_mcx(self):
        # 这一部分是最开始初始化的()后面在调整位置
        self.parser.add_argument('--photon_n', type=int, default=5000000, help='photon number set to simulation')
        self.parser.add_argument('--photon_i', type=int, default=0, help='photon index set to simulation')
        self.parser.add_argument('--photon_w', type=float, default=1, help='photon weight set to simulation')
        self.parser.add_argument('--photon_status', type=bool, default=True, help='photon status set to simulation')
        # 后面这部分是需要按照mci设置的 pho认为是photon前缀
        self.parser.add_argument('--pho_pos', type=list, default=[0, 0, 0], help='photon position x y z')
        self.parser.add_argument('--pho_u', type=list, default=[0, 0, 0], help='photon angle component x y z')
        self.parser.add_argument('--pho_i', type=list, default=[0, 0, 0], help='photon index component x y z')
        # 后面这部分是需要按照bin设置的 tis认为是tissue前缀
        self.parser.add_argument('--tis_mua', type=float, default=0.0, help='tissue optical absorption')
        self.parser.add_argument('--tis_mus', type=float, default=0.0, help='tissue optical scattering')
        self.parser.add_argument('--tis_g', type=float, default=0.0, help='tissue Anisotropy parameter')
        # 后面这部分是运动过程中的flag
        self.parser.add_argument('--flag_b', type=bool, default=False,
                                 help='boundary flag True: continue, False: break')
        # 后面这部分是运动过程中的参数
        self.parser.add_argument('--hop_sleft', type=float, default=0, help='dimensionless step')
        self.parser.add_argument('--hop_step', type=float, default=0, help='step size')
        self.parser.add_argument('--hop_cnt', type=float, default=0, help='count step')
        self.parser.add_argument('--hop_pos', type=list, default=[0, 0, 0], help='position photon move to')

        args = self.parser.parse_args()
        return args

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
            v_mus.append(properties[i + 1]*0.0001)
            v_g.append(properties[i + 2])
        # print('ua: {}\nus: {}\ng : {}'.format(v_mua, v_mus, v_g))
        self.parser.add_argument('--v_mua', type=list, default=v_mua, help='Optical absorption coefficient')
        self.parser.add_argument('--v_mus', type=list, default=v_mus, help='Optical scattering coefficient')
        self.parser.add_argument('--v_g', type=list, default=v_g, help='Anisotropy parameter')

        args = self.parser.parse_args()

        if save_prop:
            path_file = os.path.join(path_output, prefix + '_prop.m')
            with open(path_file, "w", encoding='UTF-8') as file:
                for i in range(args.v_Nt):
                    file.write('muav({0:.0f})={1:.4f};\nmusv({0:.0f})={2:.4f};\nmusv({0:.0f})={3:.4f};\n\n'.format(
                        i + 1, args.v_mua[i], args.v_mus[i], args.v_g[i]))

        return args

    def init_probe(self):
        """
            position : [x,y, hh]
            scale : [width,height]
        """
        self.parser.add_argument('--probe_1', type=dict,
                                 default={'position': [-0.6 + 0.0945, -0.1675, 1.22], 'scale': [0.189, 0.355]}, help='')
        self.parser.add_argument('--probe_2', type=dict,
                                 default={'position': [0.6 - 0.0945, -0.1675, 1.22], 'scale': [0.189, 0.355]}, help='')
        self.parser.add_argument('--probe_3', type=dict,
                                 default={'position': [0, -0.6, 1.22], 'scale': [0.355, 0.189]}, help='')
        self.parser.add_argument('--probe_4', type=dict,
                                 default={'position': [0, 0.6 - 0.189, 1.22], 'scale': [0.355, 0.189]}, help='')

        args = self.parser.parse_args()
        return args

    def init_tissue(self, opts, path_input, prefix):
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

        self.parser.add_argument('--mat_v', default=matrix_v, help='Tissue info with z,y,x')
        self.parser.add_argument('--mat_f', default=matrix_f,
                                 help='Luminous flux with z,y,x also called relative fluence rate [W/cm^2/W.delivered]')
        self.parser.add_argument('--mat_r', default=matrix_r, help='escaping flux [W/cm^2/W.delivered] , not used')

        self.parser.add_argument('--v_mua', type=list, default=opts.v_mua, help='Optical absorption coefficient')
        self.parser.add_argument('--v_mus', type=list, default=opts.v_mus, help='Optical scattering coefficient')
        self.parser.add_argument('--v_g', type=list, default=opts.v_g, help='Anisotropy parameter')

        self.parser.add_argument('--vox_d', type=list, default=opts.space_d, help='tissue voxel bins size x y z')
        self.parser.add_argument('--vox_N', type=list, default=opts.space_N, help='tissue voxel number x y z')

        args = self.parser.parse_args()
        return args


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


if __name__ == '__main__':
    path_input = '../bin_input'
    path_output = '../bin_output'
    prefix = 'oppo122'
    opt_mci = Arguments().init_mci(path_input, prefix, True, path_output)  # 读mci、写prop
    opt_tissue = Arguments().init_tissue(opt_mci, path_input, prefix)

    print('tissue shape with z,y,x is {}'.format(opt_tissue.mat_v.shape))
    ix = int(opt_mci.space_N[0] / 2)
    iy = int(opt_mci.space_N[1] / 2)
    print('with cut from the center of z {}'.format(opt_tissue.mat_v[:, iy, ix]))

    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use('qt5agg')
    fig = plt.figure()  # 创建画布
    ax1, ax2, ax3 = fig.subplots(1, 3)  # 创建图表
    ax1.imshow(opt_tissue.mat_v[100, :, :])
    ax1.set_title('xy')
    ax2.imshow(opt_tissue.mat_v[:, 100, :])
    ax2.set_title('xz')
    ax3.imshow(opt_tissue.mat_v[:, :, 100])
    ax3.set_title('yz')
    # ax1.axis('off')
    # ax2.axis('off')
    # ax3.axis('off')
    plt.show()
