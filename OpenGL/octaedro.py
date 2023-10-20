# Crear un octaedro u octoedro, a partir de una sola cara. 
# Luego ver para agregar lo de mover con el teclado.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800
x0, y0, z0 = 1.2, 0.8, 2 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio)
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
angulo = 30 # angulo comun (Se controla con 'j' y 'l')
beta = 0 # angulo de giro de la figura entera (Se controla con 'n' y 'm')

# Sirve para dibujar las caras de los poligonos (triangulos)
def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLES) # dibuja triangulos
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

# Sirve para dibujar el octaedro.
def octaedro():
    vertices = [] # lista de vertices.
    p = 0.3 # parametro para definir los vertices.
    # angulo = 30 # angulo comun de rotacion para formar el pico del octaedro.

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    # Triangulo base (0, 0, 0), (p, 0, 0), (p/2, p, 0)
    vertices.append((0, 0, 0))
    vertices.append((p, 0, 0))
    vertices.append((p/2, p, 0))

    glRotate(beta, 0, 1, 0)

    # Triangulo trasero gris
    glPushMatrix()
    glRotate(angulo, 1, 0, 0) # rota en x
    cara(vertices, (0.4, 0.4, 0.4)) 
    glPopMatrix()

    # Triangulo trasero de abajo verde
    glPushMatrix()
    glRotate(180-angulo, 1, 0, 0) #rota en x
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Triangulo derecho de abajo rojo
    glPushMatrix()
    glTranslate(p, 0, 0) # trasladar p unidades en x
    glRotate(-angulo, 0, 0, 1) # rota en z
    glRotate(-90, 0, 1, 0) # rota en y
    glRotate(180, 1, 0, 0) # rota en x
    cara(vertices, (0.8, 0, 0))
    glPopMatrix()

    # Triangulo izquierdo de abajo azul
    glPushMatrix()
    glRotate(angulo, 0, 0, 1) # rota en z
    glRotate(-90, 0, 1, 0) # rota en y
    glRotate(180, 1, 0, 0) # rota en x
    cara(vertices, (0, 0, 0.8))
    glPopMatrix()
 
    # Triangulo frontal de abajo naranja (DESCOMENTAR PARA VER EL OCTAEDRO COMPLETO)
    glPushMatrix()
    glTranslate(0, 0, p) # trasladar p unidades en z
    glRotate(180+angulo, 1, 0, 0) #rota en x
    cara(vertices, (1, 0.52, 0))
    glPopMatrix()

    # Triangulo derecho rosado
    glPushMatrix()
    glTranslate(p, 0, 0) # trasladar p unidades en x
    glRotate(angulo, 0, 0, 1) # rota en z
    glRotate(-90, 0, 1, 0) # rota en y
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Triangulo izquierdo amarillo
    glPushMatrix()
    glRotate(-angulo, 0, 0, 1) # rota en z
    glRotate(-90, 0, 1, 0) # rota en y
    cara(vertices, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Triangulo frontal celeste (DESCOMENTAR PARA VER EL OCTAEDRO COMPLETO)
    glPushMatrix()
    glTranslate(0, 0, p) # trasladar p unidades en z
    glRotate(-angulo, 1, 0, 0) # rota en x
    cara(vertices, (0.2, 0.4, 0.8))
    glPopMatrix()    

    glFlush() # para forzar a que pinte.
    # glFinish()

# Para dibujar los ejes de coordenadas.
def ejes():
    largo = 2
    glBegin(GL_LINES) # Contexto lineas
    # Eje X (ROJO)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)
    # Eje Y (VERDE)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)
    # Eje Z (AZUL)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, largo)

    glEnd() # Fin contexto lineas


# Funcion de pintar
def display():
    # global ojox, ojoy, ojoz
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Selecciona la matriz de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Inicializar la matriz.

    # Ángulo, ratio, near, far
    gluPerspective(35, alto/ancho, 0.1, 10.0)

    # Seleccionar la matriz modelview
    glMatrixMode(GL_MODELVIEW)

    # Inicializar la matriz.
    glLoadIdentity()

    # Desde, Hacia, Dirección arriba
    #ojox += 0.2
    gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

    octaedro()

# Captura las teclas 'w', 'a', 's' y 'd' para mover la camara en una esfera centrada en el origen.
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

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    # Borrar la pantalla
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Octaedro") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    # glutIdleFunc(display) # Mantiene la ventana abierta
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    

main()