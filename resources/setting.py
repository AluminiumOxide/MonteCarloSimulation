import random
import math


def set_source(opt_mcx, opt_mci, opt_light):
    """
    判断flag，返回位置和角度信息
    """
    if opt_mci.flag_launch == 1:
        for i in range(3):
            opt_mcx.pho_pos[i] = opt_mci.space_s[i]
            opt_mcx.pho_u[i] = opt_mci.space_u0[i]
    else:
        if opt_mci.flag_mc == 0:
            # opt_mcx.pho_pos = opt_mci.space_s  # 这里先设置成这个  # 怪！为什么会干扰
            for i in range(3):
                opt_mcx.pho_pos[i] = opt_mci.space_s[i]

            theta_r = random.uniform(0, 90.49)  # 纬角 = 0.5π*rand  uniform是左闭右闭
            theta_w = round(theta_r)
            theta_cos = math.cos(theta_r / 180 * math.pi)
            theta_sin = math.sqrt(1.0 - theta_cos * theta_cos)

            psi_r = random.uniform(0, 360)  # 经角 = 2π*rand  uniform是左闭右闭
            psi_w = math.floor(psi_r)  # 没办法,索引只有0~359
            psi_cos = math.cos(psi_r / 180 * math.pi)
            if psi_r < 180:
                psi_sin = math.sqrt(1.0 - psi_cos * psi_cos)
            else:
                psi_sin = -1 * math.sqrt(1.0 - psi_cos * psi_cos)

            opt_mcx.pho_u = [theta_sin * psi_cos, theta_sin * psi_sin, theta_cos]
            opt_mcx.photon_w = opt_light[theta_w][psi_w]

            # if opt_mcx.pho_u[0] * opt_mcx.pho_u[0] + opt_mcx.pho_u[1] * opt_mcx.pho_u[1] + opt_mcx.pho_u[2] * opt_mcx.pho_u[2] == 1:
            #     print('check')
            # else:
            #     print('not check')
    pho_i = []
    pho_i.append(int(opt_mci.space_N[0] / 2 + opt_mcx.pho_pos[0] / opt_mci.space_d[0]))  # ix
    pho_i.append(int(opt_mci.space_N[1] / 2 + opt_mcx.pho_pos[1] / opt_mci.space_d[1]))  # iy
    pho_i.append(int(opt_mcx.pho_pos[2] / opt_mci.space_d[2]))  # iz
    for i in range(3):
        if pho_i[i] >= opt_mci.space_N[i]:
            pho_i[i] = opt_mci.space_N[i] - 1
        if pho_i[i] < 0:
            pho_i[i] = 0
    opt_mcx.pho_i = pho_i

    return opt_mcx


def set_tissue(opt_mcx, opt_tissue):
    type = opt_tissue.mat_v[opt_mcx.pho_i[2], opt_mcx.pho_i[1], opt_mcx.pho_i[0]]
    # print(type)
    opt_mcx.tis_mua = opt_tissue.v_mua[type - 1]  # 应该是需要-1的?
    opt_mcx.tis_mus = opt_tissue.v_mus[type - 1]  # 应该是需要-1的?
    opt_mcx.tis_g = opt_tissue.v_g[type - 1]  # 应该是需要-1的?

    return opt_mcx


def set_step(opt_mcx):
    rnd = 1 - random.random()  # 这样出来是(0, 1]的
    opt_mcx.hop_sleft = -math.log(rnd)
    opt_mcx.hop_cnt = opt_mcx.hop_cnt + 1
    return opt_mcx






