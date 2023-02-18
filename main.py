from models import *
from tools.drawing import draw_mat_info, draw_photon_plot_3d, draw_photon_cut

from copy import deepcopy
import time


def simulation(opt, photon, probe, light, tissue, with_print=False):
    d_total_pho_list = []
    d_total_idx_list = []
    d_total_weight = []
    for photon_index in range(opt.photon_number):  # 最外层转光子数目
        photon.num_index = photon_index
        # 忽略判断光子数目的,有空再补
        photon.set_source(opt, light)
        photon.set_tissue(tissue)
        photon.set_others()

        d_pho_list = []
        d_idx_list = []
        d_weight = []
        print('----------------------------------------------------------------------------')
        while photon.pho_status:  # 光子只要没死就一直随机怼
            d_pho_list.append(photon.pho_pos)

            d_weight.append(photon.pho_w)
            photon.set_step()  # 设置运动长度
            while photon.move_sleft > 0:  # 迭代一次光子移动的sleft 按照一个方向走到死
                # print(photon.pho_index)
                photon.iteration_sleft(tissue, opt.flag_boundary)

            d_float = deepcopy(photon.pho_index)  # 我谢谢你，浅复制??????????????????????????????????????????????????????
            print(d_float)
            d_idx_list.append(d_float)

            photon.change_direction()  # SPIN update angle
            # photon.roulette()  # CHECK ROULETTE
        if photon_index % 1000 == 0:
            print('index finished', photon.num_index)
            pass

        d_total_pho_list.append(d_pho_list)
        d_total_idx_list.append(d_idx_list)
        d_total_weight.append(d_weight)
        # break
    print('------------  finish ------------')

    draw_mat_info(option, tissue, opt.photon_number)

    draw_photon_plot_3d(opt, d_total_pho_list, d_total_weight, 'scatter', 'position')
    draw_photon_plot_3d(opt, d_total_idx_list, d_total_weight, 'scatter', 'index')
    draw_photon_plot_3d(opt, d_total_pho_list, d_total_weight, 'line', 'position')
    draw_photon_plot_3d(opt, d_total_idx_list, d_total_weight, 'line','index')

    draw_photon_cut(opt, d_total_pho_list, d_total_weight, 'scatter', 'position')
    draw_photon_cut(opt, d_total_pho_list, d_total_weight, 'line', 'position')
    # draw_photon_cut(opt, d_total_idx_list, d_total_weight, 'index')


if __name__ == '__main__':
    path_input = './bin_input'
    path_output = './bin_output'
    prefix = 'oppo122'

    option = Argument().init_mci()  # 读mci、写prop
    photon = Photon()
    probe = Probe_list()  # 四个探头的位置信息
    light = Light(option)  # 光源的data.txt

    tissue = Tissue(option)

    print('网格 ',tissue.vox_N)
    print('正常进入模拟')

    simulation(option, photon, probe, light, tissue)
    pass
    # save_tissue(path_output, prefix, optical_flux)


