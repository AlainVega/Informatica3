# ALAIN VEGA Y11159
# Parcial Informatica 3

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from itertools import cycle

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 0.2, 0.2, 2 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio) # los angulos respectivos de las cias
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
X = 0 # valor para la traslacion en el eje X.
angulo = 0 # angulo de rotacion para el ejex Y.
cantidadTriangulos = 4 # cantidad de triangulos que forman la figura.
beta = 0 # angulo de rotacion para una arista definida.

############################################################################################################################################################
# Funciones auxiliares.
############################################################################################################################################################

# Sirve para dibujar triangulos
def triangulo(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLES) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd()  

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

############################################################################################################################################################
# Funcion que define la logica del problema.
############################################################################################################################################################
def piramideTriangulos():
    ancho = 0.2
    alto = 0.4

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul
    vertices = []
    
    vertices.append((0,0,0)) # vertice 0
    vertices.append((ancho,0,0)) # vertice 1
    vertices.append((0,alto,0)) # vertice 2

    # Componentes del vector director de la recta de la arista.
    a = vertices[2][0] - vertices[1][0]
    b = vertices[2][1] - vertices[1][1]
    c = vertices[2][2] - vertices[1][2]

    glRotate(angulo, 0, 1, 0) # para rotar al rededor del eje Y
    glTranslate(X, 0, 0) # para trasladar en X
    # Manejar la rotacion al rededor de una arista
    glTranslate(vertices[1][0], vertices[1][1], vertices[1][2])
    glRotate(beta, a, b, c)
    glTranslate(- vertices[1][0], - vertices[1][1], - vertices[1][2])
    
    color = [ (1,1,0), (0,1,1), (1,0,1), (0.1, 0.8, 0.2) ]

    pool = cycle(color)

    alpha = 360/cantidadTriangulos
    for i in range(cantidadTriangulos):
        glPushMatrix()
        glRotate(alpha*i, 0, 1, 0)
        triangulo(vertices, next(pool))
        glPopMatrix()

    glFlush() # Para forzar a que pinte.
    # glFinish()

############################################################################################################################################################
# Funcion llamada en cada frame.
############################################################################################################################################################

# Funcion de pintar
def display():
    # global ojox, ojoy, ojoz
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  
    
    # Selecciona la matriz de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Inicializar la matriz.

    # Ángulo, ratio, near, far
    gluPerspective(35, alto/ancho, 0.1, 10)

    # Seleccionar la matriz modelview
    glMatrixMode(GL_MODELVIEW)

    # Inicializar la matriz.
    glLoadIdentity()

    # Desde, Hacia, Dirección arriba
    gluLookAt(ojox, ojoy, ojoz, 0, 0, 0, 0.0, 1.0, 0.0)

    piramideTriangulos()

############################################################################################################################################################
# Manejadores de teclas.
############################################################################################################################################################

# Captura las teclas distintas funciones.
def buttons(key, x, y):
    global ojoz, ojox, ojoy, teta, phi, radio, angulo, cantidadTriangulos, X, beta
    # print(f'key={key}')
    match key:
        case b't':
            ojox, ojoy, ojoz, = x0, y0, z0
            teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
            phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
            cantidadTriangulos = 4
            X, angulo, beta = 0,0,0
            print('La figura volvio a su tamanho y disposicion inicial.')
        case b'm':
            cantidadTriangulos += 1
        case b'n':
            if cantidadTriangulos > 1:
                cantidadTriangulos -= 1
        case b'y':
            angulo += 4
        case b'x':
            X += 0.05
        case b'r':
            beta += 4
    glutPostRedisplay() # Dibuja otra vez.

# Captura las flechas para mover la camara en una esfera centrada en el origen.
def handleSpecialKeypress(key, x, y):
    global teta, phi, ojox, ojoy, ojoz
    if key == GLUT_KEY_UP:
        teta += 0.1
        ojoy = radio*math.sin(teta)
        ojoz = radio*math.cos(teta)
    elif key == GLUT_KEY_DOWN:
        teta -= 0.1
        ojoy = radio*math.sin(teta)
        ojoz = radio*math.cos(teta)
    elif key == GLUT_KEY_LEFT:
        phi += 0.1
        ojoz = radio*math.sin(phi)
        ojox = radio*math.cos(phi)
    elif key == GLUT_KEY_RIGHT:
        phi -= 0.1
        ojoz = radio*math.sin(phi)
        ojox = radio*math.cos(phi)
    glutPostRedisplay() # Dibuja otra vez.

############################################################################################################################################################
# Funcion principal.
############################################################################################################################################################
def main():
    print("********************************************************************************************************************************** \n " +
          "BIENVENIDO: la interactividad del programa es la siguiente: \n" + 
          "* Fechas: mueven la camara en una esfera centrada en el origen \n" +
          "* 't': reinicia todos los parametros ajustables por el usuario \n" +
          "* 'x': mueve toda la figura en direccion positiva de las X \n" +
          "* 'y': rota la figura respecto al eje Y \n" +
          "* 'r': rota la figura respecto a la recta del contorno de una arista \n" +
          "* 'm': aumenta la cantidad de triangulos en 1 \n" +
          "* 'n': disminuye la cantidad de triangulos en 1\n" +
          "**********************************************************************************************************************************")
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Programa en PyOpenGL") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutSpecialFunc(handleSpecialKeypress)
    glutMainLoop() # mantiene la ventana corriendo en bucle.
main()