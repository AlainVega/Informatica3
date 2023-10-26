# Graficar la tierra rotando al rededor del sol y rotando en su eje.

#imports
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

#variables globales
ancho, alto = 800, 800 # Para la ventana emergente.
x0, y0, z0 = 0.2, 0.2, 3 # Posicion inicial de la camara (esta en una esfera centrada en el origen) # angulo phi y teta iniciales.
ojox, ojoy, ojoz = x0, y0, z0
radio = math.sqrt(x0*x0 + y0*y0 + z0*z0) # de la esfera centrada en el origen.
phi0, teta0 = math.asin(z0/radio), math.acos(z0/radio)
teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
N = 3
lado = 0.1
X, Y, Z = 0, 0, 0
cantidadRectangulos = 4
angulo = 45
largo = 0.2
time = 0

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

# Sirve para dibujar triangulos strip
def trianguloStrip(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLE_STRIP) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar triangulos fan
def trianguloFan(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_TRIANGLE_FAN) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar cuadrilateros
def trianguloFan(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_QUADS) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar cuadrilateros strip
def trianguloFan(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_QUAD_STRIP) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Sirve para dibujar rectas strio
def rectaStrip(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINE_STRIP) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

    # Sirve para dibujar rectas.
def recta(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_LINES) 
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
    else:
        for alpha in range(-90, 91):
            x = -radio*math.cos(math.radians(alpha)) + centro[0]
            y = -radio*math.sin(math.radians(alpha)) + centro[1]
            glVertex3f(x, y, 0)
            v.append((x,y,0))
    glEnd()
    return v
    
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

# Devuelve los puntos de la curva en el espacio
# p0 incial, p1 control, p2 control, p3 final
def bezierCubico(p0, p1, p2, p3):
    intervalo = [i*0.01 for i in range(100)]
    puntos = []
    for t in intervalo:
        x = (1 - t)*(1 - t)*(1 - t)*p0[0] + 3*t*(1 - t)*(1 - t)*p1[0] + 3*t*t*(1-t)*p2[0] + t*t*t*p3[0]
        y = (1 - t)*(1 - t)*(1 - t)*p0[1] + 3*t*(1 - t)*(1 - t)*p1[1] + 3*t*t*(1-t)*p2[1] + t*t*t*p3[1]
        z = (1 - t)*(1 - t)*(1 - t)*p0[2] + 3*t*(1 - t)*(1 - t)*p1[2] + 3*t*t*(1-t)*p2[2] + t*t*t*p3[2]
        puntos.append((x, y, z))
    return puntos

# Para dibujar poligonos
def poligono(vertices, color):
    glColor(color[0], color[1], color[2], 1) # pintar con este color
    glBegin(GL_POLYGON) 
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() 

# Logica del triangulo de pascal (Recursivo)
def Pascal(triangulo, N, color):
    # Vector del vertice 0 al 2
    a, b, c = triangulo[2][0] - triangulo[0][0], triangulo[2][1] - triangulo[0][1], triangulo[2][2] - triangulo[0][2]
    if N == 1:
        poligono(triangulo, color)
    else:
        for i in range(N):
            glPushMatrix()
            glTranslate(i*lado, 0, 0)
            poligono(triangulo, color)
            glPopMatrix()
        glTranslate(a,b,c)
        Pascal(triangulo, N-1, color)

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
def orbita():

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    glColor((1,1,0))
    glutSolidSphere(0.1, 70, 70)
    global time
    time += 0.01
    alpha = 4
    glColor((0.1, 0.7, 0.1))
    glPushMatrix()
    glRotate(4*time, 0, 1, 0)
    glTranslate(0.5, 0, 0)
    glutSolidSphere(0.03, 70, 70)
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

    orbita()

############################################################################################################################################################
# Manejadores de teclas.
############################################################################################################################################################

# Captura las teclas distintas funciones.
def buttons(key, x, y):
    global ojoz, ojox, ojoy, teta, phi, radio, angulo, cantidadRectangulos, largo
    # print(f'key={key}')
    match key:
        case b'r':
            ojox, ojoy, ojoz, = x0, y0, z0
            teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
            phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
            angulo = 45
            cantidadRectangulos = 4
            largo = 0.2
            print('La figura volvio a su tamanho y disposicion inicial.')
        case b's':
            if cantidadRectangulos > 1:
                cantidadRectangulos -= 1
        case b'a':
            if largo > 0.1:
                largo -= 0.001
        case b'w':
            cantidadRectangulos += 1
        case b'd':
            largo += 0.001
        case b'+':
            angulo -= 1
        case b'-':
            angulo += 1

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
          "* 'r': reinicia todos los parametros ajustables por el usuario \n" +
          "* \n" +
          "* \n" +
          "* \n" +
          "* \n" +
          "* \n" +
          "**********************************************************************************************************************************")
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("Orbita de la tierra") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutSpecialFunc(handleSpecialKeypress)
    glutIdleFunc(display)
    glutMainLoop() # mantiene la ventana corriendo en bucle.
main()