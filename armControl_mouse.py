import math
import numpy as np
from scipy.signal import butter, lfilter
import serial
import pygame as pg, pygamebg


global width, height, L
(width, height) = [1000,500]
L = (.75 * width)/2

global origin, pos, old_pos, elbow_pos, end_theory, click_start, moving, direction
origin = np.array([0,height/2])
start_pos = np.array([2*L,height/2])
pos=old_pos=click_start = start_pos
moving=moving1=moving2 = False
direction = 1

global angles, step, lp_len
lp_len = 30
angles = [[0,0]] * lp_len
step = 0


def get_elbow_ik(pos, direction):
    global origin, width, height, L

    x = pos[0]
    y = height/2-pos[1]
    r = (x**2 + y**2)**(.5)

    theta0 = math.atan(y/x)
    theta1 = direction * (theta0 + math.acos(r/(2*L)))

    elbow_x = origin[0] + L*math.cos(theta1)
    elbow_y = origin[1] + L*math.sin(theta1)
    elbow_pos = np.array([elbow_x,elbow_y])

    forearm = np.add(pos, -1 * elbow_pos)
    theta2 = math.atan2(forearm[1],forearm[0])
    #theta2 = math.atan2(pos[1]-(origin[1]+L*math.sin(theta1)),pos[0]-(origin[0]+L*math.cos(theta1)))
    end_theory = np.array([elbow_pos[0] + L*math.cos(theta2), elbow_pos[1] + L*math.sin(theta2)])

    return elbow_pos, end_theory, theta1, theta2


def realize(ser):
    global angles, lp_len, step
    angle = np.sum(angles,0)/lp_len
    angleString = "<0," + str(-1 * angle[0] * 180 / math.pi) + "," + str(angle[1] * 180 / math.pi) + ">"
    print(angleString)
    ser.write(bytes(angleString, 'utf-8'))


def clamp(pos1, pos2, limit, mode, tolerance=.999):
    vec = np.add(pos2, -1*pos1)
    d = np.linalg.norm(vec)

    if mode == "min" and d <= limit * tolerance:
        vec = vec/d
        pos2 = pos1 + limit * vec * tolerance

    if mode == "max" and d >= limit * tolerance:
        vec = vec/d
        pos2 = pos1 + limit * vec * tolerance

    return pos2


def draw_circles(canvas, locs):
    for loc in locs:
        pg.draw.circle(canvas,"white",loc,10)

canvas = pygamebg.open_window(width, height, "Arm Control")
font = pg.font.SysFont('Arial',12,bold=True)
elbow_pos, end_theory, angles[step][0], angles[step][1] = get_elbow_ik(pos,direction)

global ser
#ser = serial.Serial('COM6', 9600)


def new_frame():
    global pos, old_pos, elbow_pos, end_theory, click_start, moving, moving1, moving2, direction, ser, angles, mode

    canvas.fill(pg.Color("black"))
    mouse_pos = np.array(pg.mouse.get_pos())
    click_L, click_M, click_R = pg.mouse.get_pressed()

    if click_L and not moving:
        old_pos = pos
        click_start = mouse_pos
        moving = True

    if moving:
        pos = np.add(old_pos,np.add(mouse_pos,-1*click_start))
        pos = clamp(origin, pos, L * 2, "max")
        elbow_pos, end_theory, angles[step][0], angles[step][1] = get_elbow_ik(pos, direction)
        direction = ((elbow_pos[1] > pos[1] and np.linalg.norm(pos) > .99*L) - .5) * 2
        pos = clamp(elbow_pos, pos, L, "min")
        pos = clamp(elbow_pos, pos, L, "max")

    if click_R:
        pos = start_pos
        elbow_pos, end_theory, angles[step][0], angles[step][1] = get_elbow_ik(pos, 1)

    if not click_L:
        moving = False
        angles[step] = angles[step-1]

    draw_circles(canvas, [origin, pos, elbow_pos])
    pg.draw.lines(canvas, "white", False, [origin,elbow_pos,pos],width=4)
    pg.draw.circle(canvas, "white", origin, 2 * L, width=4)
    pg.draw.circle(canvas, "red", end_theory,5)

    img1 = font.render(str(round(angles[step][0] * 180/math.pi,2)) + u'\N{DEGREE SIGN}', True, "white", "black")
    img2 = font.render(str(round(angles[step][1] * 180/math.pi,2)) + u'\N{DEGREE SIGN}', True, "white", "black")
    canvas.blit(img1, [.2 * (elbow_pos[0] - origin[0]) + origin[0],.2 * (elbow_pos[1] - origin[1]) + origin[1] + 50])
    canvas.blit(img2, [elbow_pos[0] - img2.get_width()/2,elbow_pos[1]+50])

    print(angles[step][0]*180/math.pi, angles[step][1]*180/math.pi)

    #realize(ser)



pygamebg.frame_loop(30, new_frame)