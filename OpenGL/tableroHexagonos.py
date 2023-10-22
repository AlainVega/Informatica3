# Dibujar un tablero consistente en hexágonos que están ubicados uno al lado del otro. El
# tablero tiene que tener 3 capas. Deberán tener tres colores diferentes por lo menos y
# deberá posicionarse una fuente de luz. Este es un tablero mirado desde arriba. Debe
# utilizarse una proyección de perspectiva

# Acciones:
# 1) La tecla “+” deberá hacer aumentar (zoom-in)
# 2) La tecla “-” deberá disminuir el tamaño (zoom-out)
# 3) La tecla “w” deberá rotar el tablero completo en dirección positiva del eje “y”
# 4) La tecla “x” deberá mover la fuente de luz hacia el lado positivo de las “x”
# 5) La tecla “y” deberá mover la fuente de luz hacia el ladod positivo de las “y”
# 6) La tecla “c” deberá mover la fuente de luz hacia el centro del tablero
# 7) La tecla “f” deberá mover la fuente alejándose

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 1.2, 0.8, 2 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio)
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
angulo = 64 # angulo comun (Se controla con 'j' y 'l')
beta = 0 # angulo de giro de la figura entera (Se controla con 'n' y 'm')
# phi = math.acos(ojox/(radio*math.sin(teta))) # angulo horizontal de la camara (PLANO XOZ, Y = constante)

# Sirve para dibujar la cara del poligono (Hexagono)
def cara(vertices, color):
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
    vertices = []
    p = 0.1 # paramtetro para definir el ancho y alto de las caras
    # angulo = 0 # angulo comun 
    # angulo = 0 # angulo2 comun
    v = []

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

    # d = (p+2*h)*math.cos(math.radians(90-64))
    w = 90 - math.asin(h*math.sin(math.radians(90-64))/b)
    d = b*math.cos(math.radians(90-w)) + 2*h*math.cos(math.radians(90-64))

    a0, b0, c0 = p/2, h, 0          # centro del hexagono
    a1, b1, c1 = p/2, h, 0.5         # centro del hexagono pero desplazado en z
    a2, b2, c2 = a1-a0, b1-b0, c1-c0  # vector desde el origen (resta de vectores)

    v.append((a0, b0, c0)) # vertice 1 de la recta
    v.append((a1, b1, c1)) # vertice 2 de la recta

    # m = (0-b)/(p - p+a)
    # alpha = math.atan(m)
    # angulo = alpha*(180/math.pi)

    # print(angulo)

    # glPushMatrix()
    glRotate(beta, 0, 1, 0)
            
    # hexagono central (base) gris
    glPushMatrix()
    cara(vertices, (0.4, 0.1, 0.7)) 
    glPopMatrix()

    # Recta paralela al eje z que pasa por centro del hexagono base 
    # glPushMatrix()
    # glTranslate(-p, 0, 0)
    # recta(v, (1, 0.52, 0))
    # glPopMatrix()

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

    # Hexagono nivel 3 (2)
    glPushMatrix()
    glTranslate(-p-a, 3*h, 0)
    cara(vertices, (0.2, 0.7, 0.8))
    glPopMatrix()

    # # hexagono de la derecha azul
    # glPushMatrix()
    # glTranslate(p, 0, 0) # destraslada en x
    # glRotate(-108, 0, 0, 1) # rota en z
    # glTranslate(-p, 0, 0) # traslada  en x
    # glRotate(angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0, 0, 0.8))
    # glPopMatrix()
 
    # # hexagono de arriba derecha naranja
    # glPushMatrix()
    # glTranslate(p/2, 0, 0) # traslada en x
    # glTranslate(0, h+r, 0) # traslada en y
    # glRotate(324, 0, 0, 1) # rota en z
    # glRotate(angulo, 1, 0, 0) # rota en x
    # cara(vertices, (1, 0.52, 0))
    # glPopMatrix()

    # # hexagono de arriba izquierda rosado
    # glPushMatrix()
    # glTranslate(-a, 0, 0)  # traslada en x
    # glTranslate(0, b, 0) # traslada en y 
    # glRotate(36, 0, 0, 1) # rota en z
    # glRotate(angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0.8, 0.2, 0.5))
    # glPopMatrix()

    # # hexagono frontal amarillo
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # cara(vertices, (0.7, 0.7, 0.1))
    # # recta(v, (1, 0.52, 0)) 
    # glPopMatrix()

    # # hexagono frontal de abajo a la derecha purpura
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # glRotate(angulo, 1, 0, 0) # rota en x
    # glRotate(180, 1, 0, 0) # rota en x
    # cara(vertices, (0.4, 0.4, 0.8))
    # glPopMatrix()     

    # # hexagono frontal de abajo a la izquierda celeste
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # glRotate(108, 0, 0, 1) # rota en z
    # glRotate(-angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0.2, 0.7, 0.8))
    # glPopMatrix()   

    # # hexagono frontal a la derecha beige
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # glTranslate(p, 0, 0) # destraslada en x
    # glRotate(-108, 0, 0, 1) # rota en z
    # glTranslate(-p, 0, 0) # traslada en x
    # glRotate(-angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0.7, 0.7, 0.7))
    # glPopMatrix()   

    # # hexagono frontal a la izquierda lila
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # glTranslate(-a, 0, 0)  # traslada en x
    # glTranslate(0, b, 0) # traslada en y 
    # glRotate(36, 0, 0, 1) # rota en z
    # glRotate(-angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0.4, 0.1, 0.7))
    # glPopMatrix()   

    # # hexagono frontal de arriba negro
    # glPushMatrix()
    # glTranslate(0, 0, d) # move en z
    # glTranslated(a0, b0, c0) # destraslada
    # glRotate(36, a2, b2, c2) # rota sobre el vector director de la recta
    # glTranslated(-a0, -b0, -c0) # traslada la recta al origen
    # glTranslate(p/2, 0, 0) # traslada en x
    # glTranslate(0, h+r, 0) # traslada en y
    # glRotate(324, 0, 0, 1) # rota en z
    # glRotate(-angulo, 1, 0, 0) # rota en x
    # cara(vertices, (0.1, 0.1, 0.1))
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
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Tablero de hexagono regulares") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()