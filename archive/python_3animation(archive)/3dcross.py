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
    (slist)
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
        check = 0
        for i in range(len(rlist2)):
            a = r1 - rlist2[i]
            b = rlist2[(i+1)%len(rlist2)] - rlist2[i]
            c = cross(a,b)
            if(c[2]<=0):
                check = 1
                break
        if(check == 0):
            return (r1,0)
    for r2 in rlist2:
        check = 0
        for i in range(len(rlist1)):
            a = r2 - rlist1[i]
            b = rlist1[(i+1)%len(rlist1)] - rlist1[i]
            c = cross(a,b)
            if(c[2]<=0):
                check = 1
                break
        if(check == 0):
            return (r2,1)

def pickperimeter(rlist):
    around = []

    xlist = []
    for r in rlist:
        xlist.append(r[0])

    lastr = rlist[xlist.index(min(xlist))]
    around.append(lastr)
    a = array([0,1,0])

    while True:
        dotlist = []
        eblist = []
        for r in rlist:
            b = r - lastr
            if(b[0]**2 + b[1]**2 == 0):
                dotlist.append(-2)
                eblist.append(0)
            else:
                eb = b / sqrt(b[0]**2 + b[1]**2)
                dotlist.append(a[0]*eb[0] + a[1]*eb[1])
                eblist.append(eb)
        i = dotlist.index(max(dotlist))
        lastr = rlist[i]
        a = eblist[i]
        if((around[0][0] == lastr[0])&(around[0][1] == lastr[1])):
            return around
        around.append(lastr)

def lapcheck(rlist1,rlist2):
    rlist1 = pickperimeter(rlist1)
    rlist2 = pickperimeter(rlist2)

    result = lapdet(rlist1,rlist2)
    rlist = []
    if result is None:
        return 0

    elif(result[1] == 0):
        rlist = rlist2
    else:
        rlist = rlist1
    r = result[0]
    r0 = rlist[0]

    a = (rlist[1] - r0)
    ea = a / sqrt(a[0]**2 + a[1]**2)
    b = r - r0
    eb = b / sqrt(b[0]**2 + b[1]**2)
    costheta1 = ea[0]*eb[0] + ea[1]*eb[1]
    for i in range(len(rlist)-2):
        b = rlist[i+2] - r0
        eb = b / sqrt(b[0]**2 + b[1]**2)
        costheta2 = ea[0]*eb[0] + ea[1]*eb[1]
        if(costheta1 >= costheta2):
            r1 = rlist[i+1]
            r2 = rlist[i+2]
            break
    crs = cross(r2-r0,r1-r0)
    d1 = dot(crs,r0)
    d2 = dot(crs,r)
    if(d1 < d2):
        return(abs(result[1]-1))
    elif(d1 > d2):
        return(result[1])

def draw3d(draw,rlist,slist,llist,color1,color2):
    rsize = len(rlist)
    rrlist = []
    for s in slist:
        rlistin = np.zeros(rsize)
        for ss in s:
            for sss in ss:
                rlistin[sss] = 1
        listr = []
        for i in range(len(rlistin)):
            if(rlistin[i] == 1):
                listr.append(rlist[i])
        rrlist.append(listr)


    rrsize = len(rrlist)
    dorder = list(range(rrsize))
    if(len(dorder) == 1):
        drawCcs(draw, rlist, slist[0] , llist[0], color_3,color_4)
    else:
        for i in range(rrsize - 1):
            for j in range(rrsize - i - 1):
                check = lapcheck(rrlist[dorder[rrsize - j -1]],rrlist[dorder[rrsize - j - 2]])
                if(check == 1):
                    dorder[rrsize - j -2],dorder[rrsize - j - 1] = dorder[rrsize - j - 1],dorder[rrsize - j -2]
        for order in dorder:
            drawCcs(draw, rlist, slist[order] , llist[order], color_3,color_4)








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
slist1 = ((0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7))
llist1=()
llist2 = ()
#llist1 = ((2,1),(2,3),(0,4),(1,5),(2,6),(3,7),(4,5),(4,7),(5,6),(6,7))
slist2 = ((12,13,1,15),(2,15,14,3),(8,9,10,11),(8,9,13,12),(9,10,0,13),(10,11,14,0),(11,8,12,14))
#llist2 = ((8,9),(9,10),(10,11),(11,8),(8,12),(9,13),(10,0),(11,14),(12,13),(13,1),(12,14),(14,3))
slist = []
llist = []
slist.append(slist1)
llist.append(llist1)
slist.append(slist2)
llist.append(llist2)

for i in range(step):
    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)

    drlist = observe(ro,rlist)
    for j in range(len(drlist)):
        drlist[j] = O + drlist[j]
    print(i)
    draw3d(draw, drlist, slist ,llist, color_3,color_4)
    #szahyoudraw(draw,ro,depth,color_2,color_2,color_2)
    images.append(im)

    ro = ro + v


images[0].save(R'C:\Users\nishi\python\hobby\output\3dshape.gif',save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)
