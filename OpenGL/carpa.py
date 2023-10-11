from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

altura, ancho = 800, 800

ojox, ojoy, ojoz = 0.8, 0.8, 2

# dibuja la cara.
def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1)
    glBegin(GL_TRIANGLES)
    for v in vertices:
        glVertex3fv(v)
    glEnd()


def display():
    global ojox, ojoy, ojoz
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Selecciona la matriz de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Inicializar la matriz.

    # Ángulo, ratio, near, far
    gluPerspective(35, altura/ancho, 0.1, 10.0)

    # Seleccionar la matriz modelview
    glMatrixMode(GL_MODELVIEW)

    # Inicializar la matriz.
    glLoadIdentity()

    # Desde, Hacia, Dirección arriba
    ojox += 0.2
    gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

    Triangulo()


def ejes():
    # Eje x
    largo = 2
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, largo)

    glEnd()


def Triangulo():
    vertices = []
    ancho = 0.8
    z = 0
    # Inferior izquierdo
    vertices.append((0, 0, z))
    # Inferior derecho
    vertices.append((ancho, 0, z))
    # Superior 
    vertices.append((ancho/2, ancho, z))
    # Superior izquierdo
    # vertices.append((0, ancho, z))

    square = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
    )

    ejes()

    angulo = 30

    # Cara trasera #gris
    #cara(vertices, (0.4, 0.4, 0.4))

    # Cara trasera #rosada
    glPushMatrix()
    glRotate(angulo, 1, 0, 0)
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Cara inferior #amarillo
    glPushMatrix()
    glRotate(-angulo, 0, 0, 1) #rota en z
    glRotate(-90, 0, 1, 0) #rota en y
    cara(vertices, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Cara derecha #celeste
    glPushMatrix()
    # glRotate(-angulo, 0, 0, 1) #rota en z
    glTranslatef(ancho, 0, 0) #move en x
    glRotate(angulo, 0, 0, 1) #rota en y
    glRotate(-90, 0, 1, 0) #rota en y
    cara(vertices, (0.2, 0.4, 0.8))
    glPopMatrix()

    # DESCOMENTAR
    # Cara frontal #verde
    # glPushMatrix()
    # glTranslatef(0, 0, ancho) #move en x
    # glRotate(-angulo, 1, 0, 0) #rota en x
    # cara(vertices, (0.1, 0.7, 0.2))
    # glPopMatrix()

    glFlush()


def buttons(key, x, y):
    global ojox
    print(f'key={key}')
    if key == b'a':
        ojox += 0.1


def main():
    glutInit(sys.argv)
    # glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(altura, ancho)
    # Borrar la pantalla
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glutInitWindowPosition(0, 0)
    glutCreateWindow("Carpa 3D")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
