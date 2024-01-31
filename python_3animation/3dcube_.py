from PIL import Image, ImageDraw
from numpy import array, floor, cos, sin, pi,sqrt, cross, dot
import matplotlib.pyplot as plt
import numpy as np

def stoz(data, rlist, color, vertical, horizontal, p, q, r):
    count = 0
    """
    まず3点をr1,r2,r3で置き換える
    """
    xlist = []
    for rr in rlist:
        xlist.append(rr[0])
    mxi = xlist.index(min(xlist))
    rsize = len(rlist)
    r1 = rlist[mxi]

    r01 = rlist[(mxi+1)%rsize]
    r02 = rlist[(mxi-1)%rsize]
    crs = cross(r02 - r1,r01 - r1)
    if(crs[2]>= 0):
        r2 = r01
        r3 = r02
    else:
        r2 = r02
        r3 = r01

    """
    平面の式、処理をするxの値、ペラペラだったときの例外処理を行う
    """

    x = max(int(floor(r1[0])),0)
    Mx = min(int(floor(max(xlist))),horizontal-1)
    step = Mx - x - 2
    if(step < 0):
        return data

    """
    上側の直線 y =a1*x + b1 と下側の直線を求める
    """
    a1 = (r1[1] - r2[1])/(r1[0] - r2[0])
    b1 = - r1[0] * a1 + r1[1]
    a2 = (r1[1] - r3[1])/(r1[0] - r3[0])
    b2 = - r1[0] * a2 + r1[1]

    """
    対象とする座標を進める処理
    """
    check1 = False
    check2 = False

    if(x + 1 >= r2[0]):
        a1 = (r2[1] - r3[1])/(r2[0] - r3[0])
        b1 = - r2[0] * a1 + r2[1]
        check1 = True
    elif(x + 1 >= r3[0]):
        a2 = (r2[1] - r3[1])/(r2[0] - r3[0])
        b2 = - r3[0] * a2 + r3[1]
        check2 = True

    """
    最大・最小のyを得て、zに当てはまる等差数列を取得、
    """

    My = min(int(floor(a1 * (x + 1) + b1)),vertical-1)
    my = max(int(floor(a2 * (x + 1) + b2)),0)
    ylist = np.arange(my, My+1, 1)
    ysize = My - my + 1
    Mz = p*x + q*My + r
    mz = p*x + q*my + r

    zlist = p*x + r + ylist * q
    vlist = (zlist / depth + 1) * 50
    intvlist = vlist.astype(int)

    for y in range(my, My + 1):
        v = intvlist[y-my]
        if((v > data[y , x])and(v >= 0)and(v <= 100)):
            count = count + 1
            data[y, x] = v

    """
    傾きにより、参照する座標が格子の右側か左側かを判断する
    """
    lr1 = lr2 = 0
    if(a1 >= 0):
        lr1 = 1
    if(a2 >= 0):
        lr2 = 1
    x = x + 1

    for i in range(step):
        if(x >= horizontal-1):
            break

        if(check1 or check2):
            My = min(int(floor(a1 * (x + lr1) + b1)),vertical-1)
            my = max(int(floor(a2 * (x + lr2) + b2)),0)
        else:
            if(x + 1 >= r2[0]):
                y = int(floor(a1 * x + b1))
                a1 = (r2[1] - r3[1])/(r2[0] - r3[0])
                b1 = - r2[0] * a1 + r2[1]
                if(a1 >= 0):
                    lr1 = 1
                else:
                    lr1 = 0

                My = min(max(int(floor((a1 * (x + 1) + b1))), y),vertical-1)
                my = max(int(floor(a2 * (x + lr2) + b2)),0)
            elif(x + 1 >= r3[0]):
                y = int(floor(a2 * x + b2))
                a2 = (r2[1] - r3[1])/(r2[0] - r3[0])
                b2 = - r3[0] * a2 + r3[1]
                if(a2 >= 0):
                    lr2 = 1
                else:
                    lr2 = 0
                My = min(int(floor((a1 * (x + lr1) + b1))),vertical-1)
                my = max(min(int(floor((a2 * (x + 1) + b2))), y),0)
            else:
                My = min(int(floor(a1 * (x + lr1) + b1)),vertical-1)
                my = max(int(floor(a2 * (x + lr2) + b2)),0)

        ylist = np.arange(my, My+1, 1)
        ysize = My - my + 1
        Mz = p*x + q*My +r
        mz = p*x + q*my +r

        zlist = p*x + r + ylist * q
        vlist = (zlist / depth + 1) * 50
        intvlist = vlist.astype(int)
        for y in range(my, My + 1):
            if(y - my > vertical):
                break
            v = intvlist[y-my]
            if((v > data[y , x])and(v >= 0)and(v <= 100)):
                count = count + 1
                data[y, x] = v

        x = x + 1

    My = min(int(floor(a1 * x + b1)),vertical-1)
    my = max(int(floor(a2 * x + b2)),0)
    ylist = np.arange(my, My+1, 1)
    ysize = My - my + 1
    Mz = p*x + q*My + r
    mz = p*x + q*my + r

    zlist = p*x + r + ylist * q
    vlist = (zlist / depth + 1) * 50

    intvlist = vlist.astype(int)
    for y in range(my, My + 1):
        v = intvlist[y-my]
        if((v > data[y , x])and(v >= 0)and(v <= 100)):
            count = count + 1
            data[y, x] = v
    #print(count)
    return data

def makedata(drlist, slist, color, vertical, horizontal):
    print(color)
    vdata = np.full((vertical,horizontal),0)
    count = 0
    for indexlist in slist:
        rlist = []
        for index in indexlist:
            rlist.append(drlist[index])
        crs = cross(rlist[1]-rlist[0],rlist[2]-rlist[0])
        p = -crs[0]/crs[2]
        q = -crs[1]/crs[2]
        r = dot(rlist[0],crs)/crs[2]

        if(abs(q) < 0.01):
            q = abs(q)
        for i in range(len(rlist)-2):
            rlist2 = [rlist[0], rlist[i + 1], rlist[i + 2]]
            vdata = stoz(vdata, rlist2, color, vertical, horizontal, p, q, r)
            count = count + 1
    hdata = np.full((vertical,horizontal),color[0])
    sdata = np.full((vertical,horizontal),color[1])
    coldata = np.stack([hdata, sdata, vdata],2)
    return coldata

def observe(ro,rlist):
    result = []
    A = -1 * array([[-sin(ro[2]),cos(ro[2]),0],[cos(ro[1])*cos(ro[2]),cos(ro[1])*sin(ro[2]),-sin(ro[1])],[sin(ro[1])*cos(ro[2]),sin(ro[1])*sin(ro[2]),cos(ro[1])]])
    roc = array([sin(ro[1])*cos(ro[2]),sin(ro[1])*sin(ro[2]),cos(ro[1])])*ro[0]
    for r in rlist:
        rr = r - roc
        result.append(A@rr)
    return result

def zahyoudraw(draw,ro,depth,color1,color2,color3):
    zahyou = [[-3 * depth,0,0],[3 * depth,0,0],[0,-3 * depth,0],[0,3 * depth,0],[0,0,-3 * depth],[0,0,3 * depth]]
    zahyou = observe(ro, zahyou)
    colors = (color1,color2,color3)
    for i in range(len(zahyou)):
        zahyou[i] = O + zahyou[i]
    for i in range(3):
        draw.line((zahyou[2*i][0],zahyou[2*i][1],zahyou[2*i+1][0], zahyou[2*i+1][1]),fill = colors[i])

def lapdet(rlist1, rlist2):#rlist1,rlist2で張られる領域の重なりの有無を判定し，重なっていればその点を返す
    for r1 in rlist1:
        for i in range(len(rlist2)):
            a = rlist2[i] - r1
            b = rlist2[i] - rlist2[i]

images = []

vertical = 1000
horizontal = 1000
depth = 500
scale = depth  #立方体の一辺の長さの半分に当たる．depth/√3で丁度収まる
O = array([vertical / 2, horizontal / 2, -depth])
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
color_3 = (0, 255, 255)
color_4 = (255, 0, 0)

step = 100
ro = array([depth,pi/3,pi / 4])
v = array([0, 2 * pi / step,2 * pi / step])
"""
r1 =  array([-1,0,-1])
r2 =  array([0,0,-1])
r3 =  array([0,0,0])
r4 =  array([-1,0,0])
r5 =  array([-1,-1,-1])
r6 =  array([0,-1,-1])
r7 =  array([0,-1,0])
r8 =  array([-1,-1,0])
r9 =  array([1,1,1])
r10 = array([1,1,-1])
r11 = array([-1,1,-1])
r12 = array([-1,1,1])
r13 = array([1,0,1])
r14 = array([1,0,-1])
r15 = array([-1,0,1])
r16 = array([0,0,1])

rlist = tuple(array((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16))*scale)
slist = ((0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7),(12,13,1,15),(2,15,14,3),(8,9,10,11),(8,9,13,12),(9,10,0,13),(10,11,14,0),(11,8,12,14))
"""

slist = ((0,1,2),(0,1,3),(0,2,3),(1,2,3))

for i in range(step * 2):
    r1 = array([sin(2 + 0 * pi / step * i) * cos(3 * pi / step * i),sin(2 + 0 * pi / step * i) * sin(3 * pi / step * i),cos(0 * pi / step * i)])*0.9
    r2 = array([sin(-1 * pi / step * i) * cos(2 * pi / step * i),sin(-1 * pi / step * i) * sin(2 * pi / step * i),cos(1 * pi / step * i)])*0.4
    r3 = array([sin(2 * pi / step * i) * cos(1 * pi / step * i),sin(2 * pi / step * i) * sin(1 * pi / step * i),cos(2 * pi / step * i)])*0.8
    r4 = array([sin(-3 * pi / step * i) * cos(0 * pi / step * i),sin(-3 * pi / step * i) * sin(0 * pi / step * i),cos(3 * pi / step * i)])*0.7
    rlist = array([r1,r2,r3,r4]) * scale
    drlist = observe(ro,rlist)
    for j in range(len(drlist)):#中心をx、y方向の原点にする
        drlist[j] = O + drlist[j]

    data = makedata(drlist, slist, (0,0), vertical, horizontal)
    im = Image.fromarray(np.uint8(data), 'HSV')
    im_rgb = im.convert('RGB')
    images.append(im_rgb)

    ro = ro + v

images[0].save(R'C:\Users\nishi\pp-python\hobby\output\3dcube2.gif',save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
