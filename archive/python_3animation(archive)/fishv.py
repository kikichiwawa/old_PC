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

step = 2000

N = 30

def list2center(list):
    if(len(list) == 0):
        return np.array([0,0])
    center = np.array([0,0])
    for index in list:
        center = center + fishlist[index].r
    return center / len(list)

def list2rad(list):
    if(len(list) == 0):
        return np.array([0,0])
    radsum = 0
    for index in list:
        radsum += fishlist[index].rad
    rad = radsum / len(list)
    return np.array([np.cos(rad), np.sin(rad)])

class fish:
    qlist = [[10,0], [-5, -5],[-5,5]] #三角形の座標
    speed = 40
    dt= 0.1

    rA = 10
    rB = 60
    rC = 120

    mA = 2
    mB = 2
    mC = 2
    mW = 10

    r = v = vA = vB = vC = vWall = np.array([0,0])
    rad = 0

    def radupdate(self):
        self.rad = np.arctan(self.v[1]/self.v[0])
        if(self.v[0] < 0):
            self.rad = self.rad + np.pi

    def vupdate(self):
        newv = (self.v + self.mA * self.vA + self.mB * self.vB + self.mC * self.vC + self.mW * self.vWall)
        self.v = newv * self.speed/np.linalg.norm(newv)

    def __init__(self, r, v):
        self.r = r
        self.v = v * self.speed / np.linalg.norm(v)
        self.radupdate()

    def check(self, r):
        dr = np.linalg.norm(r - self.r)
        if(dr < self.rA):
            return "A"
        elif(dr < self.rB):
            return "B"
        elif(dr < self.rC):
            return "C"

    def move(self, checklist):
        self.moveA(checklist[0])
        self.moveB(checklist[1])
        self.moveC(checklist[2])
        self.moveWall()

        self.update()

    #以下のA～Cは仮設計の状態である
    def moveA(self, list):
        if(len(list) == 0):
            self.vA = np.array([0,0])
        else:
            buff = self.r - list2center(list)
            self.vA = buff / np.linalg.norm(buff)

    def moveB(self, list):
        if(len(list) == 0):
            self.vB = np.array([0,0])
        else:
            buff = list2rad(list)
            self.vB = buff / np.linalg.norm(buff)

    def moveC(self, list):
        if(len(list) == 0):
            self.vC = np.array([0,0])
        else:
            buff = list2center(list) - self.r
            self.vC = buff / np.linalg.norm(buff)

    def moveWall(self):
        vwall = np.array([0,0])
        check = True
        if(self.r[0] <= self.rA):
            vwall = vwall + np.array([1,0])
            check = False
        elif(self.r[0] >= width - self.rA):
            vwall = vwall + np.array([-1,0])
            check = False
        if(self.r[1] <= self.rA):
            vwall = vwall + np.array([0,1])
            check = False
        elif(self.r[1] >= width - self.rA):
            vwall = vwall + np.array([0,-1])
            check = False
        if(check):
            self.vWall =  vwall
            return
        self.vWall =  vwall / np.linalg.norm(vwall)

    def update(self):
        self.vupdate()
        self.r = self.r + self.dt * self.v
        self.radupdate()

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

    for i in range(N):
        Alist = Blist = Clist = []

        for j in range(i + 1, N):
            result = fishlist[i].check(fishlist[j].r)
            if(result == "A"):
                Alist.append(j)
            elif(result == "B"):
                Blist.append(j)
            elif(result == "C"):
                Clist.append(j)
        checklist.append(list((Alist,Blist,Clist)))

    return checklist

fishlist = generatefish(N)
checklist = []

for i in range(0, step):
    for j in range(N):
        fishlist[j].move(checklist[j])
        fishlist[j].draw(draw)


    if(i%5 == 0):
        im = Image.new('RGB', (width, width), color_1)
        draw = ImageDraw.Draw(im)
        checklist = check(fishlist)
        images.append(im)

images[0].save(R'C:\Users\nishi\pp-python\hobby\output\fishv.gif',
              save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
"""
fig, ax = plt.subplots(facecolor="w")


ax.legend(["A", "B"])
ax.plot(list(range(0, step)), Wc, label = "Wall")
ax.plot(list(range(0, step)), Ac, label = "A")
ax.plot(list(range(0, step)), Bc, label = "B")
ax.plot(list(range(0, step)), Cc, label = "C")
ax.legend(["Wall", "A", "B", "C"])
plt.show()
"""
