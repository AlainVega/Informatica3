# Dibujar una espiral donde los parametros son los siguientes
# 1) Posicion del centro
# 2) Color de relleno
# 3) Ancho de la linea (La parte sin color tiene el mismo ancho que la parte con color)
# 4) Cantidad de vueltas

# Operacion con teclas
# Tecla 's' mover hacia abajo
# Tecla 'w' mover hacia abajo
# Tecla 'a' mover hacia la izquierda
# Tecla 'd' mover hacia la derecha
# Tecla 'i' escalar toda la figura (reducir)
# Tecla 'k' escalar toda la figura (aumentar)
# Tecla '-' aumentar el valor 4) (en .1)
# Tecla '+' disminuir el valor 4) (en .1)

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
a = 0.06
vertical, horizontal = 0,0
size = 1
k = 5

# Sirve para dibujar la cara del poligono (Hexagono)
def cara(vertices, color):
    # Setear las propiedades del material.
    c = [color[0], color[1], color[2], 1]
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, c) 
    # glMaterialfv(GL_FRONT, GL_SPECULAR, rojo) 
    # glMaterialfv(GL_FRONT, GL_EMISSION, c) 
    # glMaterialfv(GL_FRONT, GL_SHININESS, 10) 
    # glMaterialfv(GL_FRONT, GL_AMBIENT, c) 

    glColor(color[0], color[1], color[2], 1) # pintar con este color

    glBegin(GL_TRIANGLE_STRIP) # dibuja triangulos para simular el hexagono.
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

# Sirve para dibujar puntos
def punto(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_POINTS) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para definir el espiral.
def espiral():
    interior = []
    exterior = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    glTranslate(horizontal, vertical, 0)
    glScale(size, size, 0)

    # Contorno interior (espiral interior)
    radios = [i * 0.0002 for i in range(1, 360*k)]
    alpha = 0
    for radio in radios:
        alpha += 0.01
        x0 = radio*math.cos(alpha) 
        y0 = radio*math.sin(alpha) 
        interior.append((x0, y0, 0))
    recta(interior, (1, 1, 1))

    # Contorno exterior (espiral exterior)
    alpha = 0
    i = 0
    for radio in radios:
        alpha += 0.01
        if i < a:
            i += 0.0004
        else:
            i = a
        x1 = (radio + i)*math.cos(alpha) 
        y1 = (radio + i)*math.sin(alpha)
        exterior.append((x1, y1, 0))
    recta(exterior, (1, 1, 1))

    vertices = []

    for i in range(len(radios)):
        vertices.append(interior[i])
        vertices.append(exterior[i])
    cara(vertices, (1,1,1)) # Pinta el relleno entre contorno exterior e interior

    glFlush() # Para forzar a que pinte.
    # glFinish()

# Para dibujar los ejes de coordenadas.
def ejes():
    largo = 100
    glBegin(GL_LINES) # Contexto lineas

    # Eje X (ROJO)
    glColor3f(1, 0, 0)
    # rojo = [1, 0, 0, 0]
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, rojo)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)

    # Eje Y (VERDE)
    glColor3f(0, 1, 0)
    # verde = [0, 1, 0, 0]
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, verde)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)

    # Eje Z (AZUL)
    glColor3f(0, 0, 1)
    # azul = [0, 0, 1, 0]
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, azul)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, largo)

    glEnd() # Fin contexto lineas

# Funcion de pintar
def display():
    # global ojox, ojoy, ojoz
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  
    
    # Luz
    # origen = [0,0,0]
    # glShadeModel(GL_SMOOTH)
    # glEnable(GL_CULL_FACE)
    # glEnable(GL_LIGHTING) # habilitar luces
    # glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition) # posicion de la luz
    # glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, origen) # direccion de la luz
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor) # color difuso de la luz
    # glLightfv(GL_LIGHT0, GL_AMBIENT, ambientColor) # color ambiente
    # glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    # glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    # glEnable(GL_LIGHT0)

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

    espiral()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, horizontal, vertical, size, k
    print(f'key={key}')
    match key:
        case b'r':
            vertical, horizontal, size, k = 0, 0, 1, 5
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
            size += 0.01
        case b'k':
            size -= 0.01
        case b'+':
            k += 1
        case b'-':
            k -= 1
    glutPostRedisplay() # Dibuja otra vez.

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("espiral") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()