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


random库:
random.random()方法用于生成一个0到1的随机浮点数：0<=n<1.0
random.uniform(a,b)：用于生成一个指定范围内的随机浮点数，两格参数中，其中一个是上限，一个是下限。如果a>b，则生成的随机数n，即b<=n<=a；如果a>b，则a<=n<=b
random.randint(a,b)：用于生成一个指定范围内的整数。其中参数a是下限，参数b是上限，生成的随机数n：a<=n<=b
random.randrange
random.randrange([start],stop[, step])：从指定范围内，按指定基数递增的集合中获取一个随机数。如：random.randrange(10,100,2)，结果相当于从[10,12,14,16,…,96,98]序列中获取一个随机数。random.randrange(10,100,2)在结果上与random.choice(range(10,100,2))等效
更多相关