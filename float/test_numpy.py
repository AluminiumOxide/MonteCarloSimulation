import numpy as np
a = np.array([1,2,3,4,5,6,7,8])
a1 = a.reshape([2,2,2])
print(a1[0,0,0])
print(a1[0,0,1])
print(a1[0,1,0])
print(a1[0,1,1])
print(a1[1,0,0])
print(a1[1,0,1])
print(a1[1,1,0])
print(a1[1,1,1])
print(a1.shape)
a_out = a1.reshape(8)

"""
输出是12345678 因此这玩意 xyz是反的
"""
a2=a1.transpose(2,1,0)
print(a2[0,0,0])
print(a2[1,0,0])
print(a2[0,1,0])
print(a2[1,1,0])
print(a2[0,0,1])
print(a2[1,0,1])
print(a2[0,1,1])
print(a2[1,1,1])
print(a2.shape)