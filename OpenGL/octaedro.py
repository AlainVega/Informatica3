# Crear un octaedro u octoedro, a partir de una sola cara. 
# Luego ver para agregar lo de mover con el teclado.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#variables globales
ancho, alto = 800, 800
ojox, ojoy, ojoz = 1.2, 0.8, 2

def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLES) # dibuja triangulos
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

def octaedro():
    vertices = []
    p = 0.3
    angulo = 30 

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    # Triangulo base (0, 0, 0), (p, 0, 0), (p/2, p, 0)
    vertices.append((0, 0, 0))
    vertices.append((p, 0, 0))
    vertices.append((p/2, p, 0))

    # Triangulo trasero gris
    glPushMatrix()
    glRotate(angulo, 1, 0, 0)
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
    glRotate(-angulo, 0, 0, 1)
    glRotate(-90, 0, 1, 0) #rota en y
    glRotate(180, 1, 0, 0) #rota en x
    cara(vertices, (0.8, 0, 0))
    glPopMatrix()

    # Triangulo izquierdo de abajo azul
    glPushMatrix()
    glRotate(angulo, 0, 0, 1)
    glRotate(-90, 0, 1, 0) #rota en y
    glRotate(180, 1, 0, 0) #rota en x
    cara(vertices, (0, 0, 0.8))
    glPopMatrix()
 
    # # Triangulo frontal de abajo naranja (DESCOMENTAR)
    # glPushMatrix()
    # glTranslate(0, 0, p) # trasladar p unidades en z
    # glRotate(180+angulo, 1, 0, 0) #rota en x
    # cara(vertices, (1, 0.52, 0))
    # glPopMatrix()

    # Triangulo derecho rosado
    glPushMatrix()
    glTranslate(p, 0, 0) # trasladar p unidades en x
    glRotate(angulo, 0, 0, 1)
    glRotate(-90, 0, 1, 0) #rota en y
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # Triangulo izquierdo amarillo
    glPushMatrix()
    glRotate(-angulo, 0, 0, 1)
    glRotate(-90, 0, 1, 0) #rota en y
    cara(vertices, (0.7, 0.7, 0.1))
    glPopMatrix()

    # # Triangulo frontal celeste (DESCOMENTAR)
    # glPushMatrix()
    # glTranslate(0, 0, p) # trasladar p unidades en z
    # glRotate(-angulo, 1, 0, 0)
    # cara(vertices, (0.2, 0.4, 0.8))
    # glPopMatrix()    

    glFlush() 
    # glFinish()

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
    # glutIdleFunc(display) # Mantiene la ventana abierta
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    

main()