# Dibujar simbolo de infinito los parametros son los siguientes:
# 1) Posicion del centro
# 2) Color de relleno
# 2.a) Color de linea (contornos)
# 3) Radio de los lados
# 4) Ancho de la cinta
# 5) Ancho del medio infinito (del centro a un extremo)

# Operacion con las teclas:
# Tecla 's' mover hacia abajo 
# Tecla 'a' mover a la izquierda
# Tecla 'w' mover hacia arriba 
# Tecla 'a' mover a la derecha
# Tecla 'i' escalar toda la figura (reducir)
# Tecla 'k' escalar toda la figura (aumentar)
# Tecla '-' aumentar el valor 4) 
# Tecla '+' disminuir el valor 4)

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
t = 0
a = 0.141
r = 0.16
l = 0.68
n = l -r -(3*a)/2
vertical, horizontal = 0,0
size = 1

# Sirve para dibujar la cara del poligono. (Pintar el ancho del infinito)
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
    glBegin(GL_LINES) 
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

# Denota los puntos de un arco de circunferencia en un plano
# Retorna la lista de puntos.
def arco(centro, radio, color):
    v = []
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINE_STRIP) 
    x, y = 0, 0
    # x0, y0, x1, y1 = 0,0,0,0
    if centro[0] >= 0:
        for alpha in range(-90, 91):
            x = radio*math.cos(math.radians(alpha)) + centro[0]
            y = radio*math.sin(math.radians(alpha)) + centro[1]
            glVertex3f(x, y, 0)
            v.append((x,y,0))
        # x0, y0 = radio*math.cos(math.radians(-90)) + centro[0], radio*math.sin(math.radians(-90)) + centro[1]
        # x1, y1 = radio*math.cos(math.radians(90)) + centro[0], radio*math.sin(math.radians(90)) + centro[1]
    else:
        for alpha in range(-90, 91):
            x = -radio*math.cos(math.radians(alpha)) + centro[0]
            y = -radio*math.sin(math.radians(alpha)) + centro[1]
            glVertex3f(x, y, 0)
            v.append((x,y,0))
        # x0, y0 = -radio*math.cos(math.radians(-90)) + centro[0], radio*math.sin(math.radians(-90)) + centro[1]
        # x1, y1 = -radio*math.cos(math.radians(90)) + centro[0], radio*math.sin(math.radians(90)) + centro[1]
    glEnd()
    return v
    

# Sirve para definir el infinito.
def infinito():
    vertices = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario
    vertice0 = (0,0,0) # centro del infinito
    vertice1 = (a/2,0,0) 
    vertice2 = (0,-a/2,0)
    vertice3 = (-a/2,0,0)
    vertice4 = (0,a/2,0)
    # punto(vertices, (0.7, 0.2, 0))

    glTranslate(horizontal, vertical, 0)
    glScale(size, size, 0)

    centro = (a/2 + n, 0) # centro de las 2 semi circunferencias (centro de la semi dona derecha)
    interior = arco(centro, r, (1, 1, 1)) # delimita el arco interior
    recta([vertice1, interior[0], vertice1, interior[-1]], (1, 1, 1)) # dibuja el arco
    
    exterior = arco(centro, r+a, (1, 1, 1)) # delimita el arco exterior
    recta([vertice2, exterior[0], vertice4, exterior[-1]], (1, 1, 1)) # dibuja el arco

    # Pintamos la semi dona de la derecha
    for i in range(len(interior)):
        vertices.append(interior[i])
        vertices.append(exterior[i])
    cara(vertices, (1,1,1)) # pinta la semi dona

    vertices.clear()

    cara([vertice1, vertice2, interior[0], exterior[0]], (1,1,1)) # Pintar lazo de arriba derecha
    cara([vertice1, vertice4, interior[-1], exterior[-1]], (1,1,1)) # Pintar lazo de abajo derecha

    centro = (-a/2 - n, 0) # centro de las 2 semi circunferencias (centro de la semi dona izquierda)
    interior = arco(centro, r, (1, 1, 1)) # delimita el arco interior
    recta([vertice3, interior[-1], vertice3, interior[0]], (1, 1, 1)) # dibuja el arco

    exterior = arco(centro, r+a, (1, 1, 1)) # delimita el arco exterior
    recta([vertice2, exterior[-1], vertice4, exterior[0]], (1, 1, 1)) # dibuja el arco
 
    # Pintamos la semi dona de la izquierda
    for i in range(len(interior)):
        vertices.append(interior[i])
        vertices.append(exterior[i])
    cara(vertices, (1,1,1)) # pinta la semi dona

    vertices.clear()

    cara([vertice4, vertice3, exterior[0], interior[0]], (1,1,1)) # Pintar lazo de arriba izquierda
    cara([vertice2, vertice3, exterior[-1], interior[-1]], (1,1,1)) # Pintar lazo de abajo izquierda
   
    cara([vertice1, vertice4, vertice3, vertice2, vertice1], (1,1,1)) # Pintar cuadrado central

    glFlush() # Para forzar a que pinte.
    # glFinish()

# Para dibujar los ejes de coordenadas.
def ejes():
    largo = 100
    glBegin(GL_LINES) # Contexto lineas

    # Eje X (ROJO)
    glColor3f(1, 0, 0)
    rojo = [1, 0, 0, 0]
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, rojo)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)

    # Eje Y (VERDE)
    glColor3f(0, 1, 0)
    verde = [0, 1, 0, 0]
    # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, verde)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)

    # Eje Z (AZUL)
    glColor3f(0, 0, 1)
    azul = [0, 0, 1, 0]
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
    origen = [0,0,0]
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

    infinito()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, horizontal, vertical, size, a
    print(f'key={key}')
    match key:
        case b'r':
            vertical, horizontal, size, a = 0, 0, 1, 0.141
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
            a += 0.005
        case b'-':
            a -= 0.005
    glutPostRedisplay() # Dibuja otra vez.

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Infinito") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()