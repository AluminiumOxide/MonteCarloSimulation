import math
import copy
import numpy as np


def same_voxel(space_1, space_2, bin_size):
    # 当前位置/dx 相当于恢复到当前精确索引位置
    # 然后的操作相当于所有的网格的顶点都位于向下取整的位置，这也是为啥÷完dx都floor一下的原因
    # 然后如果都在网格以内，就应该是在这个网格位置对角，（最大的点）比两个点的位置都大，那就是证明网格没有洞
    x1,y1,z1 = space_1
    x2,y2,z2 = space_2
    dx,dy,dz = bin_size
   # 意义不明
    min_x = min(math.floor(x1/dx), math.floor(x2/dx)) * dx
    min_y = min(math.floor(y1/dy), math.floor(y2/dy)) * dy
    min_z = min(math.floor(z1/dz), math.floor(z2/dz)) * dz
    max_x = min_x + dx
    max_y = min_y + dx
    max_z = min_z + dx
    sv = x1 <= max_x and x2 <= max_x and \
         y1 <= max_y and y2 <= max_y and \
         z1 <= max_z and z2 <= max_z

    # space_min = np.floor((space_2 - space_1)/bin_size)
    # sv2 = np.max(space_min) < 1
    # if sv != sv2:
    #     print('出问题了')

    return sv


def find_voxel_margin(space_1, space_2, bin_size, angle_weight):
    '''
    首先和上面一样，[xyz]1/d[xyz] 相当于获得到0~网格数量精确的位置信息
    那么经过向下取整，i[xyz]就相当于获取到这个位置对应方形网格的索引
    并且根据当前的角度u[xyz] 可以得到这个索引位置的移动方向，取这个方向的调整位置至于为什么是正方向加反方向不加，这个问题还得问它是向下取整的

    也就是可以理解为，我们能捕获的范围包括索引点为中心（默认是左后上）的三维米字，这样不够，只占了这个网格的三个面
        为了让检测域填满当前立方体的所有边界面，
        移动三次，把右前下靠着的索引面给带进去
        至少现在，按照调整后索引的米字检测范围，经过调整后的 i[xyz]2 可以正好抓到这个网格往这个方向飞的光子
    '''


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
    '''
        i[xyz]2*d[xyz]相当于恢复到和[xyz]1一样的尺度上索引与位置相减并取绝对值,这里就相当于寻找到这个点到三个面的距离,
        当然, 还得考虑到角度分量,至于为什么说是除法呢?
        你可以理解为: 当前坐标向对应面做垂线,前面的计算是这条垂线的长度
        过当前点 方向为当前移动角度 的 延长线 与对应面相交 
        我忙除一下就相当于得到这个延长线和的长度,三个面怼的线段还都是一个,最先怼到的面就相当于是最近的面,只需要确保刚出这个网格的长度就完事
        
        也是为什么后面取最小的,为了出去就打中,然后加一个很小的数保证能确实出这个网格
    '''
    xs = math.fabs((ix2*dx - x1) / (ux + 1e-8))
    ys = math.fabs((iy2*dy - y1) / (uy + 1e-8))
    zs = math.fabs((iz2*dz - z1) / (uz + 1e-8))

    s = min(xs, ys, zs)

    return s + 1e-4

