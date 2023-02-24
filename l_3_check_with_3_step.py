import scipy.io as io
import os

import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from models import *
from tools.drawing import draw_mat_info, draw_photon_plot_3d, draw_photon_cut

from copy import deepcopy
from collections import Counter  # 我谢谢你


def simple_mat_info(opt, mat_info, photon_number, append='Alu'):
    # temp = mat_info.shape[0] * mat_info.shape[1] * mat_info.shape[2] * photon_number
    # mat_info_bin = mat_info / temp
    #
    # mat_flux = mat_info_bin
    mat_flux = np.log(mat_info + 1e-8)
    save_path = os.path.join(opt.path_output, opt.prefix + '_' + append + '_F.mat')
    io.savemat(save_path, {'flux': mat_flux})

    matplotlib.use('qt5agg')
    fig = plt.figure(dpi=320, figsize=(5, 12))
    ax1, ax2, ax3 = fig.subplots(3, 1)
    ax1.imshow(mat_flux[100, :, :])
    # ax1.imshow(np.argmax(mat_flux,axis=0))
    ax1.set_title('xy')
    ax2.imshow(mat_flux[:, 100, :])
    # ax2.imshow(np.argmax(mat_flux, axis=1))
    ax2.set_title('xz')
    ax3.imshow(mat_flux[:, :, 100])
    # ax3.imshow(np.argmax(mat_flux, axis=2))
    ax3.set_title('yz')
    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')
    # fig.colorbar(mappable=None)
    save_path = os.path.join(opt.path_output, opt.prefix + '_' + append + '_F.png')
    # if use_log:
    #     save_path = os.path.join(opt.path_output, opt.prefix + '_log_F.png')
    fig.savefig(save_path)
    plt.close()


def simple_photon_route(opt, info_list, info_weight, check_list, choose=1, plot_type='scatter', title_name=''):
    list_x, list_y, list_z, list_s = [], [], [], []
    adjust_check_list = check_list[:, 0] * 4 + check_list[:, 1] * 2 + check_list[:, 2]
    check_index = np.where(adjust_check_list == choose)[0]

    matplotlib.use('qt5agg')
    fig = plt.figure(dpi=320, figsize=(20, 20))  # x 320*10 y 320*9
    ax = fig.add_subplot(221, projection='3d')
    # ax.set_title(title_name)
    ax.set_xlabel('X (cm)', size=16)
    ax.set_ylabel('Y (cm)', size=16)
    ax.set_zlabel('Z (cm)', size=16)
    ax.set_zlim([0.6, 0.0])

    plt.subplot(2, 2, 2)
    plt.title(title_name + '_cut_X_vs_Z', size=36)
    plt.xlim([-0.3, 0.3])
    plt.ylim([0.0, 0.6])
    plt.xlabel('x (cm)', size=36)  # 这个可以不要
    plt.ylabel('z (cm)', size=36)
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major', linewidth=2.5)
    plt.subplot(2, 2, 3)
    plt.title(title_name + '_cut_Z_vs_Y', size=36)
    plt.xlim([0.6, 0.0])  # 没错,是反的
    plt.ylim([-0.3, 0.3])
    plt.xlabel('z (cm)', size=36)
    plt.ylabel('y (cm)', size=36)
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major', linewidth=2.5)
    plt.subplot(2, 2, 4)
    plt.title(title_name + '_cut_X_vs_Y', size=36)
    plt.xlim([-0.3, 0.3])
    plt.ylim([-0.3, 0.3])
    plt.xlabel('x (cm)', size=36)
    plt.ylabel('y (cm)', size=36)  # 这个可以不要
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major', linewidth=2.5)

    for i in check_index:      # received_number = len(info_list)
        np_list = np.transpose(info_list[i])  # eg [3,39] > transpose > [39,3]
        np_weight = np.transpose(info_weight[i]) * 5  # same
        list_x.append(np_list[0,:])  # [39,]
        list_y.append(np_list[1,:])
        list_z.append(np_list[2,:])
        list_s.append(np_weight)

        list_alpha = list_s

        if list_alpha[-1].max()-list_alpha[-1].min():  # 后面可能会出现除0的问题
            list_alpha_norm = 0.01 + 0.988 * (list_alpha[-1]-list_alpha[-1].min())/(list_alpha[-1].max() - list_alpha[-1].min())
        else:
            list_alpha_norm = np.zeros(list_alpha[-1].shape) + 0.5

        if plot_type == 'line':
            plt.subplot(2, 2, 1)
            plt.plot(list_x[-1], list_y[-1], list_z[-1])
            plt.subplot(2, 2, 2)
            plt.plot(list_x[-1], list_z[-1])  # 线图没法加权重的，不要想了
            plt.subplot(2, 2, 3)
            plt.plot(list_z[-1], list_y[-1])
            plt.subplot(2, 2, 4)
            plt.plot(list_x[-1], list_y[-1])

        elif plot_type == 'scatter':
            ax.scatter(list_x[-1], list_y[-1], list_z[-1], s=list_s[-1])
            plt.subplot(2, 2, 2)
            plt.scatter(list_x[-1],list_z[-1],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)
            plt.subplot(2, 2, 3)
            plt.scatter(list_z[-1],list_y[-1],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)
            plt.subplot(2, 2, 4)
            plt.scatter(list_x[-1],list_y[-1],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)
            # if list_x[-1].shape[0] - 2 >= 0:
            #     list_x[-1] = list_x[-1][:int(list_x[-1].shape[0]-2)]
            #     list_y[-1] = list_y[-1][:int(list_y[-1].shape[0]-2)]
            #     list_z[-1] = list_z[-1][:int(list_z[-1].shape[0]-2)]

            ax.plot(list_x[-1], list_y[-1], list_z[-1],lw=1, alpha=0.1)
            plt.subplot(2, 2, 2)
            plt.plot(list_x[-1], list_z[-1],lw=1, alpha=0.1)
            plt.subplot(2, 2, 3)
            plt.plot(list_z[-1], list_y[-1], lw=1, alpha=0.1)
            plt.subplot(2, 2, 4)
            plt.plot(list_x[-1], list_y[-1], lw=1, alpha=0.1)

    save_path = os.path.join(opt.path_output,'cut_'+plot_type+'_'+title_name+'.png')
    plt.savefig(save_path)


def simulation(opt, photon, probe, light, tissue, with_print=False):
    d_total_pho_list, d_total_idx_list, d_total_weight, d_check_list = [], [], [], []
    mat_f_mask_0 = tissue.mat_f.view()  # 原有的什么都加
    mat_f_mask_1 = tissue.mat_f.view()  # 加入check1
    mat_f_mask_2 = tissue.mat_f.view()  # 加入check2
    mat_f_mask_3 = tissue.mat_f.view()  # 加入check3
    count_1, count_2, count_3 = 0, 0, 0
    for photon_index in range(opt.photon_number):  # 最外层转光子数目
        photon.num_index = photon_index
        # 忽略判断光子数目的,有空再补
        photon.set_source(opt, light)
        photon.set_tissue(tissue,with_buffer=True)
        photon.set_others()

        d_pho_list, d_idx_list, d_weight = [], [], []
        while photon.pho_status:  # 光子只要没死就一直随机怼

            d_pho_list.append(photon.pho_pos)
            d_weight.append(photon.pho_w)
            photon.set_step()  # 运动长度
            while photon.move_sleft > 0:  # 迭代一次光子移动的sleft 按照一个方向走到死
                # 理论上在这, 但是可能会出问题？
                photon.iteration_sleft(tissue, opt.flag_boundary)

            d_float = deepcopy(photon.pho_index)
            d_idx_list.append(d_float)

            photon.change_direction()  # SPIN update angle
            photon.roulette()  # CHECK ROULETTE

        # tissue内mat_r没有过使用，这东西每次copy一份上个一个光子的mat_f # 追加在 set_tissue()里
        [check_1_from_glass, check_2_to_glass, check_3_in_probe] = probe.judge(d_pho_list, info_dist=True)
        d_check_list.append([check_1_from_glass, check_2_to_glass, check_3_in_probe])
        mat_f_mask_0 = mat_f_mask_0 + tissue.mat_f
        if check_1_from_glass:
            mat_f_mask_1 = mat_f_mask_1 + tissue.mat_f
            count_1 += 1
        if check_1_from_glass and check_2_to_glass:
            mat_f_mask_2 = mat_f_mask_2 + tissue.mat_f
            count_2 += 1
        if check_1_from_glass and check_2_to_glass and check_3_in_probe:
            mat_f_mask_3 = mat_f_mask_3 + tissue.mat_f
            count_3 += 1
        tissue.mat_f = np.zeros(shape=(200, 200, 200))  # 每次都重置一遍 劳资直接出这些储存空间!
        if photon_index % 100 == 0:
            print(
                'Run {}/{} photon : with {} photon from center glass {} scattered from tissue to probe glass {} received by probe.'.format(
                    photon_index, opt.photon_number, count_1, count_2, count_3))
        d_total_pho_list.append(d_pho_list)
        d_total_idx_list.append(d_idx_list)
        d_total_weight.append(d_weight)
        # else:               # 没有满足条件的, mat_f 退回 mat_r,并且不加
        #     tissue.mat_f = deepcopy(tissue.mat_r)  # tissue.mat_r.view()

    print('------------  finish ------------')
    print('Total photon number is: {} with {} photon from center glass {} scattered from tissue to probe glass'
          ' {} received by probe.'.format(opt.photon_number, count_1, count_2, count_3))

    save_path = os.path.join(opt.path_output, opt.prefix + '_infos_list.mat')  #
    io.savemat(save_path, {'check_list': d_check_list,
                           'pho': d_total_pho_list,
                           'idx': d_total_idx_list,
                           'weight': d_total_weight})

    # simple_mat_info(option, tissue.mat_f, opt.photon_number,append='Without_mask')  # 这个忽略，加了重置项，已经没用了
    simple_mat_info(option, mat_f_mask_0, opt.photon_number, append='Without_mask')
    simple_mat_info(option, mat_f_mask_1, opt.photon_number, append='with_mask_1')
    simple_mat_info(option, mat_f_mask_2, opt.photon_number, append='with_mask_2')
    simple_mat_info(option, mat_f_mask_3, opt.photon_number, append='with_mask_3')


if __name__ == '__main__':
    option = Argument().init_mci()  # read mci、 write prop
    photon = Photon()
    probe = Probe_list()  # 4 probe location
    light = Light(option)  # data.txt
    tissue = Tissue(option)

    print('Specialized contrast mask')
    simulation(option, photon, probe, light, tissue)  # --------- MAIN SIMULATION STEP ---------

    save_path = os.path.join(option.path_output, option.prefix + '_infos_list.mat')
    hook_mat = io.loadmat(save_path)
    check_list = hook_mat['check_list']
    pho_list = hook_mat['pho'][0]
    idx_list = hook_mat['idx'][0]
    weight_list = hook_mat['weight'][0]

    # check_list = check_list[0:10000]
    # pho_list = pho_list[0:10000]
    # idx_list = idx_list[0:10000]
    # weight_list = weight_list[0:10000]

    simple_photon_route(option, pho_list, weight_list, check_list, choose=0, plot_type='scatter', title_name='0')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=1, plot_type='scatter', title_name='1')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=2, plot_type='scatter', title_name='2')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=3, plot_type='scatter', title_name='3')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=4, plot_type='scatter', title_name='4')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=5, plot_type='scatter', title_name='5')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=6, plot_type='scatter', title_name='6')
    simple_photon_route(option, pho_list, weight_list, check_list, choose=7, plot_type='scatter', title_name='7')

    status = []
    for statu in check_list:
        status.append(statu[0] * 4 + statu[1] * 2 + statu[2])
    count_statu = Counter(status)
    print(count_statu)






