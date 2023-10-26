# Utilizando PyOpenGL dibujar una flecha en 3D. 
# El color, la posicion inicial y las dimensiones quedan a criterio del alumno. 
# Se debera ubicar una fuente de luz blanca en cualquier posicion
# y las teclas "asdw" deberan mover la fuente de luz en las direcciones 
# (izquierda, abajo, derecha y arriba, respectivamente). Las teclas "u y j" deberan rotar
# toda la flecha alrededor de cualquiera de las aristas (queda a criterio del alumno
# alrededor de que arista rotar, siempre y cuando NO COINCIDA con ninguno de los ejes)
# Dibujar tambien los ejes.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 1.2, 0.8, 2 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
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

# Sirve para dibujar la cara del poligono. (Pintar el ancho del flecha)
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

# Devuelve los puntos de la curva en el plano XOY
# p0 incial, p1 control, p2 final
def bezierCuadratico(p0, p1, p2):
    intervalo = [i*0.01 for i in range(100)]
    puntos = []
    for t in intervalo:
        x = (1 - t)*(1 - t)*p0[0] + 2*t*(1 - t)*p1[0] + t*t*p2[0]
        y = (1 - t)*(1 - t)*p0[1] + 2*t*(1 - t)*p1[1] + t*t*p2[1]
        puntos.append((x, y, 0))
    return puntos

# Sirve para definir la flecha.
def flecha():
    vertices = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario

    glRotate(beta, 0, 1, 0)
    # glTranslate(horizontal, vertical, 0)
    # glScale(size, size, 0)

   # Puntas de los 2 triangulos
    puntaAbajo = (0,0,0) # punta de la flecha abajo
    puntaArriba = (0,0.2,0) # punta de la flecha arriba
    
    # Triangulo ancho
    aDerechaAbajo = (0.35, 0, 0.3)
    aIzquierdaAbajo = (-0.35, 0, 0.3)
    aDerechaArriba = (0.35, 0.2, 0.3)
    aIzquierdaArriba = (-0.35, 0.2, 0.3)

    # rectaLoop([puntaAbajo, aDerechaAbajo, aIzquierdaAbajo], (0.7, 0.7, 0.1))
    # rectaLoop([puntaArriba, aDerechaArriba, aIzquierdaArriba], (0.7, 0.7, 0.1))
    cara([aDerechaAbajo, aIzquierdaAbajo, aIzquierdaArriba, aDerechaArriba], (0.7, 0.7, 0.1))
    cara([aDerechaAbajo, puntaAbajo, puntaArriba, aDerechaArriba], (0.7, 0.7, 0.1))
    cara([aIzquierdaAbajo, puntaAbajo, puntaArriba, aIzquierdaArriba], (0.7, 0.7, 0.1))

    # Triangulo largo
    lDerechaAbajo = (0.25, 0, 0.7)
    lIzquierdaAbajo = (-0.25, 0, 0.7)
    lDerechaArriba = (0.25, 0.2, 0.7)
    lIzquierdaArriba = (-0.25, 0.2, 0.7)

    # rectaLoop([puntaAbajo, lDerechaAbajo, lIzquierdaAbajo], (0.7, 0.7, 0.1))
    # rectaLoop([puntaArriba, lDerechaArriba, lIzquierdaArriba], (0.7, 0.7, 0.1))
    cara([lDerechaAbajo, lIzquierdaAbajo, lIzquierdaArriba, lDerechaArriba], (0.7, 0.7, 0.1))
    cara([lDerechaAbajo, puntaAbajo, puntaArriba, lDerechaArriba], (0.7, 0.7, 0.1))
    cara([lIzquierdaAbajo, puntaAbajo, puntaArriba, lIzquierdaArriba], (0.7, 0.7, 0.1))

    # rectaLoop([punta, vertice3, vertice4], (0.1, 0.7, 0.7))

    # glPushMatrix()
    # glTranslate(0, 0.2, 0)
    # rectaLoop([punta, vertice1, vertice2], (0.7, 0.7, 0.1))
    # rectaLoop([punta, vertice3, vertice4], (0.1, 0.7, 0.7))
    # glPopMatrix()

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

    flecha()

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
    glutCreateWindow("Flecha 3D") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()