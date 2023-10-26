# Utilizando PyOpenGL dibujar una mesa en 3D compuesta de prismas o poligonos.
# El color, la posicion inicial y las dimensiones de la mesa quedan a criterio
# del alumno. 
# Se debera ubicar una fuente de luz blanca en cualquier posicion y las teclas
# "asdw" deberan mover la fuente de luz en las direcciones 
# (izquierda, abajo, derecha y arriba, respectivamente). Las teclas "u y j" deberan rotar
# toda la mesa alrededor de cualquiera de las patas (queda a criterio del alumno
# alrededor de que pata rotar, siempre y cuando NO COINCIDA con ninguno de los ejes)
# Dibujar tambien los ejes de coordenadas.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 1.2, 0.8, 3 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
beta = 0
lightZeroPosition = [0.7, 0.4, 1.5, 0] # posicion de la fuente de luz
lightZeroColor = [1, 1, 0.6, 0] # color de la fuente de luz
rojo = [1, 0, 0, 1]
ambientColor = [0.7, 0.7, 0.3, 1] # tono de la luz ambiente
radio = 0.3
cantidadPuntas = 6
vertical, horizontal = 0,0
size = 1

# Sirve para dibujar la cara del poligono. (Pintar el ancho del mesa)
def cara(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_QUADS) # dibuja triangulos para simular el hexagono.
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

# Sirve para dibujar rectas.
def recta(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINE_STRIP) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar line loop.
def rectaLoop(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINE_LOOP) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar puntos
def punto(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_POINTS) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para definir la mesa.
def mesa():
    vertices = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario

    glRotate(beta, 0, 1, 0)
    # glTranslate(horizontal, vertical, 0)
    # glScale(size, size, 0)

    # Patas
    lado = 0.1
    alto = 0.3
    # Vertices para la pata en sentido anti horario.
    # Abajo
    v0 = (0, 0, 0) 
    v1 = (0, 0, -lado) 
    v2 = (-lado, 0, -lado)
    v3 = (-lado, 0, 0)
    # Arriba
    v4 = (0, alto, 0) 
    v5 = (0, alto, -lado) 
    v6 = (-lado, alto, -lado)
    v7 = (-lado, alto, 0)

    # rectaLoop([v0, v1, v2, v3], (0.5, 0.25, 0))
    # rectaLoop([v4, v5, v6, v7], (0.5, 0.25, 0))

    anchura, largor = 0.5, 1
    # Pata 1
    cara([v0, v4, v5, v1], (0.5, 0.25, 0))
    cara([v0, v4, v7, v3], (0.5, 0.25, 0))
    cara([v1, v5, v6, v2], (0.5, 0.25, 0))
    cara([v2, v6, v7, v3], (0.5, 0.25, 0))

    # Pata 2
    glPushMatrix()
    glTranslate(0, 0, largor)
    cara([v0, v4, v5, v1], (0.5, 0.25, 0))
    cara([v0, v4, v7, v3], (0.5, 0.25, 0))
    cara([v1, v5, v6, v2], (0.5, 0.25, 0))
    cara([v2, v6, v7, v3], (0.5, 0.25, 0))
    glPopMatrix()

    # Pata 3
    glPushMatrix()
    glTranslate(anchura, 0, largor)
    cara([v0, v4, v5, v1], (0.5, 0.25, 0))
    cara([v0, v4, v7, v3], (0.5, 0.25, 0))
    cara([v1, v5, v6, v2], (0.5, 0.25, 0))
    cara([v2, v6, v7, v3], (0.5, 0.25, 0))
    glPopMatrix()

    # Pata 4
    glPushMatrix()
    glTranslate(anchura, 0, 0)
    cara([v0, v4, v5, v1], (0.5, 0.25, 0))
    cara([v0, v4, v7, v3], (0.5, 0.25, 0))
    cara([v1, v5, v6, v2], (0.5, 0.25, 0))
    cara([v2, v6, v7, v3], (0.5, 0.25, 0))
    glPopMatrix()

    # Tablon
    t0 = (-lado, alto, -lado)
    t1 = (-lado, alto, largor)
    t2 = (anchura, alto, largor)
    t3 = (anchura, alto, -lado)

    t4 = (-lado, alto+lado, -lado)
    t5 = (-lado, alto+lado, largor)
    t6 = (anchura, alto+lado, largor)
    t7 = (anchura, alto+lado, -lado)

    # punto([t0, t1, t2, t3], (0, 1, 1))
    # punto([t4, t5, t6, t7], (0, 1, 1))

    rectaLoop([t0, t1, t2, t3], (0.5, 0.25, 0))
    rectaLoop([t4, t5, t6, t7], (0.5, 0.25, 0))

    cara([t1, t5, t6, t2], (0.5, 0.25, 0))
    cara([t2, t6, t7, t3], (0.5, 0.25, 0))
    cara([t0, t4, t5, t1], (0.5, 0.25, 0))
    cara([t0, t4, t7, t3], (0.5, 0.25, 0))

    cara([t4, t5, t6, t7], (0.5, 0.25, 0))

    glFlush() # Para forzar a que pinte.
    # glFinish()

# Para dibujar los ejes de coordenadas.
def ejes():
    largo = 100
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
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  

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
    gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

    mesa()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, horizontal, vertical, beta
    print(f'key={key}')
    match key:
        case b'r':
            vertical, horizontal, radio, cantidadPuntas = 0, 0, 0.3, 6
            print('La figura volvio a su tamanho y posicion inicial.')
        case b's':
            vertical -= 0.01
        case b'a':
            horizontal -= 0.01
        case b'w':
            vertical += 0.01
        case b'd':
            horizontal += 0.01
        case b'i':
            radio += 0.01
        case b'k':
            radio -= 0.01
        case b'+':
            cantidadPuntas += 1
        case b'-':
            cantidadPuntas -= 1
        case b'm':
            beta += 4
        case b'n':
            beta -= 4
    glutPostRedisplay() # Dibuja otra vez.

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("mesa 3D") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()