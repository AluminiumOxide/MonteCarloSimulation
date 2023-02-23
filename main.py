from models import *
from tools.drawing import draw_mat_info, draw_photon_plot_3d, draw_photon_cut

from copy import deepcopy

def judge(probe,pho_list):
    """
    :param probe: 终于用上的光学探头位置
    :param pho_list:  这个光子的传播路径
    :return: Bool 表示是否达到光学探头  如果条件满足 返回true
    """
    p1 = probe.p_1
    [prob_x,prob_y,prob_z] = p1.position
    [width, height] = p1.scale
    half_height = height/2

    in_probe = False
    for position in pho_list:
        pho_x,pho_y,pho_z = abs(position)  # 当前位置取模，相当于对称来一遍,两个压缩成一个
        # prob_x <= pho_x and pho_x <= (prob_x + width)
        # 0 <= pho_y and pho_y <= half_height
        # 0 <= pho_z and pho_z <= prob_z
        if prob_x <= pho_x and pho_x <= (prob_x + width) and pho_y <= half_height and pho_z <= prob_z:
            in_probe = True
            break
        # 同理需要考虑xy互换的情况
        if prob_x <= pho_y and pho_y <= (prob_x + width) and pho_x <= half_height:
            in_probe = True
            break
    """
        在当前的基础上，增加判断当高度比 prob_z 小的时候
            x和y计算到玻璃圆心的距离
            如果距离大于半径
                直接抛弃
    """
    [glass_center, glass_bias,glass_radiu] = probe.light_1  # 正常拿
    flag_1 = True # False
    flag_2 = False
    # for position in pho_list:  # 这段没法加，第一个发射的位置不会算到光子路径里，因为设置空气介质纯不吸收，相当于第一个点就是糊到组织体上的
    #     pho_x, pho_y, pho_z = abs(position)
    #     if pho_z <= prob_z:  # 当位于组织体上面时
    #         radiu0_2 = pho_x*pho_x+pho_y*pho_y
    #         if radiu0_2 <= glass_center*glass_center:  # 如果存在经过光源镜片的点
    #             flag_1 = True
    #             break
    for position in pho_list:
        pho_x, pho_y, pho_z = abs(position)
        if pho_z <= prob_z:  # 当位于组织体上面时
            l11 = pho_x-glass_bias
            l12 = pho_x+glass_bias
            l21 = pho_y-glass_bias
            l22 = pho_y+glass_bias
            radiu1_2 = l11 * l11 + pho_y * pho_y
            radiu2_2 = l12 * l12 + pho_y * pho_y
            radiu3_2 = pho_x * pho_x + l21 * l21
            radiu4_2 = pho_x * pho_x + l22 * l22
            radiug = glass_radiu * glass_radiu
            if radiu1_2 <= radiug or radiu2_2 <= radiug or radiu3_2 <= radiug or radiu4_2 <= radiug:
                # 如果这个里面有一个比这个半径小，那就说明是有过镜片的地方，理论是过探头镜片的
                flag_2 = True
                break
    in_glass = False
    if flag_1 and flag_2:  # 如果这俩都满足，那就说明是经过两个镜片的
        in_glass = True

    set_true = in_probe and in_glass
    return set_true


def simulation(opt, photon, probe, light, tissue, with_print=False):
    d_total_pho_list, d_total_idx_list, d_total_weight = [], [], []
    float_list = []
    for photon_index in range(opt.photon_number):  # 最外层转光子数目
        photon.num_index = photon_index

        # 忽略判断光子数目的,有空再补
        photon.set_source(opt, light)
        photon.set_tissue(tissue)  #
        photon.set_others()

        d_pho_list, d_idx_list, d_weight = [], [], []

        while photon.pho_status:  # 光子只要没死就一直随机怼

            d_pho_list.append(photon.pho_pos)
            d_weight.append(photon.pho_w)
            photon.set_step()  # 运动长度
            while photon.move_sleft > 0:  # 迭代一次光子移动的sleft 按照一个方向走到死
                # 理论上在这, 但是可能会出问题？
                #
                photon.iteration_sleft(tissue, opt.flag_boundary)

            d_float = deepcopy(photon.pho_index)
            d_idx_list.append(d_float)

            photon.change_direction()  # SPIN update angle
            photon.roulette()  # CHECK ROULETTE
        if photon_index % 1000 == 0:
            print('index finished', photon.num_index)
            pass
        # tissue内mat_r没有过使用，这东西每次copy一份上个一个光子的mat_f # 追加在 set_tissue()里
        # 该轮光子路径中，如果有满足条件的，保留
        dash_to_prob = judge(probe, d_pho_list)   # judge(probe, d_pho_list) True
        if dash_to_prob:
            d_total_pho_list.append(d_pho_list)
            d_total_idx_list.append(d_idx_list)
            d_total_weight.append(d_weight)
        # 没有满足条件的, mat_f 退回 mat_r,并且不加
        else:
            tissue.mat_f = tissue.mat_r.view()

    print('------------  finish ------------')
    print('Total photon number is: {} with {} photon received'.format(opt.photon_number,len(d_total_pho_list)))
    draw_mat_info(option, tissue, opt.photon_number)
    draw_mat_info(option, tissue, opt.photon_number, use_log=True)

    draw_photon_plot_3d(opt, d_total_pho_list, d_total_weight, 'scatter', 'position')
    draw_photon_plot_3d(opt, d_total_idx_list, d_total_weight, 'scatter', 'index')
    draw_photon_plot_3d(opt, d_total_pho_list, d_total_weight, 'line', 'position')
    draw_photon_plot_3d(opt, d_total_idx_list, d_total_weight, 'line', 'index')

    draw_photon_cut(opt, d_total_pho_list, d_total_weight, 'scatter', 'position')
    draw_photon_cut(opt, d_total_pho_list, d_total_weight, 'line', 'position')


if __name__ == '__main__':
    option = Argument().init_mci()  # read mci、 write prop
    photon = Photon()
    probe = Probe_list()  # 4 probe location
    light = Light(option)  # data.txt
    tissue = Tissue(option)

    print('Load info success, Begin simulation')
    simulation(option, photon, probe, light, tissue)
