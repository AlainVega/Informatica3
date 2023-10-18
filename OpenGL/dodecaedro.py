# Crear un dodecaedro, a partir de una sola cara. 
# Luego ver para agregar lo de mover con el teclado.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800
ojox, ojoy, ojoz = 1.2, 0.8, 2

# Sirve para dibujar la cara del poligono (Pentagono)
def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLE_FAN) # dibuja triangulos para simular el pentagono.
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

# Sirve para dibujar rectas.
def recta(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINES) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar el dodecaedro.
def dodecaedro():
    vertices = []
    p = 0.2 # paramtetro para definir el ancho y alto de las caras
    angulo = 30 # angulo comun 
    v = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    # PENTAGONO REGULAR formado con triangulos.
    # Pentagono base (primero el centro, luego los vertices en sentido antihorario)
    # (p/2, pSIN(2pi/5), 0), (0, 0, 0), (p, 0, 0), (p+pCOS(2pi/5), pSIN(2pi/5), 0), (p/2, 2p, 0), (-pCOS(2pi/5), pSIN(2pi/5), 0)
    r = p/(2*math.cos(3*math.pi/10))
    a, b, h = p*math.cos(2*math.pi/5), p*math.sin(2*math.pi/5), (p*math.tan(3*math.pi/10))/2
    vertices.append((p/2, h, 0)) # centro del pentagono
    vertices.append((0, 0, 0)) # vertice 1
    vertices.append((p, 0, 0)) # vertice 2
    vertices.append((p+a, b, 0)) # vertice 3
    vertices.append((p/2, h+r, 0)) # vertice 4
    vertices.append((-a, b, 0)) # vertice 5
    vertices.append((0, 0, 0)) # vertice 6 (para cerrar el abanico de triangulos.)

    # v.append((p, 0, 0))
    # v.append((p+a, b, 0))

    # recta(v, (1, 0.52, 0))

    # m = (0-b)/(p - p+a)
    # alpha = math.atan(m)
    # beta = alpha*(180/math.pi)

    # print(beta)

    # Pentagono trasero gris
    glPushMatrix()
    cara(vertices, (0.4, 0.4, 0.4)) 
    glPopMatrix()

    # glPushMatrix()
    # glTranslate(-p, 0, 0)
    # recta(v, (1, 0.52, 0))
    # glPopMatrix()

    # Petagono de abajo verde
    glPushMatrix()
    glRotate(180, 1, 0, 0) # rota en x
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Pentagono de la izquierda rojo
    glPushMatrix()
    glRotate(108, 0, 0, 1) # rota en z
    cara(vertices, (0.8, 0, 0))
    glPopMatrix()

    # Pentagono de la derecha azul
    glPushMatrix()
    glTranslate(p, 0, 0) # destraslada en x
    glRotate(-108, 0, 0, 1) # rota en z
    glTranslate(-p, 0, 0) # traslada  en x
    cara(vertices, (0, 0, 0.8))
    glPopMatrix()
 
    # Pentagono de arriba izq naranja
    glPushMatrix()
    glTranslate(p/2, 0, 0) # traslada en x
    glTranslate(0, h+r, 0) # traslada en y
    glRotate(324, 0, 0, 1) # rota en z
    cara(vertices, (1, 0.52, 0))
    glPopMatrix()

    # Pentagono de arriba derecha 
    glPushMatrix()
    glTranslate(-a, 0, 0)  # traslada en x
    glTranslate(0, b, 0) # traslada en y 
    glRotate(36, 0, 0, 1) # rota en z
    cara(vertices, (0.8, 0.2, 0.5))
    glPopMatrix()

    # # Triangulo izquierdo amarillo
    # glPushMatrix()
    # glRotate(-angulo, 0, 0, 1)
    # glRotate(-90, 0, 1, 0) #rota en y
    # cara(vertices, (0.7, 0.7, 0.1))
    # glPopMatrix()

    # # Triangulo frontal celeste (DESCOMENTAR)
    # glPushMatrix()
    # glTranslate(0, 0, p) # trasladar p unidades en z
    # glRotate(-angulo, 1, 0, 0)
    # cara(vertices, (0.2, 0.4, 0.8))
    # glPopMatrix()    

    glFlush() # Para forzar a que pinte.
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

    dodecaedro()

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    # Borrar la pantalla
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Dodecaedro") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    # glutIdleFunc(display) # Mantiene la ventana abierta
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    

main()