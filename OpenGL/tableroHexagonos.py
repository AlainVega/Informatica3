# Dibujar un tablero consistente en hexágonos que están ubicados uno al lado del otro. El
# tablero tiene que tener 3 capas. Deberán tener tres colores diferentes por lo menos y
# deberá posicionarse una fuente de luz. Este es un tablero mirado desde arriba. Debe
# utilizarse una proyección de perspectiva

# Acciones:
# 1) La tecla “+” deberá hacer aumentar (zoom-in)
# 2) La tecla “-” deberá disminuir el tamaño (zoom-out)
# 3) La tecla “w” deberá rotar el tablero completo en dirección positiva del eje “y”
# 4) La tecla “x” deberá mover la fuente de luz hacia el lado positivo de las “x”
# 5) La tecla “y” deberá mover la fuente de luz hacia el lado positivo de las “y”
# 6) La tecla “c” deberá mover la fuente de luz hacia el centro del tablero
# 7) La tecla “f” deberá mover la fuente alejándose del centro del tablero

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
centroTablero = [0, 0, 0]

# Sirve para dibujar la cara del poligono (Hexagono)
def cara(vertices, color):
    # Setear las propiedades del material.
    c = [color[0], color[1], color[2], 1]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, c) 
    glMaterialfv(GL_FRONT, GL_SPECULAR, rojo) 
    glMaterialfv(GL_FRONT, GL_EMISSION, c) 
    glMaterialfv(GL_FRONT, GL_SHININESS, 10) 
    glMaterialfv(GL_FRONT, GL_AMBIENT, c) 

    glColor(color[0], color[1], color[2], 1) # pintar con este color

    glBegin(GL_TRIANGLE_FAN) # dibuja triangulos para simular el hexagono.
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

# Sirve para definir el tablero.
def tablerohexagono():
    global centroTablero
    vertices = []
    p = 0.1 # paramtetro para definir el ancho y alto de las caras

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)

    # hexagono REGULAR formado con triangulos.
    # hexagono base (primero el centro, luego los vertices en sentido antihorario)
    r = p/(2*math.cos(3*math.pi/10))
    alpha = math.radians(60)
    a, b, h = p*math.cos(alpha), p*math.sin(alpha), (math.sqrt(3)*p)/2
    n, m = a, b
    vertices.append((p/2, h, 0)) # centro del hexagono
    vertices.append((0, 0, 0)) # vertice 1
    vertices.append((p, 0, 0)) # vertice 2
    vertices.append((p+a, b, 0)) # vertice 3
    vertices.append((p, m+b, 0)) # vertice 4
    vertices.append((0, m+b, 0)) # vertice 5
    vertices.append((-a, b, 0)) # vertice 6
    vertices.append((0, 0, 0)) # vertice 7 (para cerrar el abanico de triangulos.)

    centroTablero[0] = p/2
    centroTablero[1] = h
    centroTablero[2] = 0

    glPushMatrix()
    glTranslate(lightZeroPosition[0], lightZeroPosition[1], lightZeroPosition[2])
    # glutWireSphere(0.01, 10, 70) # para ver el foco de luz
    glPopMatrix()
    
    # glPushMatrix()
    glRotate(beta, 0, 1, 0)
            
    # hexagono central (base) gris
    glPushMatrix()
    cara(vertices, (0.4, 0.1, 0.7)) 
    glPopMatrix()

    # El nivel 2 (verde) se va a dibujar en sentido horario
    # (1) arriba
    # (2) arriba derecha
    # (3) abajo derecha
    # (4) abajo
    # (5) abajo izquierda
    # (6) arriba izquierda

    # Hexagono nivel 2 (1)
    glPushMatrix()
    glTranslate(0, 2*h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Hexagono nivel 2 (2)
    glPushMatrix()
    glTranslate(p+a, h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Hexagono nivel 2 (3)
    glPushMatrix()
    glTranslate(p+a, -h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Hexagono nivel (4)
    glPushMatrix()
    glTranslate(0, -2*h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix()

    # Hexagono nivel 2 (5)
    glPushMatrix()
    glTranslate(-p-a, -h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix() 

    # Hexagono nivel 2 (6)
    glPushMatrix()
    glTranslate(-a-p, h, 0)
    cara(vertices, (0.1, 0.7, 0.2))
    glPopMatrix() 

    # El nivel 3 (celeste) se va a dibujar en sentido horario empezando con el de mas arriba.

    # Hexagono nivel 3 (1)
    glPushMatrix()
    glTranslate(0, 4*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (2)
    glPushMatrix()
    glTranslate(p+a, 3*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()
    
    # Hexagono nivel 3 (3)
    glPushMatrix()
    glTranslate(2*p+2*a, 2*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (4)
    glPushMatrix()
    glTranslate(2*p+2*a, 0, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (5)
    glPushMatrix()
    glTranslate(2*p+2*a, -2*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (6)
    glPushMatrix()
    glTranslate(p+a, -3*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (7)
    glPushMatrix()
    glTranslate(0, -4*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (8)
    glPushMatrix()
    glTranslate(-p-a, -3*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (9)
    glPushMatrix()
    glTranslate(-2*p-2*a, -2*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (10)
    glPushMatrix()
    glTranslate(-2*p-2*a, 0, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (11)
    glPushMatrix()
    glTranslate(-2*p-2*a, 2*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # Hexagono nivel 3 (12)
    glPushMatrix()
    glTranslate(-p-a, 3*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    glFlush() # Para forzar a que pinte.
    # glFinish()

# Para dibujar los ejes de coordenadas.
def ejes():
    largo = 100
    glBegin(GL_LINES) # Contexto lineas

    # Eje X (ROJO)
    glColor3f(1, 0, 0)
    rojo = [1, 0, 0, 0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, rojo)
    glVertex3f(0, 0, 0)
    glVertex3f(largo, 0, 0)

    # Eje Y (VERDE)
    glColor3f(0, 1, 0)
    verde = [0, 1, 0, 0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, verde)
    glVertex3f(0, 0, 0)
    glVertex3f(0, largo, 0)

    # Eje Z (AZUL)
    glColor3f(0, 0, 1)
    azul = [0, 0, 1, 0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, azul)
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
    glEnable(GL_LIGHTING) # habilitar luces
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition) # posicion de la luz
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, origen) # direccion de la luz
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor) # color difuso de la luz
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientColor) # color ambiente
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)

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

    tablerohexagono()

# Captura las teclas 'w', 'a', 's' y 'd' para mover la camara en una esfera centrada en el origen.
def buttons(key, x, y):
    global ojoz, ojox, ojoy, beta, lightZeroPosition, t
    print(f'key={key}')
    match key:
        case b'r':
            ojox = x0
            ojoy = y0
            ojoz = z0
            beta = 0
            print('La camara y la figura volvieron a su posicion original.')
        case b'l':
            angulo += 4
            print(f'angulo = {angulo}')
        case b'j':
            angulo -= 4
            print(f'angulo = {angulo}')
        case b'+':
            ojox += 0.1
            ojoz += 0.1
        case b'-':
            ojox -= 0.1
            ojoz -= 0.1
        case b'w':
            beta += 4
        case b'x':
            lightZeroPosition[0] += 0.01
        case b'y':
            lightZeroPosition[1] += 0.01
        case b'c':
            t += 0.001
            lightZeroPosition[0] = lightZeroPosition[0] + t*(centroTablero[0]-lightZeroPosition[0])
            lightZeroPosition[1] = lightZeroPosition[1] + t*(centroTablero[1]-lightZeroPosition[1])
            lightZeroPosition[2] = lightZeroPosition[2] + t*(centroTablero[2]-lightZeroPosition[2])
        case b'f':
            t += 0.001
            lightZeroPosition[0] = lightZeroPosition[0] + t*(lightZeroPosition[0]-centroTablero[0])
            lightZeroPosition[1] = lightZeroPosition[1] + t*(lightZeroPosition[1]-centroTablero[1])
            lightZeroPosition[2] = lightZeroPosition[2] + t*(lightZeroPosition[2]-centroTablero[2])
    glutPostRedisplay() # Dibuja otra vez.

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Tablero de hexagono regulares") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()