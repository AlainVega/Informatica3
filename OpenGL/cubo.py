from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

altura, ancho = 800, 800

x0, y0, z0 = 1.2, 0.8, 2 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio)
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
angulo = 90 # angulo comun (Se controla con 'j' y 'l')
beta = 0 # angulo de giro de la figura entera (Se controla con 'n' y 'm')


def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1)
    glBegin(GL_QUADS)
    for v in vertices:
        glVertex3fv(v)
    glEnd()


def display():
    global ojox, ojoy, ojoz
    glEnable(GL_DEPTH_TEST)
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
    # ojox += 0.2
    gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

    Cube()


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


def Cube():
    vertices = []
    ancho = 0.3
    z = 0
    # Inferior izquierdo
    vertices.append((0, 0, z))
    # Inferior derecho
    vertices.append((ancho, 0, z))
    # Superior derecho
    vertices.append((ancho, ancho, z))
    # Superior izquierdo
    vertices.append((0, ancho, z))

    square = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
    )

    ejes()

    glRotate(beta, 0, 1, 0) # para mover la figura en y (con teclas 'n' y 'm')

    # Cara izquierda #rosada
    glPushMatrix()
    glRotate(-angulo, 0, 1, 0)
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Cara inferior #amarillo
    glPushMatrix()
    glRotate(angulo, 1, 0, 0)
    cara(vertices, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Cara derecha #celeste
    glPushMatrix()
    glTranslatef(ancho, 0, 0)
    glRotate(-angulo, 0, 1, 0)
    cara(vertices, (0.2, 0.4, 0.8))
    glPopMatrix()

    # Cara frontal #verde
    glPushMatrix()
    glTranslatef(0, 0, ancho)
    # cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Cara superior #lila
    glPushMatrix()
    glTranslatef(0, ancho, 0)
    glRotate(angulo, 1, 0, 0)
    cara(vertices, (0.3, 0.1, 0.3))
    glPopMatrix()

    # Cara trasera #gris
    cara(vertices, (0.4, 0.4, 0.4))

    glFlush()


# Captura las teclas 'w', 'a', 's' y 'd' para mover la camara en una esfera centrada en el origen.
# Tambien las teclas 'j' y 'l' para mover el angulo comun de los lados.
# Tambien las teclas 'n' y 'm' para mover la figura entera respecto a y
# La tecla 'r' sirve para posicionar la camara en su inicio.
def buttons(key, x, y):
    global ojoz, ojox, ojoy, phi, teta, angulo, beta
    print(f'key={key}')
    match key:
        case b'd':
            phi -= 0.1
            ojoz = radio*math.sin(phi)
            ojox = radio*math.cos(phi)
            # ojoy = radio*math.cos(teta)
        case b'a':
            phi += 0.1
            ojoz = radio*math.sin(phi)
            ojox = radio*math.cos(phi)
            # ojoy = radio*math.cos(teta)
        case b'w':
            teta += 0.1
            ojoy = radio*math.sin(teta)
            ojoz = radio*math.cos(teta)
            # ojox = radio*math.cos(phi)
        case b's':
            teta -= 0.1
            ojoy = radio*math.sin(teta)
            ojoz = radio*math.cos(teta)
            # ojox = radio*math.cos(phi)
        case b'r':
            teta, phi = teta0, phi0
            ojox = x0
            ojoy = y0
            ojoz = z0
            print('La camara volvio a su posicion original.')
        case b'l':
            angulo += 4
            print(f'angulo = {angulo}')
        case b'j':
            angulo -= 4
            print(f'angulo = {angulo}')
        case b'n':
            beta += 1
        case b'm':
            beta -= 1
    glutPostRedisplay() # Dibuja otra vez.


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glDepthFunc(GL_LESS)
    glutInitWindowSize(altura, ancho)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Cubo 3D con rotación de caras")
    glutDisplayFunc(display)
    glutKeyboardFunc(buttons)
    glutMainLoop()


main()
