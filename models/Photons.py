import numpy as np
import random
import math
from copy import deepcopy

from tools.iteration import same_voxel, find_voxel_margin


class Photon:
    def __init__(self):
        self.flag_b = False
        self.move_cnt = 0
        self.move_pos = [0, 0, 0]
        self.move_sleft = 0
        self.move_step = 0  # 反正是跟着sleft变的，是不是可以删了
        self.num_index = 0
        self.pho_index = [0, 0, 0]
        self.pho_pos = [0, 0, 0]
        self.pho_radiu = [0, 0, 0]
        self.pho_status = True
        self.pho_w = 1
        self.tis_g = 0.0
        self.tis_mua = 0.0
        self.tis_mus = 0.0

    def set_source(self, opt, light):
        """
        判断flag，返回位置和角度信息
        """
        if opt.flag_launch == 1:
            self.pho_pos = deepcopy(opt.space_s)
            self.pho_radiu = deepcopy(opt.space_u0)
        else:
            if opt.flag_mc == 0:

                self.pho_pos = deepcopy(opt.space_s)

                theta_r = random.uniform(0, 90)  # 纬角 = 0.5π*rand  uniform是左闭右闭
                theta_w = round(theta_r)
                theta_cos = math.cos(theta_r / 180 * math.pi)
                theta_sin = math.sqrt(1.0 - theta_cos * theta_cos)

                psi_r = random.uniform(0, 359.99)  # 经角 = 2π*rand  uniform是左闭右闭
                psi_w = math.floor(psi_r)  # 没办法,索引只有0~359
                psi_cos = math.cos(psi_r / 180 * math.pi)
                if psi_r < 180:
                    psi_sin = math.sqrt(1.0 - psi_cos * psi_cos)
                else:
                    psi_sin = -1 * math.sqrt(1.0 - psi_cos * psi_cos)

                self.pho_radiu = [theta_sin * psi_cos, theta_sin * psi_sin, theta_cos]
                self.pho_w = light.data[theta_w][psi_w]

        pho_i = []
        pho_i.append(int(opt.space_N[0] / 2 + self.pho_pos[0] / opt.space_d[0]))  # ix
        pho_i.append(int(opt.space_N[1] / 2 + self.pho_pos[1] / opt.space_d[1]))  # iy
        pho_i.append(int(self.pho_pos[2] / opt.space_d[2]))  # iz
        for i in range(3):
            if pho_i[i] >= opt.space_N[i]:
                pho_i[i] = opt.space_N[i] - 1
            if pho_i[i] < 0:
                pho_i[i] = 0

        self.pho_index = pho_i

    def set_tissue(self, tissue):
        """
        根据光子的当前位置，更新当前位置组织的光学信息 photon update tissue optical info
        """
        type = tissue.mat_v[self.pho_index[2], self.pho_index[1], self.pho_index[0]]
        # print(type)
        self.tis_mua = tissue.v_mua[type - 1]  # 应该是需要-1的?
        self.tis_mus = tissue.v_mus[type - 1]  # 应该是需要-1的?
        self.tis_g = tissue.v_g[type - 1]  # 应该是需要-1的?

    def set_others(self):
        # 重置光子其他信息 未接触边界 光子存活 重置光子移动
        self.flag_b = True
        self.pho_status = True
        self.move_cnt = 0

    def set_step(self):
        """
        每次光子只要没死，就都会重新设置一个随机的移动步长，并且纪录移动次数
        """
        rnd = 1 - random.random()  # 这样出来是(0, 1]的
        self.move_sleft = -math.log(rnd)
        self.move_cnt = self.move_cnt + 1


    def boundary_treatment(self, flag_boundary, voxel_N):
        if flag_boundary == 0:  # 边界处理 Infinite medium.
            pass
        elif flag_boundary == 1:  # 超出边缘强制跳出 Escape at boundaries
            for i, (pho_index, vox_N) in enumerate(zip(self.pho_index, voxel_N)):
                if pho_index >= vox_N:
                    self.pho_index[i] = voxel_N[i] - 1
                    self.pho_status = False
                    self.move_sleft = 0
                    # print('\t\ttorch boundary_1')
            for i, pho_index in enumerate(self.pho_index):
                if pho_index < 0:
                    self.pho_index[i] = 0
                    self.pho_status = False
                    self.move_sleft = 0
                    # print('\t\ttorch boundary_2')
        elif flag_boundary == 2:  # Escape at top surface, no x,y bottom z boundaries
            pass


    def iteration_sleft(self, tis, flag_boundary, with_print=False):
        self.move_step = self.move_sleft / (self.tis_mus + 1e-12)

        for i in range(3):
            self.move_pos[i] = self.pho_pos[i] + self.move_step * self.pho_radiu[i]
        # 这里的检测过没过等之后再加
        if with_print:
            print('\t <<< begin sleft >>> ------------------------')
            print('\t --- tis_mus {}'.format(self.tis_mus))
            print('\t --- space1 {}'.format(self.pho_pos))
            print('\t --- space2 {}'.format(self.move_pos))
            print('\t --- move_step {}'.format(self.move_step))
            print('\t --- angle component {}'.format(self.pho_radiu))

        sv = same_voxel(self.pho_pos, self.move_pos, tis.vox_d)

        if with_print:
            print('\tin the same voxel') if sv else print('\tcrossed voxel boundary')

        if sv:  # in the same voxel
            self.pho_pos = deepcopy(self.move_pos)

            # Drop photon weight (W) into local bin.
            absorb = self.pho_w * (1 - math.exp(-self.tis_mua * self.move_step))
            self.pho_w -= absorb  # decrement WEIGHT by amount absorbed

            tis.mat_f[self.pho_index[2], self.pho_index[1], self.pho_index[0]] += absorb  # ############################

            self.move_sleft = 0

        else:  # photon has crossed voxel boundary
            s = find_voxel_margin(self.pho_pos, self.move_pos, tis.vox_d, self.pho_radiu)

            # Drop photon weight (W) into local bin
            absorb = self.pho_w * (1 - math.exp(-self.tis_mua * self.move_step))
            self.pho_w -= absorb

            tis.mat_f[self.pho_index[2], self.pho_index[1], self.pho_index[0]] += absorb   # ###########################
            self.move_sleft -= s * self.tis_mus

            if self.move_sleft <= 1e-5:
                self.move_sleft = 0

            self.pho_pos[0] += s * self.pho_radiu[0]
            self.pho_pos[1] += s * self.pho_radiu[1]
            self.pho_pos[2] += s * self.pho_radiu[2]

            self.pho_index[0] = int(tis.vox_N[0] / 2 + self.pho_pos[0] / tis.vox_d[0])
            self.pho_index[1] = int(tis.vox_N[1] / 2 + self.pho_pos[1] / tis.vox_d[1])
            self.pho_index[2] = int(                   self.pho_pos[2] / tis.vox_d[2])

            self.boundary_treatment(flag_boundary, tis.vox_N)  # 边界条件，因为还需要修改光子包中的数据，还是按内部方法来吧

            # update pointer to tissue type
            type = tis.mat_v[self.pho_index[2], self.pho_index[1], self.pho_index[0]]
            self.tis_mua = tis.v_mua[type - 1]
            self.tis_mus = tis.v_mus[type - 1]
            self.tis_g = tis.v_g[type - 1]

        if with_print:
            print('\t >>> position index {} location {:.4f} {:.4f} {:.4f}'.format(self.pho_index,self.pho_pos[0], self.pho_pos[1], self.pho_pos[2]))
            print('\t >>> photon move count {} with weight {} and step {} '.format(self.move_cnt, self.pho_w, self.move_step))
            print('\t <<< end sleft >>> ------------------------')

    def change_direction(self, with_print=False):
        g = self.tis_g
        if g == 0:
            theta_cos = 2.0 * random.random() - 1.0
        else:
            temp = (1.0 - g * g) / (1.0 - g + 2 * g * random.random())
            theta_cos = (1.0 + g * g - temp * temp) / (2.0 * g)
        theta_sin = math.sqrt(1.0 - theta_cos * theta_cos)
        # Sample psi
        psi = 2.0 * math.pi * random.random()
        psi_cos = math.cos(psi)
        if psi < math.pi:
            psi_sin = math.sqrt(1.0 - psi_cos * psi_cos)
        else:
            psi_sin = -math.sqrt(1.0 - psi_cos * psi_cos)
        # New trajectory
        u_x,u_y,u_z = self.pho_radiu
        # u_x * u_x + u_y * u_y + u_z * u_z
        if (1 - math.fabs(u_z)) <= 1e-12:
            new_ux = theta_sin * psi_cos
            new_uy = theta_sin * psi_sin
            if u_z >= 0:
                new_uz = theta_cos
            else:
                new_uz = - theta_cos
        else:
            temp = math.sqrt(1.0-u_z*u_z)
            new_ux = theta_sin*(u_x * u_z * psi_cos - u_y * psi_sin) / temp + u_x * theta_cos
            new_uy = theta_sin*(u_y * u_z * psi_cos - u_x * psi_sin) / temp + u_y * theta_cos
            new_uz = -theta_sin*psi_cos*temp + u_z*theta_cos

        adjust = new_ux*new_ux + new_uy*new_uy + new_uz*new_uz
        if math.fabs(adjust-1) > 0.001:
            if with_print:
                print("原来这里平方和不为1吗？ {}".format(adjust))
            adjust_sqrt = math.sqrt(adjust)
            new_ux = new_ux/adjust_sqrt
            new_uy = new_uy/adjust_sqrt
            new_uz = new_uz/adjust_sqrt
            adjust = new_ux*new_ux + new_uy*new_uy + new_uz*new_uz
            if with_print:
                print("调整至当前平方和 {}".format(adjust))

        self.pho_radiu[0] = new_ux
        self.pho_radiu[1] = new_uy
        self.pho_radiu[2] = new_uz

    def roulette(self):
        THRESHOLD, CHANCE = 0.01, 0.1
        if self.pho_w < THRESHOLD:
            if random.random() <= CHANCE:
                self.pho_w /= CHANCE
            else:
                self.pho_status = False