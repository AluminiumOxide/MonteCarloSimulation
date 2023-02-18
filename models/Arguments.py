import argparse
import os


class Argument:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def init_mci(self):
        # 前这一部分是控制训练的参数
        self.parser.add_argument('--photon_number', type=int, default=1000, help='total simulation photon number')
        self.parser.add_argument('--path_input', type=str, default='./bin_input')
        self.parser.add_argument('--path_output', type=str, default='./bin_output')
        self.parser.add_argument('--prefix', type=str, default='oppo122')

        parser = self.parser.parse_args()

        # 后面是读取mci数据获得的参数
        path_file = os.path.join(parser.path_input, parser.prefix + '_H.mci')
        with open(path_file, 'r', encoding='UTF-8') as file:
            infos = file.readlines()

        infos = [float(x.strip('\n')) for x in infos]  # 不知道为啥正常读取全是带\n的str，全部整理成浮点的
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
        self.parser.add_argument('--v_mua', type=list, default=v_mua, help='Optical absorption coefficient')
        self.parser.add_argument('--v_mus', type=list, default=v_mus, help='Optical scattering coefficient')
        self.parser.add_argument('--v_g', type=list, default=v_g, help='Anisotropy parameter')

        args = self.parser.parse_args()
        # -----------------------------------------------------------------------------------------------
        path_file = os.path.join(args.path_output, args.prefix + '_prop.m')
        with open(path_file, "w", encoding='UTF-8') as file:
            for i in range(args.v_Nt):
                file.write('muav({0:.0f})={1:.4f};\nmusv({0:.0f})={2:.4f};\nmusv({0:.0f})={3:.4f};\n\n'.format(
                    i + 1, args.v_mua[i], args.v_mus[i], args.v_g[i]))

        return args







