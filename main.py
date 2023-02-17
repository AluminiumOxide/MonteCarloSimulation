import numpy as np
import math
import random
import os

from resources.arguments import Arguments,  Photon, Probes, Tissue, Lights, save_tissue
from resources.drawing import draw_mat_info

from resources.setting import set_source, set_tissue, set_step
from resources.iteration import iteration_sleft
from resources.tools import scatter_photon, roulette


def simulation(opt, photon, probes, lights, tissue, with_print=False):
    for photon_index in range(opt.photon_number):  # 最外层转光子数目
        photon.num_index = photon_index
        # 忽略判断光子数目的,有空再补

        # 重置光子位置，并且获得这个位置对应的索引，随机设置光子的入射角度
        photon = set_source(opt, photon, lights)
        # 根据光子的当前位置，更新当前位置组织的光学信息
        photon = set_tissue(photon, tissue)
        # 重置光子其他信息 未接触边界 光子存活 重置光子移动
        photon.flag_b = True
        photon.pho_status = True
        photon.move_cnt = 0

        if with_print:
            print('\nindex', photon.num_index)
            print('init position float: ', photon.pho_pos)
            print('init position index: ', photon.pho_index)

        while photon.pho_status:  # 光子只要没死就一直随机怼
            # 只要光子没死就往一个方向怼
            photon = set_step(photon)  # 设置一下怼的长度

            if with_print:
                print('with init move_sleft {}'.format(photon.move_sleft))
            # -----------------------------------------------------------------------------
            while photon.move_sleft > 0:  # 迭代一次光子移动的sleft 按照一个方向走到死
                # 劳资写完后面一定把这个flag_boundary塞到mcx命名空间里！！！
                photon, tissue = iteration_sleft(photon, tissue, opt.flag_boundary)
            # -----------------------------------------------------------------------------
            if with_print:
                print('with out move_sleft {}'.format(photon.move_sleft))

            # SPIN update angle  # 我的天，这个角度怎么还带衰减
            photon = scatter_photon(photon)

            # CHECK ROULETTE
            photon = roulette(photon)
            if with_print:
                print('photon_w {:.3f} status {}'.format(photon.pho_w, photon.pho_status))
        if photon_index % 1 == 0:

            print('index finished', photon.num_index)

    print('------------  finish ------------')

    draw_mat_info(tissue)
    # temp = opt_tissue.vox_d[0] * opt_tissue.vox_d[1] * opt_tissue.vox_d[2] * opt_mcx.photon_n
    # optical_flux = opt_tissue.mat_f / temp
    # return optical_flux



if __name__ == '__main__':
    path_input = './bin_input'
    path_output = './bin_output'
    prefix = 'oppo122'

    option = Arguments().init_mci(path_input, prefix, True, path_output)  # 读mci、写prop
    photon = Photon()
    probes = Probes()  # 四个探头的位置信息
    lights = Lights(path_input)  # 光源的data.txt

    tissue = Tissue(option, path_input, prefix)

    print(tissue.vox_N)
    print('正常进入模拟')
    optical_flux = simulation(option, photon, probes, lights, tissue)

    # save_tissue(path_output, prefix, optical_flux)


