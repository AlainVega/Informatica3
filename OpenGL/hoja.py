# Dibujar una hoja

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
cantidadHojasPar = 4 # cantidad pares de hojas de la rama
alturaHoja = 0.1 # altura del tallo de cada hoja
beta = math.radians(45) # angulo de inclinacion respecto a la recta raiz

# Sirve para dibujar la cara del poligono. (Pintar el ancho del hoja)
def cara(vertices, color):
    # Setear las propiedades del material.
    # c = [color[0], color[1], color[2], 1]
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, c) 
    # glMaterialfv(GL_FRONT, GL_SPECULAR, rojo) 
    # glMaterialfv(GL_FRONT, GL_EMISSION, c) 
    # glMaterialfv(GL_FRONT, GL_SHININESS, 10) 
    # glMaterialfv(GL_FRONT, GL_AMBIENT, c) 

    glColor(color[0], color[1], color[2], 1) # pintar con este color

    glBegin(GL_TRIANGLE_FAN) # dibuja triangulos para simular el hexagono.
    for vertice in vertices:
        glVertex3fv(vertice)
    glEnd() # fin del contexto de triangulos

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

# Sirve para definir la hoja .
def hoja():
    verticesHoja = []

    ejes() # pintar los ejes X=rojo, Y=verde, Z=azul

    verdePlanta = (45/255, 87/255, 44/255)

    # USANDO EL ALGORITMO DEL PINTOR 
    # (dibujar primero los objetos lejanos, los de atras)
    # Vertices en sentido antihorario
    vInicial = (0,0,0)
    vFinal = (0.5, 0.5, 0)
    verticesHoja.append(vInicial)
    verticesHoja.append(vFinal)
    m = (vFinal[1]-vInicial[1])/(vFinal[0]-vInicial[0])
    alpha = math.atan(m)
    rectaStrip(verticesHoja, verdePlanta)

    cX = vFinal[0]/cantidadHojasPar
    cY = vFinal[1]/cantidadHojasPar
    puntosHojas = []
    for i in range(cantidadHojasPar):
        puntosHojas.append((verticesHoja[0][0] + i*cX, verticesHoja[0][1] + i*cY, 0))
        # punto([(verticesHoja[0][0] + i*cX, verticesHoja[0][1] + i*cY, 0)], (0.1, 0.7, 0.2))

    # punto(puntosHojas, (0.1, 0.7, 0.2))

    puntosExternos = []
    puntosExternos.append((puntosHojas[0][0] + alturaHoja*math.cos(alpha + beta), puntosHojas[0][1] + alturaHoja*math.sin(alpha + beta), 0))

    a = puntosExternos[0][0] - puntosHojas[0][0] 
    b = puntosExternos[0][1] - puntosHojas[0][1] 
    c = 0

    vectorRaiz = (a,b,c)
    normalRaiz1 = (-b,a,c)
    normalRaiz2 = (b,-a,c)

    # hojas de arriba
    for i in range(0, cantidadHojasPar):
        glPushMatrix()
        v1, v2, v3 = puntosHojas[i][0], puntosHojas[i][1], puntosHojas[i][2]
        glTranslate(v1, v2, v3)
        bezier1 = bezierCuadratico(puntosHojas[0], (a + normalRaiz1[0], b + normalRaiz1[1], 0 ), puntosExternos[0])
        bezier2 = bezierCuadratico(puntosHojas[0], (a + normalRaiz2[0], b + normalRaiz2[1], 0 ), puntosExternos[0])
        rectaLoop(bezier1, verdePlanta)
        rectaLoop(bezier2,  verdePlanta)
        glPopMatrix()

    # hojas de abajo
    for i in range(0, cantidadHojasPar):
        glPushMatrix()
        v1, v2, v3 = vFinal[0] - vInicial[0], vFinal[1] - vInicial[1], vFinal[2] - vInicial[2]
        glTranslate(puntosHojas[i][0], puntosHojas[i][1], puntosHojas[i][2])
        glRotate(180, v1, v2, v3)
        bezier1 = bezierCuadratico(puntosHojas[0], (a + normalRaiz1[0], b + normalRaiz1[1], 0 ), puntosExternos[0])
        bezier2 = bezierCuadratico(puntosHojas[0], (a + normalRaiz2[0], b + normalRaiz2[1], 0 ), puntosExternos[0])
        rectaLoop(bezier1,  verdePlanta)
        rectaLoop(bezier2,  verdePlanta)
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

    hoja()

# Captura las teclas
def buttons(key, x, y):
    global ojoz, ojox, ojoy, teta, phi, radio, cantidadHojasPar, alturaHoja, beta
    print(f'key={key}')
    match key:
        case b'r':
            ojox, ojoy, ojoz, = x0, y0, z0
            teta = math.acos(ojoz/radio) # angulo vertical de la camara (PLANO YOZ, X = constante)
            phi = math.asin(ojoz/radio) # angulo horizontal de la camara (PLANO XOZ, Y = constante)
            cantidadHojasPar = 4
            alturaHoja = 0.1
            beta = math.radians(45)
            print('La figura volvio a su tamanho y disposicion inicial.')
        case b's':
            if alturaHoja > 0.05:
                alturaHoja -= 0.01
        case b'a':
            beta -= 0.1
        case b'w':
            alturaHoja += 0.01
        case b'd':
            beta += 0.1
        case b'+':
            cantidadHojasPar += 1
        case b'-':
            if cantidadHojasPar > 1:
                cantidadHojasPar -= 1

    glutPostRedisplay() # Dibuja otra vez.

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

# Funcion principal.
def main():
    glutInit(sys.argv) # Inicializa el motor OpenGL
    glutInitDisplayMode(GLUT_RGB) # Elige el modelo de colores
    glutInitWindowSize(ancho, alto) # Dar el ancho y alto de la ventana
    glutInitWindowPosition(1000, 100) # Posicion absoluta de la ventana emergente. (0,0) es de arriba a la izquierda
    glutCreateWindow("hoja ") # Crear ventana emergente y darle titulo.
    glutDisplayFunc(display) # Que pinte la funcion
    glutKeyboardFunc(buttons) # callback para los botones.
    glutSpecialFunc(handleSpecialKeypress)
    glutMainLoop() # mantiene la ventana corriendo en bucle.
    
main()