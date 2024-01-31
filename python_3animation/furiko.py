from PIL import Image, ImageDraw
import math, numpy as np
import matplotlib.pyplot as plt

images = []
imagesf = []

width = 200
center = width // 2
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
color_3 = (0, 255, 255)

step = 10000
l = np.array([50, 50])
m = np.array([1, 1])
g = 1
dt = 1

a1 = (5 / 3 * m[0] + 4 * m[1]) * l[0] ** 2
a2 = 2 * m[0] * l[0] * l[1]
a3 = (m[0] + 2 * m[1]) * g * l[0]
b1 = 2 * m[1] * l[0] * l[1]
b2 = 5 / 3 * m[1] * l[1] ** 2
b3 = m[1] * g * l[1]

def energy(theta, omega):
    K = (a1 * omega[0] ** 2 + b2 * omega[1] ** 2) / 2 + b1 * math.cos(theta[0] - theta[1]) * omega[0] * omega[1]
    U = a3 * (1 - math.cos(theta[0])) + b3 * (1 - math.cos(theta[1]))
    return K + U

def force(theta, omega):
    Ai = np.array([[b2, -a2 * math.cos(theta[0] - theta[1])],[-b1 * math.cos(theta[0] - theta[1]), a1]])
    x = np.array([-a2 * math.sin(theta[0] - theta[1]) * omega[1] ** 2 - a3 * math.sin(theta[0]), b1 * math.sin(theta[0] - theta[1]) * omega[0] ** 2 - b3 * math.sin(theta[1])])
    f = np.dot(Ai, x) / (a1 * b2 - a2 * b1 * math.cos(theta[0] - theta[1] ** 2))
    return f

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

#def flog(theta, omega):

theta = np.array([90, 90]) * 2 * math.pi / 360
omega = np.array([0, 0])
E1 = []

for i in range(0, step):
    c = kutta(theta, omega)
    theta = c[0]
    omega = c[1]
    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)
    draw.line((center, center , center + l[0] * math.sin(theta[0]), center + l[0] * math.cos(theta[0])), fill=color_2, width = 3)
    draw.line((center + l[0] * math.sin(theta[0]), center + l[0] * math.cos(theta[0]), center + l[0] * math.sin(theta[0]) + l[1] * math.sin(theta[1]), center + l[0] * math.cos(theta[0]) + l[1] * math.cos(theta[1])), fill=color_2, width = 3)
    images.append(im)
    E1.append(energy(theta, omega))

theta = np.array([90, 91]) * 2 * math.pi / 360
omega = np.array([0, 0])
E2 = []

for i in range(0, step):
    c = kutta(theta, omega)
    theta = c[0]
    omega = c[1]
    im = images[i]
    draw = ImageDraw.Draw(im)
    draw.line((center, center , center + l[0] * math.sin(theta[0]), center + l[0] * math.cos(theta[0])), fill=color_3, width = 3)
    draw.line((center + l[0] * math.sin(theta[0]), center + l[0] * math.cos(theta[0]), center + l[0] * math.sin(theta[0]) + l[1] * math.sin(theta[1]), center + l[0] * math.cos(theta[0]) + l[1] * math.cos(theta[1])), fill=color_3, width = 3)
    images.append(im)
    E2.append(energy(theta, omega))

images[0].save("./output/furiko2D.gif",
              save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

plt.plot(list(range(0, step)), E1)
plt.plot(list(range(0, step)), E2)
plt.show()
