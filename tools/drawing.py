import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import scipy.io as io
import os
import math


def draw_mat_info(opt, tissue, photon_number, use_log=False):
    temp = tissue.vox_d[0] * tissue.vox_d[1] * tissue.vox_d[2] * photon_number
    flux_to_bin = tissue.mat_f / temp
    # 先转换成bin那种
    save_path = os.path.join(opt.path_output, opt.prefix + '_F.bin')
    length = flux_to_bin.shape[0] * flux_to_bin.shape[1] * flux_to_bin.shape[2]
    flux_to_bin = flux_to_bin.reshape(length)
    flux_to_bin = flux_to_bin.astype(np.float32)
    flux_to_bin.tofile(save_path)
    #
    mat_flux = tissue.mat_f
    if use_log:
        mat_flux = np.log(tissue.mat_f+1e-8)
    else:
        save_path = os.path.join(opt.path_output, opt.prefix + '_F.mat')
        io.savemat(save_path, {'flux': mat_flux})

    matplotlib.use('qt5agg')
    fig = plt.figure(dpi=320,figsize=(12,5))
    ax1, ax2, ax3 = fig.subplots(1, 3)
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
    save_path = os.path.join(opt.path_output, opt.prefix + '_F.png')
    if use_log:
        save_path = os.path.join(opt.path_output, opt.prefix + '_log_F.png')
    fig.savefig(save_path)
    plt.close()
    # plt.show()


def draw_photon_plot_3d(opt, info_list, info_weight, plot_type, title_name=''):
    list_x = []
    list_y = []
    list_z = []
    list_s = []
    fig = plt.figure(dpi=320,figsize=(5,5))
    ax = plt.axes(projection='3d')
    # received_number = math.floor(opt.photon_number/2)  # 原来的
    received_number = len(info_list)
    for i in range(received_number):
        np_list = np.array(info_list[i])
        np_weight = np.array(info_weight[i])
        np_list = np.transpose(np_list)
        np_weight = np.transpose(np_weight)*5
        list_x.append(np_list[0,:])
        list_y.append(np_list[1,:])
        list_z.append(-np_list[2,:])
        list_s.append(np_weight)

        if plot_type == 'line':
            ax.plot(list_x[i], list_y[i], list_z[i])  # 三维线图没法加权重的，不要想了
        elif plot_type == 'scatter':
            ax.scatter(list_x[i], list_y[i], list_z[i], s=list_s[i])

        # print(np.mean(np_weight))
    ax.set_title(title_name)
    # ax.legend()
    # ax.set_xlim(0, 200)
    # ax.set_ylim(0, 200)
    # ax.set_zlim(0, 200)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # plt.show()
    save_path = os.path.join(opt.path_output,plot_type+'_'+title_name+'.png')
    fig.savefig(save_path)
    plt.close()


def draw_photon_cut(opt,info_list,info_weight,plot_type, title_name=''):
    """
    :param opt: 字面意思
    :param info_list:   位置信息（xy标记位置信息，z标记透明度
    :param info_weight:   权重信息  标记大小
    :param num:
    :return:
    """
    list_x = []
    list_y = []
    list_z = []
    list_s = []

    matplotlib.use('qt5agg')
    plt.figure(dpi=320,figsize=(20,19))  # x 320*10 y 320*9
    plt.subplot(2, 2, 2)
    plt.title(title_name+'_cut_X_vs_Z' ,size=36)
    plt.xlim([-0.3,0.3])
    plt.ylim([0.0, 0.6])
    plt.xlabel('x (cm)',size=36)  # 这个可以不要
    plt.ylabel('z (cm)' ,size=36)
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major',linewidth =2.5)
    plt.subplot(2, 2, 3)
    plt.title(title_name+'_cut_Z_vs_Y' ,size=36)
    plt.xlim([0.6,0.0])  # 没错,是反的
    plt.ylim([-0.3,0.3])
    plt.xlabel('z (cm)' ,size=36)
    plt.ylabel('y (cm)' ,size=36)
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major',linewidth =2.5)
    plt.subplot(2, 2, 4)
    plt.title(title_name+'_cut_X_vs_Y' ,size=36)
    plt.xlim([-0.3,0.3])
    plt.ylim([-0.3,0.3])
    plt.xlabel('x (cm)' ,size=36)
    plt.ylabel('y (cm)' ,size=36)   # 这个可以不要
    plt.minorticks_on()
    plt.grid(which='minor')
    plt.grid(which='major',linewidth =2.5)

    # received_number = math.floor(opt.photon_number/2)
    received_number = len(info_list)
    for i in range(received_number):
        np_list = np.array(info_list[i])
        np_weight = np.array(info_weight[i])
        np_list = np.transpose(np_list)
        np_weight = np.transpose(np_weight)*5
        list_x.append(np_list[0,:])
        list_y.append(np_list[1,:])
        list_z.append(np_list[2,:])
        list_s.append(np_weight)

        list_alpha = list_s
        # 我谢谢你 ValueError: alpha must be between 0 and 1, inclusive, but min is -45, max is -45
        if list_alpha[i].max()-list_alpha[i].min():  # 后面可能会出现除0的问题
            list_alpha_norm = 0.01 + 0.988 * (list_alpha[i]-list_alpha[i].min())/(list_alpha[i].max() - list_alpha[i].min())
        else:
            list_alpha_norm = np.zeros(list_alpha[i].shape)+0.5
        # ValueError: alpha must be between 0 and 1, inclusive, but min is nan, max is nan


        if plot_type == 'line':
            plt.subplot(2, 2, 2)
            plt.plot(list_x[i], list_z[i])  # 三维线图没法加权重的，不要想了
            plt.subplot(2, 2, 3)
            plt.plot(list_z[i], list_y[i])  # 三维线图没法加权重的，不要想了
            plt.subplot(2, 2, 4)
            plt.plot(list_x[i], list_y[i])  # 三维线图没法加权重的，不要想了

        elif plot_type == 'scatter':
            # plt.scatter(list_x[i],list_z[i],s=list_y[i],alpha=list_alpha_norm,linewidths=0)
            plt.subplot(2, 2, 2)
            plt.scatter(list_x[i],list_z[i],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)
            plt.subplot(2, 2, 3)
            plt.scatter(list_z[i],list_y[i],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)
            plt.subplot(2, 2, 4)
            plt.scatter(list_x[i],list_y[i],s=list_alpha_norm*list_alpha_norm*30,alpha=list_alpha_norm,linewidths=0)

            # if list_x[i].shape[0] - 2 >= 0:
            #     list_x[i] = list_x[i][:int(list_x[i].shape[0]-2)]
            #     list_y[i] = list_y[i][:int(list_y[i].shape[0]-2)]
            #     list_z[i] = list_z[i][:int(list_z[i].shape[0]-2)]
            plt.subplot(2, 2, 2)
            plt.plot(list_x[i], list_z[i],lw=1, alpha=0.1)
            plt.subplot(2, 2, 3)
            plt.plot(list_z[i], list_y[i], lw=1, alpha=0.1)
            plt.subplot(2, 2, 4)
            plt.plot(list_x[i], list_y[i], lw=1, alpha=0.1)

        # break

    # plt.show()
    save_path = os.path.join(opt.path_output,'cut_'+plot_type+'_'+title_name+'.png')
    plt.savefig(save_path)
