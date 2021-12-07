from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w, h = 1000, 1000


def buildCenterPosList(num, initX, initY, offsetX, offsetY):
    return [[initX + i * offsetX, initY + i * offsetY] for i in range(0, num)]


def square(center, length, r, g, b):
    centerX = center[0]
    centerY = center[1]
    hlen = length / 2

    # begin drawing square
    glColor3f(r, g, b)                                  # define colour
    glBegin(GL_QUADS)
    glVertex2f(centerX - hlen, centerY - hlen)          # bottom left
    glVertex2f(centerX + hlen, centerY - hlen)          # bottom right
    glVertex2f(centerX + hlen, centerY + hlen)          # top right
    glVertex2f(centerX - hlen, centerY + hlen)          # top left
    glEnd()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)                        # clean screen
    glLoadIdentity()                                    # reset graphic position
    glOrtho(0 - w / 2, w / 2, 0 - h / 2, h / 2, 0, 1)   # define coord system

    # colours (in r, g, b)
    clr_server = 0.75, 0.15, 1.55
    clr_customer = 0.1, 0.4, 0.4

    # server init pos
    pos_s = buildCenterPosList(2, -250, -250, 0, 500)

    # draw servers
    for s in pos_s:
        square(s, 300, *clr_server)

    # draw customer queue
    pos_q = buildCenterPosList(3, 0, 250, 150, 0)
    pos_q = pos_q + \
            buildCenterPosList(3, 0, -250, 150, 0)

    for q in pos_q:
        square(q, 100, *clr_customer)

    glutSwapBuffers()                                   # bring up new buffer


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()