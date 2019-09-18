import numpy as  np

a=np.array([[1,2],[3,4]])
a1=np.mat([[1,2],[3,4]]).T
print(a)
print(a1)
b=np.array([1,2])
print()
print(np.dot(a,b))
print(np.multiply(a,b))
print((a-b))
