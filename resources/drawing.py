import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import scipy.io as io


def draw_mat_info(opt_tissue):
    mat_flux = opt_tissue.mat_f
    # mat_flux = mat_flux*200
    io.savemat('./flux.mat', {'flux': mat_flux})
    # matplotlib.use('qt5agg')
    # fig = plt.figure()  # 创建画布
    # ax1, ax2, ax3 = fig.subplots(1, 3)  # 创建图表
    # ax1.imshow(mat_flux[100, :, :])
    # # ax1.imshow(np.argmax(mat_flux,axis=0))
    # ax1.set_title('xy')
    # ax2.imshow(mat_flux[:, 100, :])
    # # ax2.imshow(np.argmax(mat_flux, axis=1))
    # ax2.set_title('xz')
    # ax3.imshow(mat_flux[:, :, 100])
    # # ax3.imshow(np.argmax(mat_flux, axis=2))
    # ax3.set_title('yz')
    # # ax1.axis('off')
    # # ax2.axis('off')
    # # ax3.axis('off')
    # plt.show()


"""
np.argmax(mat_flux, axis=0)
"""
