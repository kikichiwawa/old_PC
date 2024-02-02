from PIL import Image, ImageDraw
import numpy as np
from numpy import array, floor, cos, sin, pi,sqrt, cross, dot
import matplotlib.pyplot as plt
def func1(size = (10,10), 
          alpha_list = np.array([[1,0,-1],[1,0,-1],[0,1,-1],[-1,-1,10]])):
    i,j = np.indices(size)
    X = np.stack((i,j,np.ones(size)), axis=2)
    B = alpha_list.T
    Y=X@B>0
    Z=Y.all(2)
    print(Z)

np.array