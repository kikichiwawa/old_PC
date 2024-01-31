from PIL import Image, ImageDraw
from numpy import array, floor, cos, sin, pi,sqrt, cross, dot
import matplotlib.pyplot as plt
import numpy as np

def inputv(data, x, My, my, xo, yo, p, q, r, depth):
    ylist = np.arange(my, My+1, 1)

    for y in range(my, My + 1):
        z = 1 / (p*x + q*y + r)
        v = 0
        if(abs(z) < depth):
            v = int((z / depth + 1) * 50)
        if(-y -1+ yo >= 1000):
            print("y")
            print(-y , yo)
        elif(x + xo >= 1000):
            print(x,xo)
            print("x")
        if(v > data[-y -1 + yo, x + xo]):
            data[-y -1 + yo, x + xo] = v
    return data

def getab(r1, r2, z):#r1は表であるとする
    a = (r1[1] * r2[2] - r1[2] * r2[1]) / (r1[0] * r2[2] - r1[2] * r2[0])
    b = (r1[0] * r2[1] - r1[1] * r2[0]) / (r1[0] * r2[2] - r1[2] * r2[0]) * z
    return a,b

def stoz(data, rlist, color, vertical, horizontal, a, b, c, d, screenz):
    count = 0
    xo = int(horizontal / 2)
    yo = int(vertical / 2)
    """
    まず3点をr1,r2,r3で置き換える
    """
    xlist = []
    ylist = []
    zcount = 0 #zが正の値を取る点の数
    omotelist = []
    uralist = []
    for i in range(3):
        if(rlist[i][2] > 0):
            xlist.append(rlist[i][0] * screenz / rlist[i][2])
            zcount = zcount + 1
            omotelist.append(i)
        else:
            uralist.append(i)

    mx = Mx = xborder = 0
    f1 , f2, f3= [], [], []
    print(zcount)
    if(zcount == 0):
        return data

    elif(zcount == 1):
        ro = rlist[uralist[0]]
        ru = rlist[uralist[1]]
        rr = rlist[omotelist[0]]
        print(rr,ro,ru)

        a1,b1 = getab(rr, ro, screenz)
        a2,b2 = getab(rr, ru, screenz)

        if(a == 0):
            if(d / b < 0):
                if(a1 > a2):
                    a1, b1, a2, b2 = a2, b2, a1, b1
                    ro, ru = ru, ro
                mx = xborder = -xo
                Mx = int(min(floor(max(xlist)), xo - 1))
                y1 = a1 * (-xo) + b1
                y2 = a2 * (-xo) + b2
                f1 = [0, y1, 0, y2 - 1]
                f2 = [a1, b1, a2, b2]

            else:
                if(a1 < a2):
                    a1, b1, a2, b2 = a2, b2, a1, b1
                    ro, ru = ru, ro
                mx = int(max(floor(min(xlist)), -xo))
                y1 = a1 * (xo + 1) + b1
                y2 = a2 * (xo + 1) + b2
                Mx = xborder = xo - 1
                f1 = [a1, b1, a2, b2]
                f2 = [0, y1, 0, y2 - 1]
        elif(d / a < 0):
            if(a1 > a2):
                a1, b1, a2, b2 = a2, b2, a1, b1
                ro, ru = ru, ro
            mx = xborder = -xo
            Mx = int(min(floor(max(xlist)), xo - 1))
            y1 = a1 * (-xo) + b1
            y2 = a2 * (-xo) + b2
            f1 = [0, y1, 0, y2 - 1]
            f2 = [a1, b1, a2, b2]

        else:
            if(a1 < a2):
                a1, b1, a2, b2 = a2, b2, a1, b1
                ro, ru = ru, ro
            mx = int(max(floor(min(xlist)), -xo))
            Mx = xborder = xo - 1
            y1 = a1 * (xo + 1) + b1
            y2 = a2 * (xo + 1) + b2
            f1 = [a1, b1, a2, b2]
            f2 = [0, y1, 0, y2 - 1]

    elif(zcount == 2):
        ro = rlist[omotelist[0]]
        ru = rlist[omotelist[1]]
        qo , qu = ro * screenz / ro[2], ru * screenz / ru[2]
        if(qo[1] < qu[1]):
            ro, ru = ru, ro
            qo, qu = qu, qo
        rr = rlist[uralist[0]]
        print(ro,ru,rr)

        a1,b1 = getab(ro, rr, screenz)
        a2,b2 = getab(ru, rr, screenz)
        a3,b3 = getab(ro, ru, screenz)

        if(a == 0):
            if(d / b < 0):
                mx = -xo
                if(qo[0] > qu[0]):
                    xborder = int(qu[0])
                    Mx = int(min(qo[0], xo - 1))
                    f1 = [a1, b1, a2, b2]
                    f2 = [a1, b1, a3, b3]
                else:
                    xborder = int(qo[0])
                    Mx = int(min(qu[0], xo - 1))
                    f1 = [a1, b1, a2, b2]
                    f2 = [a3, b3, a2, b2]
            else:
                Mx = xo - 1
                if(qo[0] > qu[0]):
                    mx = int(max(qu[0], -xo))
                    xborder = int(qo[0])
                    f1 = [a1, b1, a3, b3]
                    f2 = [a1, b1, a2, b2]
                else:
                    xborder = int(qu[0])
                    mx = int(max(qo[0], -xo))
                    f1 = [a3, b3, a2, b2]
                    f2 = [a1, b1, a2, b2]
        elif(d / a < 0):
            mx = -xo
            if(qo[0] > qu[0]):
                xborder = int(qu[0])
                Mx = int(min(qo[0], xo - 1))
                f1 = [a1, b1, a2, b2]
                f2 = [a1, b1, a3, b3]
            else:
                xborder = int(qo[0])
                Mx = int(min(qu[0], xo - 1))
                f1 = [a1, b1, a2, b2]
                f2 = [a3, b3, a2, b2]

        else:
            Mx = xo - 1
            if(qo[0] > qu[0]):
                mx = int(max(qu[0], -xo))
                xborder = int(qo[0])
                f1 = [a1, b1, a3, b3]
                f2 = [a1, b1, a2, b2]
            else:
                xborder = int(qu[0])
                mx = int(max(qo[0], -xo))
                f1 = [a3, b3, a2, b2]
                f2 = [a1, b1, a2, b2]

    else:
        mxi = xlist.index(min(xlist))
        r1 = rlist[mxi]
        mx = int(max(r1[0] * screenz / r1[2], -xo))
        r2, r3 = rlist[(mxi+1)%3], rlist[(mxi-1)%3]
        q1, q2, q3 = r1 * screenz / r1[2], r2 * screenz / r2[2], r3 * screenz / r3[2]

        q12, q13 = q2 - q1, q3 - q1
        if(q12[0] * q13[1] - q12[1] * q13[0] > 0):
            r2, r3 = r3, r2
            q2, q3 = q3, q2

        a1,b1 = getab(r1, r2, screenz)
        a2,b2 = getab(r1, r3, screenz)
        a3,b3 = getab(r2, r3, screenz)

        f1 = [a1, b1, a2, b2]
        if(q2[0] < q3[0]):
            xborder = q2[0]
            Mx = int(min(q3[0], xo - 1))
            f2 = [a3, b3, a2, b2]
        else:
            xborder = q3[0]
            Mx = int(min(q2[0], xo - 1))
            f2 = [a1, b1, a3, b3]
    print(xborder)
    """
    平面の式、処理をするxの値、ペラペラだったときの例外処理を行う
    """
    p, q, r = a / (d * screenz), b / (d * screenz), c / d
    x = mx
    step =int(Mx - mx - 2)
    print("Mx,mx = ",Mx,mx,step)
    if(step < 0):
        return data

    """
    最大・最小のyを得て、zに当てはまる等差数列を取得、
    """
    a1, b1, a2, b2 = f1

    check = True
    if(check &(x >= xborder)):
        a1, b1, a2, b2 = f2
        if(f3 == []):
            check = False
        else:
            f1, f2, f3 = f2, f3, []
    print("bordder = " + str(xborder))
    print(f1,f2)
    My = int(min(floor(a1 * (x + 1) + b1), yo - 1))
    my = int(max(floor(a2 * (x + 1) + b2), -yo))
    inputv(data, x, My, my, xo, yo, p, q, r, depth)

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
        if(check &(x > xborder)):
            a1, b1, a2, b2 = f2
            if(f3 == []):
                check = False
            else:
                f1, f2, f3 = f2, f3, []
            lr1 = lr2 = 0
            if(a1 >= 0):
                lr1 = 1
            if(a2 >= 0):
                lr2 = 1
            My = int(min(max(floor((a1 * (x + 1) + b1)), floor(f1[0] * x + f1[1])), yo - 1))
            my = int(max(min(floor((a2 * (x + 1) + b2)), floor(f1[2] * x + f1[3])), -yo))

        else:
            My = int(min(floor(a1 * (x + lr1) + b1), yo - 1))
            my = int(max(floor(a2 * (x + lr2) + b2), -yo))

        inputv(data, x, My, my, xo, yo, p, q, r, depth)
        x = x + 1

    My = int(min(floor(a1 * x + b1), yo - 1))
    my = int(max(floor(a2 * x + b2), -yo))
    inputv(data, x, My, my, xo, yo, p, q, r, depth)
    return data

def makedata(drlist, slist, color, vertical, horizontal, screenz):
    vdata = np.full((vertical,horizontal),0)
    count = 0
    for indexlist in slist:
        rlist = []
        for index in indexlist:
            rlist.append(drlist[index])
        crs = cross(rlist[1]-rlist[0],rlist[2]-rlist[0])
        a, b, c = crs
        d = dot(crs,rlist[0])
        if(d != 0):
            for i in range(len(rlist)-2):
                rlist2 = [rlist[0], rlist[i + 1], rlist[i + 2]]
                vdata = stoz(vdata, rlist2, color, vertical, horizontal, a, b, c, d, screenz)
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

images = []

vertical = 1000
horizontal = 1000
depth = 600
scale = depth / 1.5  #立方体の一辺の長さの半分に当たる．depth/√3で丁度収まる
screenz = depth / 3
O = array([vertical / 2, horizontal / 2, -depth])
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
color_3 = (0, 255, 255)
color_4 = (255, 0, 0)

step = 100
ro = array([depth,0,0])
v = array([0,0,pi *2 / step])
"""

r1 =  array([-1,-1,-1])
r2 =  array([1,-1,-1])
r3 =  array([1,1,-1])
r4 =  array([-1,1,-1])
r5 =  array([0,-sqrt(2),0])
r6 =  array([sqrt(2),0,0])
r7 =  array([0,sqrt(2),0])
r8 =  array([-sqrt(2),0,0])
r9 =  array([-1,-1,1])
r10 = array([1,-1,1])
r11 = array([1,1,1])
r12 = array([-1,1,1])


rlist = tuple(array((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12))*scale)
slist = ((0,1,4),(1,2,5),(2,3,6),(3,0,7),(4,5,1),(5,6,2),(6,7,3),(7,4,0),(8,9,4),(9,10,5),(10,11,6),(11,8,7),(4,5,9),(5,6,10),(6,7,11),(7,4,8))
"""

r1 =  array([1,-1,5])
r2 =  array([-1,-1,5])
r3 =  array([-1,1,5])
r4 =  array([1,1,5])
r5 =  array([1,-1,-5])
r6 =  array([-1,-1,-5])
r7 =  array([-1,1,-5])
r8 =  array([1,1,-5])

rlist = tuple(array((r1,r2,r3,r4,r5,r6,r7,r8))*scale)

slist = tuple(((0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)))


for i in range(step):
    drlist = observe(ro,rlist)
    data = makedata(drlist, slist, (0,0), vertical, horizontal, screenz)
    im = Image.fromarray(np.uint8(data), 'HSV')
    im_rgb = im.convert('RGB')
    images.append(im_rgb)

    ro = ro + v

images[0].save(R'C:\Users\nishi\pp-python\hobby\output\3dcube2.gif',save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
