# Utilizando PyOpenGL dibujar una estrella en 3D compuesta de prismas o poligonos.
# El color, la posicion inicial y las dimensiones de la estrella quedan a criterio
# del alumno. 
# Se debera ubicar una fuente de luz blanca en cualquier posicion y las teclas
# "asdw" deberan mover la fuente de luz en las direcciones 
# (izquierda, abajo, derecha y arriba, respectivamente). Las teclas "u y j" deberan rotar
# toda la estrella alrededor de cualquiera de las puntas (queda a criterio del alumno
# alrededor de que punta rotar, siempre y cuando NO COINCIDA con ninguno de los ejes)
# Dibujar tambien los ejes de coordenadas.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 1.2, 1, 4 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio)
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
beta = 0
lightZeroPosition = [0.7, 0.4, 1.5, 0] # posicion de la fuente de luz
lightZeroColor = [1, 1, 0.6, 0] # color de la fuente de luz
rojo = [1, 0, 0, 1]
ambientColor = [0.7, 0.7, 0.3, 1] # tono de la luz ambiente
# radio = 0.3
cantidadPuntas = 6
vertical, horizontal = 0,0
size = 1

# Sirve para dibujar la cara del poligono. (Pintar el ancho del estrella)
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

def poligono(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_POLYGON) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para definir la estrella.
def estrella():
    verticesBaseAbajo = []
    verticesPuntasAbajo = []
    verticesBaseArriba = []
    verticesPuntasArriba = []
    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario

    # ESTRELLA DE ABAJO
    glRotate(beta, 0, 1, 0)

    # Pentagono regular
    alpha = 360/5
    radio = 0.4
    for i in range(5):
        x = radio*math.cos(math.radians(alpha*i))
        z = radio*math.sin(math.radians(alpha*i))
        verticesBaseAbajo.append((x, 0, z))
    poligono(verticesBaseAbajo, (0.6, 0.7, 0.1))

    alturaEstrella = 0.7
    for i in range(5):
        x = (radio + alturaEstrella)*math.cos(math.radians(alpha*i + alpha/2))
        z = (radio + alturaEstrella)*math.sin(math.radians(alpha*i + alpha/2))
        verticesPuntasAbajo.append((x, 0, z))
    
    for i in range(5):
        if i == 4:
            poligono([verticesBaseAbajo[i], verticesBaseAbajo[0], verticesPuntasAbajo[i]], (0.6, 0.7, 0.1))
        else:
            poligono([verticesBaseAbajo[i], verticesBaseAbajo[i+1], verticesPuntasAbajo[i]], (0.6, 0.7, 0.1))

    # ESTRELLA DE ARRIBA
    alto = 0.2
    for i in range(5):
        x = radio*math.cos(math.radians(alpha*i))
        z = radio*math.sin(math.radians(alpha*i))
        verticesBaseArriba.append((x, alto, z))
    poligono(verticesBaseArriba, (0.6, 0.7, 0.1))

    for i in range(5):
        x = (radio + alturaEstrella)*math.cos(math.radians(alpha*i + alpha/2))
        z = (radio + alturaEstrella)*math.sin(math.radians(alpha*i + alpha/2))
        verticesPuntasArriba.append((x, alto, z))
    
    for i in range(5):
        if i == 4:
            poligono([verticesBaseArriba[i], verticesBaseArriba[0], verticesPuntasArriba[i]], (0.6, 0.7, 0.1))
        else:
            poligono([verticesBaseArriba[i], verticesBaseArriba[i+1], verticesPuntasArriba[i]], (0.6, 0.7, 0.1))

    # Pintar lados de las estrellas
    iterable = [(0,0)]
    for i in range(9):
        if i == 8:
            a = -1
            b = iterable[-1][1]
        else:
            a, b = iterable[-1][0], iterable[-1][1]
        if i % 2 == 0:
            iterable.append((a+1, b))
        else:
            iterable.append((a, b+1))
    # print(iterable)
            
    v = []
    for i,j in iterable:
        v.append(verticesBaseAbajo[i])
        v.append(verticesBaseArriba[i])
        v.append(verticesPuntasArriba[j])
        v.append(verticesPuntasAbajo[j])
    poligono(v, (0.6, 0.7, 0.1))

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

    estrella()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, horizontal, vertical, beta, phi, teta
    print(f'key={key}')
    match key:
        case b'r':
            teta, phi = teta0, phi0
            ojox = x0
            ojoy = y0
            ojoz = z0
            beta = 0
            print('La figura volvio a su posicion inicial.')
        case b's':
            vertical -= 0.01
        case b'a':
            horizontal -= 0.01
        case b'w':
            vertical += 0.01
        case b'd':
            horizontal += 0.01
        case b'm':
            beta += 4
        case b'n':
            beta -= 4

    glutPostRedisplay() # Dibuja otra vez.

def handleSpecialKeypress(key, x, y):
    global teta, phi, ojox, ojoy, ojoz
    if key == GLUT_KEY_UP:
        print("GLUT_KEY_UP")
        teta += 0.1
        ojoy = radio*math.sin(teta)
        ojoz = radio*math.cos(teta)
    elif key == GLUT_KEY_DOWN:
        print("GLUT_KEY_DOWN")
        teta -= 0.1
        ojoy = radio*math.sin(teta)
        ojoz = radio*math.cos(teta)
    elif key == GLUT_KEY_LEFT:
        print("GLUT_KEY_LEFT")
        phi += 0.1
        ojoz = radio*math.sin(phi)
        ojox = radio*math.cos(phi)
    elif key == GLUT_KEY_RIGHT:
        print("GLUT_KEY_RIGHT")
        phi -= 0.1
        ojoz = radio*math.sin(phi)
        ojox = radio*math.cos(phi)
        
    glutPostRedisplay() # Dibuja otra vez.

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("estrella 3D") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutSpecialFunc(handleSpecialKeypress)
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()