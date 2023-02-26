import scipy.io as io
import os
import numpy as np
import math

"""  
以下代码注释的OOC量爆炸，无关人员请赶紧撤离，如果您掘的看不下去，请赶紧删除这个项目，因为这个脚本的注释真的很抽象
我TM不清楚为什么要加载spectralLIB.mat！！！谁TM来解释解释，把数据都导入了还插值是什么意思！解释解释！！！我都插值了你还不用！！！
好吧，这个脚本用来产<>_T.bin没别的什么用
"""
def get_tissue_with_wave_length():  # 待问，这块我真的很需要导入文件吗？
    """
        # 加载为一个长度为7的字典，下面储存[701,1]的ndarray 不过这些处理真的有用吗？你后面都没用，甚至这个函数都没用上
        save_path = os.path.join(os.getcwd(), 'bin_input','spectralLIB.mat')
        wave = 532
        hook_mat = io.loadmat(save_path)
        wave_list = hook_mat['nmLIB'].squeeze()
        mua_oxy = hook_mat['muaoxy'].squeeze()
        mua_deoxy = hook_mat['muadeoxy'].squeeze()
        mua_water = hook_mat['muawater'].squeeze()
        mua_mel  = hook_mat['muamel'].squeeze()
        mus_p = hook_mat['musp'].squeeze()
        inter_list = [np.interp(wave,wave_list,mua_oxy),
                      np.interp(wave,wave_list,mua_deoxy),
                      np.interp(wave,wave_list,mua_water),
                      np.interp(wave,wave_list,mua_mel)]
    """
    # 谢谢上面的代码，完全没用！下面开始似乎正常的干活 不过还是没用上（那之前写这玩意干啥啊！
    tissue_info = {"name":[],"mua":[],"mus":[],"g":[]}
    tissue_info["name"].extend(['air','skin','fat','bone','tiss','xue1','xue2','muscle','standard'])
    tissue_info["mua"].append( [0.0  ,1.6   ,0.09 ,0.5   ,1.4   ,4.87  ,2.65  ,0.52    ,1.0       ])
    tissue_info["mus"].append( [0.0  ,223   ,121  ,280   ,88    ,509   ,1413  ,73.56   ,100       ])
    tissue_info["g"].append(   [1.0  ,0.9   ,0.9  ,0.9   ,0.96  ,0.995 ,0.99  ,0.93    ,0.9       ])
    return tissue_info

if __name__ == '__main__':
    tissue_info = get_tissue_with_wave_length()  # 好不容易取出来后面又不用是什么意思！还是说需要蓝色药丸？

    #忽略上面的那个函数，注释掉都没事
    mat_T = np.ones((200, 200, 200),dtype=np.uint8)
    for i in range(200):
        for j in range(200):
            # 手腕
            dd = math.sqrt(((i - 100) / 83) ** 2 + ((j - 100) / 50) ** 2)
            if dd < 1:
                mat_T[i, j, :] = 2
            # 皮肤
            dd = math.sqrt(((i - 100) / 78) ** 2 + ((j - 100) / 45) ** 2)
            if dd < 1:
                mat_T[i, j, :] = 3
            # 骨头
            dd_1 = math.sqrt(((i - 100) / 17) ** 2 + ((j - 100) / 17) ** 2)
            dd_2 = math.sqrt(((i - 152) / 12) ** 2 + ((j - 89) / 12) ** 2)
            dd_3 = math.sqrt(((i - 60) / 25) ** 2 + ((j - 108) / 25) ** 2)
            if dd_1 < 1 or dd_2 < 1 or (dd_3 < 1 and i < 70):
                mat_T[i, j, :] = 4
            # 血管
            dd_1 = math.sqrt(((i - 47) / 3) ** 2 + ((j - 75) / 3) ** 2)
            dd_2 = math.sqrt(((i - 30) / 3) ** 2 + ((j - 100) / 3) ** 2)
            if dd_1 < 1 or dd_2 < 1:
                mat_T[i, j, :] = 6
            dd = math.sqrt(((i - 34) / 3) ** 2 + ((j - 120) / 3) ** 2)
            if dd < 1 and i < 70:
                mat_T[i, j, :] = 7

    # 骨头
    mat_T[120:154,106:130,:]=4
    mat_T[81:115,123:133,:]=4
    # 软腔
    mat_T[60: 140, 66: 81,:]=5
    # 血管
    mat_T[147:151,70:74,:]=6
    mat_T[72:76,133:137,:]=6  # 94:98,136:140,:
    mat_T[163:167,96:100,:]=6
    mat_T[94:98,136:140,:]=7
    mat_T[119:123,134:138,:]=7
    mat_T[168:172,107:111,:]=7
    # 肌肉束
    mat_T[69: 73, 74: 78,:]=8
    mat_T[80: 84, 75: 79,:]=8
    mat_T[91: 97, 73: 79,:]=8
    mat_T[105: 108, 68: 80,:]=8
    mat_T[112: 125, 68: 71,:]=8
    mat_T[112: 125, 76: 79,:]=8
    mat_T[128: 138, 69: 78,:]=8

    mat_T[160: 164, 103: 107,:]=8
    mat_T[162: 166, 114: 118,:]=8
    mat_T[167: 171, 88: 92,:]=8
    mat_T[170: 174, 97: 101,:]=8  # 168:172,107:111,:

    mat_T[82: 86, 137: 141,:]=8  # 72:76,133:137,:
    mat_T[106: 110, 138: 142,:]=8  # 94:98,136:140,:
    mat_T[129: 133, 135: 139,:]=8  # 119:123,134:138,:
    mat_T[36: 40, 80: 84,:]=8
    mat_T[27: 31, 89: 93,:]=8
    mat_T[29: 33, 107: 111,:]=8
    mat_T[48: 52, 79: 83,:]=8
    # 相当于之前的文件如果设置xyz是 180 200 220 现在mat_T = [200,180,220]
    mat_T = mat_T.transpose((2,0,1))  # 对应 282 T=shiftdim(T,2)   也就是这么转完，就是[220,200,180]的了
    mat_T = np.flip(mat_T, axis = 2)   # 然后还有个翻转X轴，聪哥，谢谢您！

    if 1:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.imshow(mat_T[100, :, :])
        plt.show()
        plt.close()

    length = mat_T.shape[0] * mat_T.shape[1] * mat_T.shape[2]
    mat_T = mat_T.reshape(length,order='F')  # 从1维开始排列啊！不愧是你
    # flux_to_bin = flux_to_bin.astype(np.int8)
    save_path = os.path.join(os.getcwd(), 'bin_input', 'oppo122_T.bin')
    mat_T.tofile(save_path)

