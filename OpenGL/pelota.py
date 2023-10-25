# Utilizando PyOpenGL dibujar una pelota en 3D compuesta de pentagonos y hexagonos.
# El color, la posicion inicial y las dimensiones de la pelota quedan a criterio
# del alumno. 
# Se debera ubicar una fuente de luz blanca en cualquier posicion y las teclas
# "asdw" deberan mover la fuente de luz en las direcciones 
# (izquierda, abajo, derecha y arriba, respectivamente). Las teclas "u y j" deberan rotar
# toda la pelota alrededor de cualquiera de las tangentes (queda a criterio del alumno
# alrededor de que tangente rotar, siempre y cuando NO COINCIDA con ninguno de los ejes)
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
xd = 0
X, Y = 0, 0
angulo = 0 # 38 es el que cierra bien

# Sirve para dibujar la cara del poligono. (Pintar el ancho del pelota)
def cara(vertices, color):
    # Setear las propiedades del material.
    c = [color[0], color[1], color[2], 1]
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, c) 
    # glMaterialfv(GL_FRONT, GL_SPECULAR, rojo) 
    # glMaterialfv(GL_FRONT, GL_EMISSION, c) 
    # glMaterialfv(GL_FRONT, GL_SHININESS, 10) 
    # glMaterialfv(GL_FRONT, GL_AMBIENT, c) 

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

# Sirve para definir la pelota.
def pelota():
    verticesPentagono = []
    verticesHexagono = []
    # verticesBaseArriba = []
    # verticesPuntasArriba = []
    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario
    p = 0.2
    r = p/(2*math.cos(3*math.pi/10))
    a, b, h = p*math.cos(2*math.pi/5), p*math.sin(2*math.pi/5), (p*math.tan(3*math.pi/10))/2
    # verticesPentagono.append((p/2, h, 0)) # centro del pentagono
    verticesPentagono.append((0, 0, 0)) # vertice 0
    verticesPentagono.append((p, 0, 0)) # vertice 1
    verticesPentagono.append((p+a, b, 0)) # vertice 2
    verticesPentagono.append((p/2, h+r, 0)) # vertice 3
    verticesPentagono.append((-a, b, 0)) # vertice 4
    verticesPentagono.append((0, 0, 0)) # vertice 5 (para cerrar)

    # Hexagono
    alpha = math.radians(60)
    n, m, H = p*math.cos(alpha), p*math.sin(alpha), (math.sqrt(3)*p)/2
    # verticesHexagono.append((p/2, H, 0)) # centro del hexagono
    verticesHexagono.append((0, 0, 0)) # vertice 0
    verticesHexagono.append((p, 0, 0)) # vertice 1
    verticesHexagono.append((p+n, m, 0)) # vertice 2
    verticesHexagono.append((p, 2*m, 0)) # vertice 3
    verticesHexagono.append((0, 2*m, 0)) # vertice 4
    verticesHexagono.append((-n, m, 0)) # vertice 5
    verticesHexagono.append((0, 0, 0)) # vertice 6 (para cerrar)

    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    poligono(verticesPentagono, (0.2, 0.2, 0.2))

    # for i in range(1):
    #     glPushMatrix()
    #     if i == 4:
    #         glTranslate((verticesPentagono[0][0]+verticesPentagono[i][0])/2, (verticesPentagono[0][1]+verticesPentagono[i][1])/2, 0)
    #         glRotate(36, 0, 0, 1)
    #         glTranslate(-(0 + p)/2, -(0 + 0)/2, 0) 
    #     else:
    #         glTranslate((verticesPentagono[i+1][0]+verticesPentagono[i][0])/2, (verticesPentagono[i+1][1]+verticesPentagono[i][1])/2, 0)
    #         glRotate(-36, 0, 0, 1)
    #         glTranslate(-(0 + p)/2, -(0 + 0)/2, 0)
    #     poligono(verticesHexagono, (0.1, 0.7, 0.8))

    #     glPopMatrix()

    # Abajo 
    # glPushMatrix()
    # glRotate(180, 1, 0, 0)
    # poligono(verticesHexagono, (0.1, 0.7, 0.8))
    # glPopMatrix()

    glPushMatrix()
    glTranslate((verticesPentagono[0][0]+verticesPentagono[1][0])/2, (verticesPentagono[0][1]+verticesPentagono[1][1])/2, 0)
    glRotate(180, 0, 0, 1)
    glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesHexagono, (0.7, 0.7, 0.1))
    glPopMatrix()

    # # Abajo izquierda
    # glPushMatrix()
    # glRotate(108, 0, 0, 1)
    # poligono(verticesHexagono, (0.1, 0.7, 0.8))
    # glPopMatrix()

    glPushMatrix()
    glTranslate((verticesPentagono[4][0]+verticesPentagono[5][0])/2, (verticesPentagono[4][1]+verticesPentagono[5][1])/2, 0)
    glRotate(108, 0, 0, 1)
    glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesHexagono, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Arriba izquierda
    glPushMatrix()
    glTranslate((verticesPentagono[3][0]+verticesPentagono[4][0])/2, (verticesPentagono[3][1]+verticesPentagono[4][1])/2, 0)
    # glTranslate((p/2 - a)/2, (b+h+r)/2, 0)
    glRotate(36, 0, 0, 1)
    glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesHexagono, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Arriba derecha
    glPushMatrix()
    glTranslate((verticesPentagono[2][0]+verticesPentagono[3][0])/2, (verticesPentagono[2][1]+verticesPentagono[3][1])/2, 0)
    # glTranslate((p+a + p/2)/2, (b+h+r)/2, 0)
    glRotate(-36, 0, 0, 1)
    glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesHexagono, (0.7, 0.7, 0.1))
    glPopMatrix()

    # Abajo derecha
    glPushMatrix()
    glTranslate((verticesPentagono[1][0]+verticesPentagono[2][0])/2, (verticesPentagono[1][1]+verticesPentagono[2][1])/2, 0)
    glRotate(-108, 0, 0, 1)
    glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesHexagono, (0.7, 0.7, 0.1))
    glPopMatrix()

    glPushMatrix()
    glTranslate(0, 4*h + H, 0)
    glRotate(180, 1, 0, 0)
    glRotate(angulo, 1, 0, 0)
    poligono(verticesPentagono, (0.90, 0.2, 0.2))
    glPopMatrix()

    # d = H*(2*math.cos(math.radians(90-angulo)) + math.cos(math.radians(90-angulo))) + h

    # glPushMatrix()
    # glTranslate(0,0,d)
    # poligono(verticesPentagono, (0.2, 0.2, 0.2))
    # glPopMatrix()

    # # Abajo
    # glPushMatrix()
    # glTranslate(0,0,d)
    # glTranslate((verticesPentagono[0][0]+verticesPentagono[1][0])/2, (verticesPentagono[0][1]+verticesPentagono[1][1])/2, 0)
    # glRotate(180, 0, 0, 1)
    # glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    # glRotate(-angulo, 1, 0, 0)
    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    # glPopMatrix()

    # # Abajo izquierda
    # glPushMatrix()
    # glTranslate(0,0,d)
    # glTranslate((verticesPentagono[4][0]+verticesPentagono[5][0])/2, (verticesPentagono[4][1]+verticesPentagono[5][1])/2, 0)
    # glRotate(108, 0, 0, 1)
    # glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    # glRotate(-angulo, 1, 0, 0)
    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    # glPopMatrix()

    # # Arriba izquierda
    # glPushMatrix()
    # glTranslate(0,0,d)
    # glTranslate((verticesPentagono[3][0]+verticesPentagono[4][0])/2, (verticesPentagono[3][1]+verticesPentagono[4][1])/2, 0)
    # # glTranslate((p/2 - a)/2, (b+h+r)/2, 0)
    # glRotate(36, 0, 0, 1)
    # glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    # glRotate(-angulo, 1, 0, 0)
    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    # glPopMatrix()

    # # Arriba derecha
    # glPushMatrix()
    # glTranslate(0,0,d)
    # glTranslate((verticesPentagono[2][0]+verticesPentagono[3][0])/2, (verticesPentagono[2][1]+verticesPentagono[3][1])/2, 0)
    # # glTranslate((p+a + p/2)/2, (b+h+r)/2, 0)
    # glRotate(-36, 0, 0, 1)
    # glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    # glRotate(-angulo, 1, 0, 0)
    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    # glPopMatrix()

    # # Abajo derecha
    # glPushMatrix()
    # glTranslate(0,0,d)
    # glTranslate((verticesPentagono[1][0]+verticesPentagono[2][0])/2, (verticesPentagono[1][1]+verticesPentagono[2][1])/2, 0)
    # glRotate(-108, 0, 0, 1)
    # glTranslate(-(verticesHexagono[0][0]+verticesHexagono[1][0])/2, -(verticesHexagono[0][1]+verticesHexagono[1][1])/2, 0)
    # glRotate(-angulo, 1, 0, 0)
    # poligono(verticesHexagono, (0.7, 0.7, 0.1))
    # glPopMatrix()


    ##################################################################################################
    # Divague
    ##################################################################################################


    # lado = 0.2
    # radioPentagono = lado / (2 * math.cos(math.radians(180-90-72/2)))
    # radioHexagono = lado / (2 * math.cos(math.radians(180-90-60/2)))
    # print(f'p={radioPentagono} \n h={radioHexagono}')

    # # Hexagono
    # alpha = math.radians(360/6)
    # for i in range(6):  
    #     x = radioHexagono*math.cos(alpha*i) 
    #     y = radioHexagono*math.sin(alpha*i)
    #     verticesHexagono.append((x,y,0))
    # # poligono(verticesHexagono, (0.7, 0.7, 0.1))

    # # Pentagono
    # alpha = math.radians(360/5)
    # for i in range(5):  
    #     x = radioPentagono*math.cos(alpha*i)
    #     y = radioPentagono*math.sin(alpha*i)
    #     verticesPentagono.append((x,y,0))
    # poligono(verticesPentagono, (0.4, 0.1, 0.9))

    # for i in range(5):
    #     if i == 4:
    #         recta([(verticesPentagono[i][0], verticesPentagono[i][1], verticesPentagono[i][2]),
    #         (verticesPentagono[0][0], verticesPentagono[0][1], verticesPentagono[0][2])], 
    #         (0.1, 1, 1))
    #     else:
    #         recta([(verticesPentagono[i][0], verticesPentagono[i][1], verticesPentagono[i][2]),
    #         (verticesPentagono[i+1][0], verticesPentagono[i+1][1], verticesPentagono[i+1][2])], 
    #         (0.1, 1, 1))

    # pendientesPentagono = []
    # for i in range(5):
    #     if i == 4:
    #         recta([(verticesPentagono[i][0], verticesPentagono[i][1], verticesPentagono[i][2]),
    #         (verticesPentagono[0][0], verticesPentagono[0][1], verticesPentagono[0][2])], 
    #         (0.1, 1, 1))
    #         pendientesPentagono.append((verticesPentagono[0][1]- verticesPentagono[i][1])/verticesPentagono[0][0]-verticesPentagono[i][0])
    #     else:
    #         recta([(verticesPentagono[i][0], verticesPentagono[i][1], verticesPentagono[i][2]),
    #         (verticesPentagono[i+1][0], verticesPentagono[i+1][1], verticesPentagono[i+1][2])], 
    #         (0.1, 1, 1))
    #         pendientesPentagono.append((verticesPentagono[i+1][1]- verticesPentagono[i][1])/verticesPentagono[i+1][0]-verticesPentagono[i][0])

    # angulosPentagono = [math.atan(i) for i in pendientesPentagono]
    # print(angulosPentagono)

    # for i in range(5):

    #     if i == 4:
    #         a = verticesPentagono[0][0] - verticesPentagono[i][0] 
    #         b = verticesPentagono[0][1] - verticesPentagono[i][1] 
    #         c = verticesPentagono[0][2] - verticesPentagono[i][2] 
    #     else:
    #         a = verticesPentagono[i+1][0] - verticesPentagono[i][0] 
    #         b = verticesPentagono[i+1][1] - verticesPentagono[i][1] 
    #         c = verticesPentagono[i+1][2] - verticesPentagono[i][2] 

    #     glPushMatrix()
    #     # glTranslate(verticesPentagono[i][0], verticesPentagono[i][1], verticesPentagono[i][2])
    #     # glRotate(180, a, b, c)
    #     # glTranslate(-verticesPentagono[i][0], -verticesPentagono[i][1], -verticesPentagono[i][2])
    #     glTranslate(X,Y,0)
    #     glRotate(xd, 0, 0, 1)
    #     for i in range(6):
    #         if i == 5:
    #             recta([(verticesHexagono[i][0], verticesHexagono[i][1], verticesHexagono[i][2]),
    #             (verticesHexagono[0][0], verticesHexagono[0][1], verticesHexagono[0][2])], 
    #             (1, 0.1, 1))
    #         else:
    #             recta([(verticesHexagono[i][0], verticesHexagono[i][1], verticesHexagono[i][2]),
    #             (verticesHexagono[i+1][0], verticesHexagono[i+1][1], verticesHexagono[i+1][2])], 
    #         (1, 0.1, 1))
    #     # poligono(verticesHexagono, (0.7, 0.7, 0.1))

    #     # poligono(verticesPentagono,  (0.7, 0.7, 0.1))

    #     glPopMatrix()

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

    pelota()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, horizontal, vertical, beta, phi, teta, xd, X, Y, angulo
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
            Y -= 0.01
        case b'a':
            X -= 0.01
        case b'w':
            Y += 0.01
        case b'd':
            X += 0.01
        case b'm':
            beta += 4
        case b'n':
            beta -= 4
        case b'l':
            angulo += 1
            print(f'angulo={angulo}')
        case b'j':
            angulo -= 1
            print(f'angulo={angulo}')

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
    glutCreateWindow("Pelota 3D (Icosaedro truncado)") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutSpecialFunc(handleSpecialKeypress)
    glutKeyboardFunc(buttons) # callback para los botones.
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()