import math


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
    x1,y1,z1 = space_1  # opt_mcx.pho_pos
    x2,y2,z2 = space_2  # opt_mcx.hop_pos
    dx,dy,dz = bin_size  # opt_tis.vox_d
    ux,uy,uz = angle_weight  # opt_mcx.pho_u

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


def iteration_sleft(mcx, tis, flag_boundary,with_print=False):
    mcx.hop_step = mcx.hop_sleft / (mcx.tis_mus + 1e-12)
    # print(mcx.hop_step)
    for i in range(3):
        mcx.hop_pos[i] = mcx.pho_pos[i] + mcx.hop_step * mcx.pho_u[i]
    # 这里的检测过没过等之后再加
    if with_print:
        print('\t --- tis_mus {}'.format(mcx.tis_mus))
        print('\t --- hop_step {}'.format(mcx.hop_step))
        print('\t --- space1 {}'.format(mcx.pho_pos))
        print('\t --- move_step {}'.format(mcx.hop_step))
        print('\t --- angle component {}'.format(mcx.pho_u))
        print('\t --- space2 {}'.format(mcx.hop_pos))

    sv = same_voxel(mcx.pho_pos, mcx.hop_pos, tis.vox_d)

    if sv:  # in the same voxel
        if with_print:
            print('\tin the same voxel')

        mcx.pho_pos = mcx.hop_pos  # Update positions

        # Drop photon weight (W) into local bin.
        absorb = mcx.photon_w * (1 - math.exp(-mcx.tis_mua * mcx.hop_step))
        mcx.photon_w -= absorb  # decrement WEIGHT by amount absorbed
        # print(absorb)
        tis.mat_f[mcx.pho_i[2], mcx.pho_i[1], mcx.pho_i[0]] = tis.mat_f[mcx.pho_i[2], mcx.pho_i[1], mcx.pho_i[0]]+absorb

        mcx.hop_sleft = 0 # Update sleft

    else:  # photon has crossed voxel boundary
        if with_print:
            print('\tcrossed voxel boundary')

        s = find_voxel_margin(mcx.pho_pos, mcx.hop_pos, tis.vox_d, mcx.pho_u)

        # Drop photon weight (W) into local bin
        absorb = mcx.photon_w * (1 - math.exp(-mcx.tis_mua * mcx.hop_step))
        mcx.photon_w -= absorb  # decrement WEIGHT by amount absorbed
        # print(absorb)
        tis.mat_f[mcx.pho_i[2], mcx.pho_i[1], mcx.pho_i[0]] = tis.mat_f[mcx.pho_i[2], mcx.pho_i[1], mcx.pho_i[0]]+absorb

        mcx.hop_sleft -= s * mcx.tis_mus
        if mcx.hop_sleft <= 1e-7:
            mcx.hop_sleft = 0

        mcx.pho_pos[0] += s * mcx.pho_u[0]
        mcx.pho_pos[1] += s * mcx.pho_u[1]
        mcx.pho_pos[2] += s * mcx.pho_u[2]

        mcx.pho_i[0] = int(tis.vox_N[0] / 2 + mcx.pho_pos[0] / tis.vox_d[0])
        mcx.pho_i[1] = int(tis.vox_N[1] / 2 + mcx.pho_pos[1] / tis.vox_d[1])
        mcx.pho_i[2] = int(mcx.pho_pos[2] / tis.vox_d[2])



        # 这块开始考虑是不是要导入boundary_flag的事,先忽略
        if flag_boundary == 0:  # Infinite medium.
            pass
        elif flag_boundary == 1:  # Escape at boundaries
            # 超出边缘强制跳出
            # if mcx.pho_pos[2] < 0.15:  # With repect, Mr.cong
            #     ss = (mcx.pho_pos[2] - 0.10) / mcx.pho_u[2]
            for i,(pho_i,vox_N) in enumerate(zip(mcx.pho_i, tis.vox_N)):
                if pho_i >= vox_N:
                    mcx.pho_i[i] = tis.vox_N[i] - 1
                    mcx.photon_status = False
                    mcx.hop_sleft = 0
                    if with_print:
                        print('\ttorch boundary')
            for i, pho_i in enumerate(mcx.pho_i):
                if pho_i < 0:
                    mcx.pho_i[i] = 0
                    mcx.photon_status = False
                    mcx.hop_sleft = 0
                    if with_print:
                        print('torch boundary')
        elif flag_boundary == 2:  # Escape at top surface, no x,y bottom z boundaries
            pass
        # update pointer to tissue type
        type = tis.mat_v[mcx.pho_i[2], mcx.pho_i[1], mcx.pho_i[0]]
        mcx.tis_mua = tis.v_mua[type - 1]
        mcx.tis_mus = tis.v_mus[type - 1]
        mcx.tis_g = tis.v_g[type - 1]

    if with_print:
        print('\t >>> position index {} location {:.4f} {:.4f} {:.4f}'.format(mcx.pho_i,mcx.pho_pos[0], mcx.pho_pos[1], mcx.pho_pos[2]))
        print('\t >>> photon move count {} with weight {} and step {}'.format(mcx.hop_cnt, mcx.photon_w, mcx.hop_step))
    return mcx, tis