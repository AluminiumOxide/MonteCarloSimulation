import random
import math
from copy import deepcopy


def set_source(opt_mci, photon, lights):
    """
    判断flag，返回位置和角度信息
    """
    if opt_mci.flag_launch == 1:
            photon.pho_pos = deepcopy(opt_mci.space_s)
            photon.pho_radiu = deepcopy(opt_mci.space_u0)
    else:
        if opt_mci.flag_mc == 0:
            # opt_mcx.pho_pos = opt_mci.space_s  # 这里先设置成这个  # 怪！为什么会干扰

            # for i in range(3):  # 可以 但是不够优雅
            #     photon['pho_pos'][i] = opt_mci.space_s[i]

            photon.pho_pos = deepcopy(opt_mci.space_s)

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

            photon.pho_radiu = [theta_sin * psi_cos, theta_sin * psi_sin, theta_cos]
            photon.pho_w = lights.data[theta_w][psi_w]


    pho_i = []
    pho_i.append(int(opt_mci.space_N[0] / 2 + photon.pho_pos[0] / opt_mci.space_d[0]))  # ix
    pho_i.append(int(opt_mci.space_N[1] / 2 + photon.pho_pos[1] / opt_mci.space_d[1]))  # iy
    pho_i.append(int(                         photon.pho_pos[2] / opt_mci.space_d[2]))  # iz
    for i in range(3):
        if pho_i[i] >= opt_mci.space_N[i]:
            pho_i[i] = opt_mci.space_N[i] - 1
        if pho_i[i] < 0:
            pho_i[i] = 0
    photon.pho_index = pho_i

    return photon


def set_tissue(photon, tissue):
    """
    根据光子的当前位置，更新当前位置组织的光学信息
    :param photon:
    :param tissue:
    :return: photon update tissue optical info
    """
    type = tissue.mat_v[photon.pho_index[2], photon.pho_index[1], photon.pho_index[0]]
    # print(type)
    photon.tis_mua = tissue.v_mua[type - 1]  # 应该是需要-1的?
    photon.tis_mus = tissue.v_mus[type - 1]  # 应该是需要-1的?
    photon.tis_g = tissue.v_g[type - 1]  # 应该是需要-1的?

    return photon


def set_step(photon):
    """
    每次光子只要没死，就都会重新设置一个随机的移动步长，并且纪录移动次数
    :param photon:
    :return:
    """
    rnd = 1 - random.random()  # 这样出来是(0, 1]的
    photon.move_sleft = -math.log(rnd)
    photon.move_cnt = photon.move_cnt + 1
    return photon






