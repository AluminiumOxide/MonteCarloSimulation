import numpy as np
import math
import random
import os

from resources.arguments import Arguments, init_light, save_tissue
from resources.drawing import draw_mat_info

from resources.setting import set_source, set_tissue, set_step
from resources.iteration import iteration_sleft
from resources.tools import scatter_photon, roulette


def simulation(opt_mcx, opt_mci, opt_probe, opt_light, opt_tissue, with_print=False):
    for photon_index in range(opt_mcx.photon_n):  # 最外层转光子数目
        opt_mcx.photon_i = photon_index
        # 忽略判断光子数目的,有空再补
        opt_mcx = set_source(opt_mcx, opt_mci, opt_light)
        opt_mcx = set_tissue(opt_mcx, opt_tissue)
        opt_mcx.flag_b = True
        opt_mcx.photon_status = True
        opt_mcx.hop_cnt = 0

        if with_print:
            print('\nindex', opt_mcx.photon_i)
            print('init position', opt_mcx.pho_pos)
            print('init pos index', opt_mcx.pho_i)

        while opt_mcx.photon_status:  # 光子迭代到死

            opt_mcx = set_step(opt_mcx)

            if with_print:
                print('with init hop_sleft {}'.format(opt_mcx.hop_sleft))

            while opt_mcx.hop_sleft > 0:  # 迭代一次光子移动的sleft 按照一个方向走到死
                # 劳资写完后面一定把这个flag_boundary塞到mcx命名空间里！！！
                opt_mcx, opt_tissue = iteration_sleft(opt_mcx, opt_tissue, opt_mci.flag_boundary)

            if with_print:
                print('with out hop_sleft {}'.format(opt_mcx.hop_sleft))

            # SPIN update angle  # 我的天，这个角度怎么还带衰减
            opt_mcx = scatter_photon(opt_mcx)

            # CHECK ROULETTE
            opt_mcx = roulette(opt_mcx)
            if with_print:
                print('photon_w {:.3f} status {}'.format(opt_mcx.photon_w, opt_mcx.photon_status))
        if photon_index % 10000 == 0:

            print('index finished', opt_mcx.photon_i)
        # print('to pos i {}'.format(opt_mcx.pho_i))
        # print('CNT {}'.format(opt_mcx.hop_cnt))
        # break  # 这个break等着删
    print('------------  finish ------------')
    draw_mat_info(opt_tissue)



    temp = opt_tissue.vox_d[0] * opt_tissue.vox_d[1] * opt_tissue.vox_d[2] * opt_mcx.photon_n
    optical_flux = opt_tissue.mat_f / temp
    return optical_flux



if __name__ == '__main__':
    path_input = './bin_input'
    path_output = './bin_output'
    prefix = 'oppo122'
    opt_mcx = Arguments().init_mcx()  # 设定需要的mcx模拟参数
    opt_mci = Arguments().init_mci(path_input, prefix, True, path_output)  # 读mci、写prop
    opt_probe = Arguments().init_probe()  # 四个探头的位置信息
    opt_light = init_light(path_input)  # 光源的data.txt

    opt_tissue = Arguments().init_tissue(opt_mci, path_input, prefix)  # 读bin
    # print(opt_probe)
    # print(opt_mci)
    print('正常进入模拟')
    optical_flux = simulation(opt_mcx, opt_mci, opt_probe, opt_light, opt_tissue)

    save_tissue(path_output, prefix, optical_flux)


