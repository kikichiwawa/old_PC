from PIL import Image, ImageDraw
from numpy import array, floor, cos, sin, pi,sqrt, cross, dot
import matplotlib.pyplot as plt
import numpy as np

def ztocol(zz,color):
    Mcol = array(color)
    z = zz-depth
    if(z < -depth):
        z = -depth
    elif(z > depth):
        z = depth
    gradation = (-z + depth)/(2 * depth)
    colf = Mcol * gradation
    col = (int(floor(colf[0])),int(floor(colf[1])),int(floor(colf[2])))
    return col

def drawCcc(draw, rlist, color):
    zlist = []
    q1 = []
    q2 = []
    for r in rlist:
        zlist.append(r[2])

    rsize = len(rlist)
    mz = max(zlist)
    im = zlist.index(mz)
    Mz = min(zlist)
    iM = zlist.index(Mz)

    if(abs(mz - Mz) < 1):
        pointslist = []
        for r in rlist:
            pointslist.append((r[0],r[1]))
        col = ztocol(mz,color)
        draw.polygon(pointslist,fill = col)

        return

    crs = cross(rlist[2]-rlist[1],rlist[0]-rlist[1])

    steplist = []
    drlist = []
    for i in range(rsize):
        step = int(floor(2 * abs(crs[0]*(rlist[i]-rlist[(i+1)%rsize])[0]-crs[1]*(rlist[i]-rlist[(i+1)%rsize])[1]) / (sqrt(crs[0]**2 + crs[1]**2)+0.0001)))
        dr = (rlist[(i+1)%rsize]-rlist[i]) / (step + 1)
        steplist.append(step)
        drlist.append(dr)



    rsize1 = (iM - im) % rsize
    rsize2 = rsize - rsize1


    drlist1 = []
    steplist1 = [0]
    step1 = 0
    for i in range(rsize1):
        drlist1.append(drlist[(im + i)%rsize])
        step1 = step1 + steplist[(im + i)%rsize]
        steplist1.append(step1)
    drlist2 = []
    steplist2 = [0]
    step2 = 0
    for i in range(rsize2):
        drlist2.append(-1 * drlist[(im -1 - i)%rsize])
        step2 = step2 + steplist[(im -1 - i)%rsize]
        steplist2.append(step2)


    for i in range(steplist1[rsize1]):
        for j in range(rsize1):
            if(i <= steplist1[j+1]):
                q1 = rlist[(im + j) % rsize] + (i-steplist1[j]) * drlist1[j]
                break
        for j in range(rsize2):
            if(i <= steplist2[j+1]):
                q2 = rlist[(im - j) % rsize] + (i-steplist2[j]) * drlist2[j]
                break

        col = ztocol(q1[2],color)
        draw.line((q1[0], q1[1], q2[0], q2[1]), fill = col)


def drawCcs(draw,rlist,slist,llist,color1,color2):
    sslist = list(slist)
    Mzlist = []
    dllist = list(llist)

    for sindex in sslist:
        zlist = []
        for i in sindex:
            zlist.append(rlist[i][2])
        Mzlist.append(max(zlist))

    for i in range(len(sslist)):
        j = Mzlist.index(max(Mzlist))

        sindex = sslist[j]
        drlist = []

        for k in range(len(sindex)):
            drlist.append(rlist[sindex[k]])
        drawCcc(draw,drlist,color1)

        for l in range(len(dllist)-1,-1,-1):
            if((dllist[l][0] in sindex) & (dllist[l][1] in sindex)):
                l1 = rlist[dllist[l][0]]
                l2 = rlist[dllist[l][1]]
                draw.line((l1[0],l1[1],l2[0],l2[1]), fill = color2)

        del sslist[j]
        del Mzlist[j]

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

"""
～～～～～～～～～～　　以下本文　　～～～～～～～～～～
"""

images = []

width = 1000
depth = 500
scale = depth/sqrt(3) #立方体の一辺の長さの半分に当たる．depth/√3で丁度収まる
center = width // 2
O = array([center,center,0])
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
color_3 = (0, 255, 255)
color_4 = (255, 0, 0)

step = 100
ro = array([depth,pi,0])
v = array([0, 2 * pi / step,2 * pi / step])

r1 =  array([-1,1,-1])
r2 =  array([1,1,-1])
r3 =  array([1,1,1])
r4 =  array([-1,1,1])
r5 =  array([-1,-1,-1])
r6 =  array([1,-1,-1])
r7 =  array([1,-1,1])
r8 =  array([-1,-1,1])

rlist = tuple(array((r1,r2,r3,r4,r5,r6,r7,r8))*scale)
slist = ((0,1,2,3),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7))
llist = ()
#llist = ((0,1),(0,3),(0,4),(1,2),(1,5),(2,3),(2,6),(3,7),(4,5),(4,7),(5,6),(6,7))
#slist = ((1,2,0),(2,3,0),(4,5,7),(5,6,7))
#llist = ((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4))


for i in range(step):
    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)

    drlist = observe(ro,rlist)
    for j in range(len(drlist)):
        drlist[j] = O + drlist[j]

    print(i)
    drawCcs(draw, drlist, slist,llist, color_3,color_4)
    #zahyoudraw(draw,ro,depth,color_2,color_2,color_2)
    images.append(im)

    ro = ro + v


images[0].save(R'C:\Users\nishi\pp-python\hobby\output\3dcube.gif',save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
