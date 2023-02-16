先类似mcx cpp文件那面

- opt_mci 来自文件.mci 对应之前matlab设置的mcx参数
  - 同时写prop.m
- opt_probe 对应个人设置的 四个探头位置
- opt_light 来自文件 data.txt 对应oppo那面给的光源分布信息
- opt_tissue 来自问你件.bin 对应之前matlab设置的组织参数

必须主义mci里面都是按照 x y z储存
而tissue 是按照 z y x 储存
后续一律按照tissue空间索引优先

其中探测器高度，把之前cpp的hh统一放到opt_probe里了

# 我谢谢你！！！argparse！！！

