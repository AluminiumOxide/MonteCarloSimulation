必须注意mci里面都是按照 x y z储存
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

## 2023/02/17

暂时算是完成了模拟的基本流程，deepcopy直接占了10%时间，先把对象里储存的东西都看成是numpy数组吧，floor也很耗时

## 2023/02/17

调出来了光子运动位置的图，看起来还行，然后就是如果拿二维表示的话，散点图，横纵xz，深度y，拿点的透明度代表深度，用大小代表weight是不是也可以？