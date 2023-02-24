import math

import numpy as np


class Probe_list:
    def __init__(self):
        self.p_position = np.array([0.05, 0, 0.122])  # position : [x,y,hh]
        self.p_scale = np.array([0.02, 0.036])  # scale : [width,height]

        self.glass_light = np.array([0.03, 0.14])  # center_radius, center_height
        self.glass_probe = np.array([0.02, 0.07, 0.14])  # radius, bias, height

    def judge(self, pho_list, info_dist=False):
        """
        :self: 终于用上的光学探头位置
        :param pho_list:  这个光子的传播路径
        :info_dist: 输出的判断信息是否是分开的
        :return: Bool 表示是否达到光学探头  如果条件满足 返回true
        """
        [prob_x, prob_y, prob_z] = self.p_position
        [width, height] = self.p_scale
        [center_r, center_z] = self.glass_light
        [glass_r, glass_b, glass_z] = self.glass_probe  # 现在center_z和glass_z相同，以后可以调
        half_height = height / 2

        # step_1 检测有没有正常向下打  check_1_from_glass = True 正常进入 False 打偏  检测入射角度直接改成检测第一个点的xy坐标在不在玻璃片和入射点的延长线交接内
        pho_x, pho_y, pho_z = abs(pho_list[0])  # 仅检测第一个光子的位置
        pho_radiu = math.sqrt(pho_x * pho_x + pho_y * pho_y)
        move_z = pho_z - prob_z
        check_r = glass_r
        check_z = center_z - prob_z
        check_1_from_glass = check_r / check_z >= pho_radiu / move_z

        # step_2 检测有没有从探头前的镜片入射
        check_2_to_glass = False
        for position in pho_list:
            pho_x, pho_y, pho_z = abs(position)
            if pho_z <= glass_z:  # 当位于组织体上面时  # 我不知道这么写是不是太冗余了，直接两个都取正判断一个行不行？
                l11 = pho_x - glass_b
                l12 = pho_x + glass_b
                l21 = pho_y - glass_b
                l22 = pho_y + glass_b
                radiu1 = l11 * l11 + pho_y * pho_y
                radiu2 = l12 * l12 + pho_y * pho_y
                radiu3 = pho_x * pho_x + l21 * l21
                radiu4 = pho_x * pho_x + l22 * l22
                radiug = glass_r * glass_r
                if radiu1 <= radiug or radiu2 <= radiug or radiu3 <= radiug or radiu4 <= radiug:
                    check_2_to_glass = True  # 如果这个里面有一个比这个半径小，那就说明是有过镜片的地方，理论是过探头镜片的
                    break

        # step3 检测有没有打到探头上
        check_3_in_probe = False
        for position in pho_list:
            pho_x, pho_y, pho_z = abs(position)  # 当前位置取模，相当于对称来一遍,两个压缩成一个
            # prob_x <= pho_x and pho_x <= (prob_x + width)
            # 0 <= pho_y and pho_y <= half_height
            # 0 <= pho_z and pho_z <= prob_z
            # if prob_x <= pho_x and pho_x <= (prob_x + width) and pho_y <= half_height and pho_z <= prob_z:
            if prob_x <= pho_x and pho_x <= (prob_x + width) and pho_y <= half_height and 0.1 <= pho_z and pho_z <= prob_z:
                check_3_in_probe = True
                break
            # 同理需要考虑xy互换的情况
            if prob_x <= pho_y and pho_y <= (prob_x + width) and pho_x <= half_height:
                check_3_in_probe = True
                break
        if info_dist:
            return [check_1_from_glass,check_2_to_glass,check_3_in_probe]
        set_true = check_1_from_glass and check_2_to_glass and check_3_in_probe
        return set_true
