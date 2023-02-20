- opt_mcx  设定需要的蒙卡模拟参数
- opt_mci  读mci、写prop
- opt_probe  四个探头的位置信息
- opt_light   光源的data.txt
- opt_tissue 组织的信息，主要包括 _T.bin的内容



##### opt_mci

opt_mci  读mci、写prop

这一部分不变,理论上作为静态变量处理

| 参数          | 类型  | 来源                                          | 描述                                                         |
| ------------- | ----- | --------------------------------------------- | ------------------------------------------------------------ |
| time          | float | infos[0]                                      | simulation time                                              |
| space_N       | list  | [int(infos[1]), int(infos[2]), int(infos[3])] | bins number Nx Ny Nz                                         |
| space_d       | list  | [infos[4], infos[5], infos[6]]                | bins size Nx Ny Nz (cm)                                      |
| flag_mc       | int   | int(infos[7])                                 | Light source mode set by matlab                              |
| flag_launch   | int   | int(infos[8])                                 | Launch mode set by matlab                                    |
| flag_boundary | int   | int(infos[9])                                 | Boundary set by matlab                                       |
| space_s       | list  | [infos[10], infos[11], infos[12]]             | The position of photon init xs,ys,zs                         |
| space_focus   | list  | [infos[13], infos[14], infos[15]]             | The position of light source xfocus，yfocus，zfocus          |
| space_u0      | list  | [infos[16], infos[17], infos[18]]             | The proportion of the angle of photon movement on xyz, Sum of squares == 1 |
| radius_waist  | list  | [infos[19], infos[20]]                        | 光源在皮肤表面的半径 & 光源在光子启动处的半径                |
| v_Nt          | int   | int(infos[21])                                | Categories number                                            |
| v_mua         | list  | 22 25 28...                                   | Optical absorption coefficient                               |
| v_mus         | list  | 23 26 29...                                   | Optical scattering coefficient                               |
| v_g           | list  | 24 27 30...                                   | Anisotropy parameter                                         |

##### init_probe()

probes 四个探头的位置信息  设定需要的光子模拟参数  字典

| 字典参数 | 参数     | 参数  | 描述                                          |
| -------- | -------- | ----- | --------------------------------------------- |
| probe_1  | position | scale | position : [x,y, hh]   scale : [width,height] |
| probe_2  | position | scale | position : [x,y, hh]   scale : [width,height] |
| probe_3  | position | scale | position : [x,y, hh]   scale : [width,height] |
| probe_4  | position | scale | position : [x,y, hh]   scale : [width,height] |

##### init_light(path_input)

light  只包含光源的data.txt, 只是一个91,360的numpy数组

##### init_photon()

之前的mcx, 现在按照字典类型设定需要的光子模拟参数  

| 字典参数      | 重置          | 更新          | 描述                                      |
| ------------- | ------------- | ------------- | ----------------------------------------- |
| **flag_b**    | 每个光子重置  |               | 边界条件 True: continue, False: break     |
| move_cnt      | 每个光子重置  | 每次sleft更新 | 光子在该sleft下移动计数                   |
| move_pos      | 每个光子重置  | 每次sleft更新 | 光子每次移动的新位置                      |
| move_sleft    | 每次sleft重置 | 每次sleft更新 | sleft剩余距离                             |
| move_step     | 每次sleft重置 | 每次sleft更新 | 根据剩余sleft和光学散射系数计算的移动步长 |
| **num_index** | 每个光子更新  |               | 光子编号                                  |
| pho_index     | 每个光子重置  | 每次sleft更新 | 光子当前位置索引                          |
| pho_pos       | 每个光子重置  | 每次sleft更新 | 光子当前的空间位置                        |
| pho_radiu     | 每个光子重置  | 每个sleft更新 | 光子在xyz上的角度分量                     |
| pho_status    | 每个光子更新  |               | 光子状态                                  |
| pho_w         | 每次sleft重置 | 每次sleft更新 | 光子权重                                  |
| **tis_g**     | 每个光子重置  | 每个sleft更新 | 该索引位置的各向异性                      |
| **tis_mua**   | 同上          |               | 该索引位置的光学吸收系数                  |
| **tis_mus**   | 同上          |               | 该索引位置光学散射系数                    |

##### init_tissue(opts, path_input, prefix)

tissue 组织的信息，主要包括 _T.bin的内容



| 字典参数 | 重置   | 更新          | 描述                                                         |
| -------- | ------ | ------------- | ------------------------------------------------------------ |
| mat_f    | 不重置 | 每次sleft更新 | 按照z,y,x储存的**光通量**  Nz, Ny, Nx维numpy数组 [W/cm^2/W.delivered] |
| mat_r    | 未使用 |               | 按照z,y,x储存的escaping flux    Nz, Ny, Nx维的numpy数组  (未使用) |
| mat_v    | 不重置 | 不更新        | 按照z,y,x储存 对应位置的 **光学参数索引**  Nz, Ny, Nx维的numpy数组 |
| v_g      | 不重置 | 不更新        | Anisotropy parameter  type长度的list                         |
| v_mua    | 不重置 | 不更新        | Optical absorption coefficient     type长度的list            |
| v_mus    | 不重置 | 不更新        | Optical scattering coefficient     type长度的list            |
| vox_N    | 不重置 | 不更新        | 组织体素的空间大小 x y z list                                |
| vox_d    | 不重置 | 不更新        | 组织体素数量x y z list                                       |

