from PIL import Image, ImageDraw
from numpy import array, floor, cos, sin, pi,sqrt
import matplotlib.pyplot as plt
from numpy.linalg import solve

images = []

width = 1000
center = width // 2
O = array([center,center,0.5])
color_1 = (0, 0, 0)
color_2 = (0, 255, 255)
color_3 = (0, 255, 255)

step = 500
theta = array([110,110,80,80]) *  pi / 180
omega = array([0, 0, 0, 0])*  pi / 180
l = (4,2)
lv = (200,200)
al = lv[0] + lv[1]
m = (2, 2)
g = 1
dt =0.1

A1 = (m[0] + 4 * m[1])*l[0] ** 2 + 2 / 3 * m[0] * l[0] ** 2
A2 = m[1] * l[1] ** 2 + 2 / 3 * m[1] * l[1] ** 2
B = 2 * m[1] * l[0] * l[1]

def line3d(draw, r1, r2, color):#r1=(x座標，y座標，色の濃さ)
    n = 1000
    w = 2
    dr = (r2 - r1) / n
    rs = sqrt(dr[0]**2+dr[1]**2)
    for i in range(n):
        r = (r1 + i * dr)
        c = (int(floor(r[2] * color[0])),int(floor(r[2] * color[1])),int(floor(r[2] * color[2])))
        draw.line((r[0] - w*dr[1]/rs, r[1] + w*dr[0]/rs, r[0] + w*dr[1]/rs, r[1] - w*dr[0]/rs), fill=c)

def force(theta, omega):
    ccc = cos(theta[0]) * cos(theta[1]) * cos(theta[2] - theta[3])
    ccs = cos(theta[0]) * cos(theta[1]) * sin(theta[2] - theta[3])
    csc = cos(theta[0]) * sin(theta[1]) * cos(theta[2] - theta[3])
    css = cos(theta[0]) * sin(theta[1]) * sin(theta[2] - theta[3])
    scc = sin(theta[0]) * cos(theta[1]) * cos(theta[2] - theta[3])
    scs = sin(theta[0]) * cos(theta[1]) * sin(theta[2] - theta[3])
    ssc = sin(theta[0]) * sin(theta[1]) * cos(theta[2] - theta[3])
    sss = sin(theta[0]) * sin(theta[1]) * sin(theta[2] - theta[3])
    ss = sin(theta[0]) * sin(theta[1])
    cs = cos(theta[0]) * sin(theta[1])
    sc = sin(theta[0]) * cos(theta[1])

    A = array([[A1, B*(ccc+ss), 0, -B*css], [B*(ccc+ss), A2, B*scs, 0], [0, B*scs, A1*sin(theta[0])**2, B*ssc], [-B*css, 0, B*ssc, A2*sin(theta[1])**2]])
    q1 = A1*sin(theta[0])*cos(theta[0])*omega[2]**2 + B*( 2*ccs*omega[2]*omega[1] + 2*csc*omega[2]*omega[3] + (csc-sc)*omega[1]**2 - csc*omega[2]**2) - (m[0]+2*m[1])*g*l[0]*sin(theta[0])
    q2 = A2*sin(theta[1])*cos(theta[1])*omega[3]**2 + B*(-2*ccs*omega[0]*omega[3] + 2*scc*omega[2]*omega[3] + (scs-cs)*omega[0]**2 + ssc*omega[3]**2) - m[1]*g*l[1]*sin(theta[1])
    q3 =  2*A1*sin(theta[0])*omega[0]*omega[2] + B*(-2*ccs*omega[0]*omega[1] -2*css*omega[0]*omega[3] + sss*(-omega[1]**2 + omega[3]**2))
    q4 = -2*A2*sin(theta[1])*omega[1]*omega[3] + B*( 2*ccs*omega[0]*omega[1] -2*scc*omega[2]*omega[1] + sss*(-omega[0]**2 + omega[2]**2))
    d = [q1, q2, q3, q4]
    result = array(solve(A, d))
    print(A, d, result)
    return result

def kutta(theta, omega):
    kt1 = omega
    ko1 = force(theta, omega)
    kt2 = omega + ko1 / 2
    ko2 = force(theta + kt1 / 2, omega + ko1 / 2)
    kt3 = omega + ko2/ 2
    ko3 = force(theta + kt2 / 2, omega + ko2 / 2)
    kt4 = omega + ko3
    ko4 = force(theta + kt3, omega + ko3)
    theta = theta + (kt1 + kt2 * 2 + kt3 * 2 + kt4) * dt / 6
    omega = omega + (ko1 + ko2 * 2 + ko3 * 2 + ko4) * dt / 6
    return theta, omega


for i in range(step):
    c = kutta(theta, omega)
    theta = c[0]
    omega = c[1]

    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)

    r1 = O
    r2 = array((center + lv[0] * sin(theta[0]) * sin(theta[2]), center + lv[0] * cos(theta[0]), (al + lv[0] * sin(theta[0]) * sin(theta[2])) / al))
    r3 = array((r2[0] + lv[1] * sin(theta[1]) * sin(theta[3]), r2[1] + lv[1] * cos(theta[1]), (al + lv[0] * sin(theta[0]) * sin(theta[2]) +  lv[1] * sin(theta[1]) * sin(theta[3])) / al))

    print(i)

    line3d(draw, r1 , r2, color_2)
    line3d(draw, r2 , r3, color_2)

    images.append(im)


images[0].save(R'C:\Users\nishi\python\hobby\output\furiko3d.gif',
              save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
