# Rotar sobre una recta cualquiera en el espacio 3D

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800
ojox, ojoy, ojoz = 1.2, 0.8, 2

# Dibuja la cara del poligono con color.
def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLE_FAN) # dibuja triangulos para simular el pentagono.
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

# Dibuja una recta con color.
def recta(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINES) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

def rotarSobreLinea():
    vertices = []
    p = 0.2 # paramtetro para definir el ancho y alto de las caras
    angulo = 30 # angulo comun 
    v = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    vertices.append((-0.6, 0.2, 0))
    vertices.append((-0.2, 0.5, 0))
    vertices.append((-0.4, 0.7, 0))

    # Triangulo (base) gris
    glPushMatrix()
    # glTranslate(a, 0, 0) # trasladar a unidades en x
    cara(vertices, (0.4, 0.4, 0.4)) 
    glPopMatrix()

    v.append((-0.2, 0, 0))
    v.append((0.1, 0.7, 0))

    # Eje de rotacion.
    recta(v, (1, 0.52, 0))


    # Triangulo (rotado) verde
    glPushMatrix()
    glTranslate(-0.2, 0, 0) # destrasladar
    # glRotate(-180, 1, 0, 0)
    # glRotate(-180, 0, 1, 0)
    # glRotate(180, 0, 0, 1)
    # glRotate(180, 0, 1, 0)
    glRotate(180, 0.1 + 0.2, 0.7, 0)
    glTranslate(0.2, 0, 0) # trasladar recta al origen.
    # recta(v, (0.1, 0.7, 0.2))
    cara(vertices, (0.1, 0.7, 0.2)) 
    glPopMatrix()

    glFlush() # Forzar a que pinte.
    # glFinish()

# Dibuja los ejes coordenados
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

    rotarSobreLinea()

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    # Borrar la pantalla
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Rotar sobre una recta cualquiera en 3D") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    # glutIdleFunc(display) # Mantiene la ventana abierta
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()