import math
import copy

def same_voxel(space_1, space_2, bin_size):
    x1,y1,z1 = space_1  # opt_mcx.pho_pos
    x2,y2,z2 = space_2  # opt_mcx.hop_pos
    dx,dy,dz = bin_size  # opt_tis.vox_d,   opt_mci.space_d
   # 意义不明
    min_x = min(math.floor(x1/dx),math.floor(x2/dx)) * dx
    min_y = min(math.floor(y1/dy),math.floor(y2/dy)) * dy
    min_z = min(math.floor(z1/dz),math.floor(z2/dz)) * dz
    max_x = min_x + dx
    max_y = min_y + dx
    max_z = min_z + dx

    sv = x1 <= max_x and x2 <= max_x and y1 <= max_y and y2 <= max_y and z1 <= max_z and z2 <= max_z

    return sv


def find_voxel_margin(space_1, space_2, bin_size, angle_weight):
    x1,y1,z1 = space_1  # original position
    x2,y2,z2 = space_2  # new position
    dx,dy,dz = bin_size  # voxel size with cm
    ux,uy,uz = angle_weight  # anle with sum^2 == 1   (nearly

    ix1 = math.floor(x1 / dx)
    iy1 = math.floor(y1 / dy)
    iz1 = math.floor(z1 / dz)

    ix2 = (ix1 + 1) if ux >= 0 else ix1
    iy2 = (iy1 + 1) if uy >= 0 else iy1
    iz2 = (iz1 + 1) if uz >= 0 else iz1

    xs = math.fabs((ix2*dx - x1) / (ux + 1e-8))
    ys = math.fabs((iy2*dy - y1) / (uy + 1e-8))
    zs = math.fabs((iz2*dz - z1) / (uz + 1e-8))

    s = min(xs,ys,zs)

    return s + 1e-7


def iteration_sleft(mcx, tis, flag_boundary, with_print=False):

    mcx.move_step = mcx.move_sleft / (mcx.tis_mus + 1e-12)

    for i in range(3):
        mcx.move_pos[i] = mcx.pho_pos[i] + mcx.move_step * mcx.pho_radiu[i]
    # 这里的检测过没过等之后再加
    if with_print:
        print('\t <<< begin sleft >>> ------------------------')
        print('\t --- tis_mus {}'.format(mcx.tis_mus))
        print('\t --- space1 {}'.format(mcx.pho_pos))
        print('\t --- space2 {}'.format(mcx.move_pos))
        print('\t --- move_step {}'.format(mcx.move_step))
        print('\t --- angle component {}'.format(mcx.pho_radiu))


    sv = same_voxel(mcx.pho_pos, mcx.move_pos, tis.vox_d)

    if sv:  # in the same voxel
        if with_print:
            print('\tin the same voxel')
        mcx.pho_pos = copy.deepcopy(mcx.move_pos)

        # Drop photon weight (W) into local bin.
        absorb = mcx.pho_w * (1 - math.exp(-mcx.tis_mua * mcx.move_step))
        mcx.pho_w -= absorb  # decrement WEIGHT by amount absorbed
        # print(absorb)
        tis.mat_f[mcx.pho_index[2], mcx.pho_index[1], mcx.pho_index[0]] = tis.mat_f[mcx.pho_index[2], mcx.pho_index[1], mcx.pho_index[0]] + absorb

        mcx.move_sleft = 0 # Update sleft
    # -------------------------------------------------------------------------------------------------------- 2023 02 16
    else:  # photon has crossed voxel boundary
        if with_print:
            print('\tcrossed voxel boundary')

        s = find_voxel_margin(mcx.pho_pos, mcx.move_pos, tis.vox_d, mcx.pho_radiu)

        # Drop photon weight (W) into local bin
        absorb = mcx.pho_w * (1 - math.exp(-mcx.tis_mua * mcx.move_step))
        mcx.pho_w -= absorb  # decrement WEIGHT by amount absorbed

        tis.mat_f[mcx.pho_index[2], mcx.pho_index[1], mcx.pho_index[0]] += absorb

        mcx.move_sleft -= s * mcx.tis_mus
        if mcx.move_sleft <= 1e-7:
            mcx.move_sleft = 0

        mcx.pho_pos[0] += s * mcx.pho_radiu[0]
        mcx.pho_pos[1] += s * mcx.pho_radiu[1]
        mcx.pho_pos[2] += s * mcx.pho_radiu[2]

        mcx.pho_index[0] = int(tis.vox_N[0] / 2 + mcx.pho_pos[0] / tis.vox_d[0])
        mcx.pho_index[1] = int(tis.vox_N[1] / 2 + mcx.pho_pos[1] / tis.vox_d[1])
        mcx.pho_index[2] = int(                   mcx.pho_pos[2] / tis.vox_d[2])

        # 这块开始考虑是不是要导入boundary_flag的事,先忽略
        if flag_boundary == 0:  # Infinite medium.
            pass
        elif flag_boundary == 1:  # Escape at boundaries
            # 超出边缘强制跳出
            # if mcx.pho_pos[2] < 0.15:  # With repect, Mr.cong
            #     ss = (mcx.pho_pos[2] - 0.10) / mcx.pho_u[2]
            for i,(pho_index,vox_N) in enumerate(zip(mcx.pho_index, tis.vox_N)):
                if pho_index >= vox_N:
                    mcx.pho_index[i] = tis.vox_N[i] - 1
                    mcx.pho_status = False
                    mcx.move_sleft = 0
                    if with_print:
                        print('\t\ttorch boundary_1')
            for i, pho_index in enumerate(mcx.pho_index):
                if pho_index < 0:
                    mcx.pho_index[i] = 0
                    mcx.pho_status = False
                    mcx.move_sleft = 0
                    if with_print:
                        print('\t\ttorch boundary_2')
        elif flag_boundary == 2:  # Escape at top surface, no x,y bottom z boundaries
            pass
        # update pointer to tissue type
        type = tis.mat_v[mcx.pho_index[2], mcx.pho_index[1], mcx.pho_index[0]]
        mcx.tis_mua = tis.v_mua[type - 1]
        mcx.tis_mus = tis.v_mus[type - 1]
        mcx.tis_g = tis.v_g[type - 1]

    if with_print:
        print('\t >>> position index {} location {:.4f} {:.4f} {:.4f}'.format(mcx.pho_index,mcx.pho_pos[0], mcx.pho_pos[1], mcx.pho_pos[2]))
        print('\t >>> photon move count {} with weight {} and step {} '.format(mcx.move_cnt, mcx.pho_w, mcx.move_step))
        print('\t <<< end sleft >>> ------------------------')
    return mcx, tis