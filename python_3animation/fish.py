from PIL import Image, ImageDraw
import math, numpy as np
import matplotlib.pyplot as plt
from random import random

images = []
imagesf = []

width = 1000
center = width // 2
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
color_3 = (0, 255, 255)

step = 250

N = 25


class fish:
    qlist = [[10,0], [-5, -5],[-5,5]] #三角形の座標
    k = 0.3
    Ma = 500
    dt= 0.1

    rA = 3
    rB = 10
    rC = 100

    r = v = a = np.array([0,0])
    rad = 0

    def v2rad(self,v):
        rad = np.arctan(v[1]/v[0])
        if(v[0] < 0):
            rad = rad + np.pi
        return rad

    def __init__(self, r, v):
        self.r, self.v = r, v
        self.a = np.array([0,0])
        self.rad = self.v2rad(self.v)

    def check(self, r):
        dr = np.linalg.norm(r - self.r)
        if(dr < self.rA):
            return "A"
        elif(dr < self.rB):
            return "B"
        elif(dr < self.rC):
            return "C"

    def move(self, checklist):
        Wall = checklist[0]
        Alist = checklist[1]
        Blist = checklist[2]
        Clist = checklist[3]

        #以下の部分で加速度aを決定する
        if(Wall != None):
            self.moveWall(Wall)
        elif(Alist != []):
            self.moveA(Alist)
        elif(Blist != []):
            self.moveB(Blist)
        elif(Clist != []):
            self.moveC(Clist)
        else:
            self.a = np.array([random(),random()])*self.Ma/10

        self.update()

    #以下のA～Cは仮設計の状態である

    def moveWall(self, Wall):

        if(Wall == "Left"):
            self.a = np.array(([self.Ma,0]))
        elif(Wall == "Right"):
            self.a = np.array(([-self.Ma,0]))
        elif(Wall == "Roof"):
            self.a = np.array(([0,self.Ma]))
        else:
            self.a = np.array(([0,-self.Ma]))

    def moveA(self,list):
        re = np.array([0,0])
        for index in list:
            dr = fishlist[index].r - self.r
            norm = np.linalg.norm(dr)
            re = re + dr*(self.rA - norm)/(norm + 0.1)
        norm2 = np.linalg.norm(re)
        self.a = min(norm2, self.Ma)*re/norm2
    def moveB(self,list):
        sumrad = 0
        n = 0
        for index in list:
            radsum = radsum + fishlist[index].rad
            n = n + 1
        randave = randsum / n
        self.a = self.Ma * np.array([cos(randave),cos(rand(ave))]) *(0.7 + 0.3*cos((radave - self.rad)/2))

    def moveC(self,list):
        sumr = np.array([0,0])
        n = 0
        for index in list:
            rsum = rsum + fishlist[index].r
            n = n + 1
        rave = rsum / n
        dr = rave - self.r
        norm = np.linalg.norm(dr)
        self.a = min(dr, self.Ma)*dr/norm

    def update(self):
        self.v = self.v*(1 - self.k*self.dt) + self.dt * self.a
        self.r = self.r + self.dt * self.v
        self.rad = self.v2rad(self.v)
        self.r = self.r % width

    def draw(self,draw):
        rlist = []
        Cos, Sin = np.cos(self.rad), np.sin(self.rad)
        x, y = self.r
        for q in self.qlist:
            rlist.append([x + Cos*q[0] - Sin*q[1], y + Sin*q[0] + Cos*q[1]])
        trir = ((rlist[0][0],rlist[0][1]),(rlist[1][0],rlist[1][1]),(rlist[2][0],rlist[2][1]))
        draw.polygon(trir, fill = color_2, outline = color_2)

def generatefish(N):
    fishlist = []
    for i in range(N):
        r = np.array([random(),random()]) * width
        v = np.array([random()-0.5,random()-0.5]) * 10
        fishlist.append(fish(r, v))
    return fishlist

def check(fishlist):
    checklist = []
    count = [0, 0, 0, 0]

    for i in range(N):
        Wall = None
        Alist = Blist = Clist = []

        if(fishlist[i].r[0] < fish.rA):
            Wall = "Left"
            count[0] = count[0] + 1
        elif(fishlist[i].r[1] < fish.rA):
            Wall = "Roof"
            count[0] = count[0] + 1
        elif(fishlist[i].r[0] > width - fish.rA):
            Wall = "Right"
            count[0] = count[0] + 1
        elif(fishlist[i].r[1] > width - fish.rA):
            Wall = "Floor"
            count[0] = count[0] + 1

        if(True):
            for j in range(i + 1, N):
                result = fishlist[i].check(fishlist[j].r)
                if(result == "A"):
                    Alist.append(j)
                    count[1] = count[1] + 1
                elif(result == "B"):
                    Blist.append(j)
                    count[2] = count[2] + 1
                elif(result == "C"):
                    Clist.append(j)
                    count[3] = count[3] + 1
        checklist.append(list((Wall,Alist,Blist,Clist)))

    return checklist, count

fishlist = generatefish(N)
checklist = []
Wc, Ac, Bc, Cc = [],[],[],[]

for i in range(0, step):
    print(i)
    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)
    checklist, result = check(fishlist)
    Wc.append(result[0])
    Ac.append(result[1])
    Bc.append(result[2])
    Cc.append(result[3])

    for j in range(N):
        fishlist[j].move(checklist[j])
        fishlist[j].draw(draw)

    images.append(im)

images[0].save(R'C:\Users\nishi\pp-python\hobby\output\fish.gif',
              save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

fig, ax = plt.subplots(facecolor="w")


ax.legend(["A", "B"])
ax.plot(list(range(0, step)), Wc, label = "Wall")
ax.plot(list(range(0, step)), Ac, label = "A")
ax.plot(list(range(0, step)), Bc, label = "B")
ax.plot(list(range(0, step)), Cc, label = "C")
ax.legend(["Wall", "A", "B", "C"])
plt.show()
