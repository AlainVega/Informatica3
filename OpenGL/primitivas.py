from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

w, h = 800,800

# ---Section 1---
def punto():
    glBegin(GL_POINTS)  
    glColor3f( 1, 0, 0 ) # rojo
    #glPointSize(1.2)
    #glEnable(GL_POINT_SMOOTH)
    glVertex2d(10, 490)
    glEnd()

def triangulo():
    glColor3f(0, 0.8, 0) # color verde
    glBegin(GL_TRIANGLES) # Begin the sketch
    glVertex2f(100, 300) # Coordinates for the bottom left point
    glVertex2f(200, 300) # Coordinates for the bottom right point
    glVertex2f(200, 350) # Coordinates for the top right point
    glEnd() # Mark the end of drawing

def cuadrado():
    glColor3f(1.0, 0.8, 0.6)
    # We have to declare the points in this sequence: bottom left, bottom right, top right, top left
    glBegin(GL_QUADS) # Begin the sketch
    glVertex2f(100, 100) # Coordinates for the bottom left point
    glVertex2f(200, 100) # Coordinates for the bottom right point
    glVertex2f(200, 200) # Coordinates for the top right point
    glVertex2f(100, 200) # Coordinates for the top left point
    glEnd() # Mark the end of drawing

def circulo():
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 0.8, 0.6)
    for i in range(64):
        angle = 6.2832 * i / 64  # 6.2832 represents 2*PI
        x = 100 * math.cos(angle) + 350
        y = 100 * math.sin(angle) + 350
        glVertex2d(x, y)
    glEnd()

def trianguloStrip():
    glColor3f(0, 0, 0.8) # color azul
    glBegin(GL_TRIANGLE_STRIP) # Begin the sketch
    glVertex2f(100, 400) # Coordinates for the bottom left point
    glVertex2f(200, 400) # Coordinates for the bottom right point
    glVertex2f(200, 450) # Coordinates for the top right point
    glVertex2d(100, 450)
    glEnd() # Mark the end of drawing

def trianguloFan():
    glColor3f(0, 0.8, 0.8) # color amarillo
    glBegin(GL_TRIANGLE_FAN) # Begin the sketch
    glVertex2f(400, 100) # Coordinates for the bottom left point
    glVertex2f(450, 150) # Coordinates for the bottom right point
    glVertex2d(400, 150) 
    glVertex2f(500, 100) # Coordinates for the top right point
    
    glEnd() # Mark the end of drawing

def cuadradoStrip():
    glColor3f(1,0,0)
    glBegin(GL_QUAD_STRIP) # Begin the sketch
    glVertex2f(500, 500) # Coordinates for the bottom left point
    glVertex2f(560, 500) # Coordinates for the bottom right point
    glVertex2f(560, 560) # Coordinates for the top right point
    glVertex2f(500, 560) # Coordinates for the top left point
    glVertex2f(500, 600) # Coordinates for the top right point
    glVertex2f(600, 600) # Coordinates for the top left point
    glEnd() # Mark the end of drawing
    
def poligono():
    glColor3f(1,0,0)
    glBegin(GL_POLYGON) # Begin the sketch
    glVertex2f(500, 500) # Coordinates for the bottom left point
    glVertex2f(560, 500) # Coordinates for the bottom right point
    glVertex2f(600, 560) # Coordinates for the top right point
    glVertex2f(640, 600) # Coordinates for the top left point
    glVertex2f(600, 500) # Coordinates for the top right point
    glEnd() # Mark the end of drawing
# This alone isn't enough to draw our square

# Add this function before Section 2 of the code above i.e. the showScreen function
def iterate():
    glViewport(0, 0, 500,500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ---Section 2---

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
    glLoadIdentity() # Reset all graphic/shape's position
    iterate()
    punto()
    triangulo()
    cuadrado() # Draw a square using our function
    circulo()
    trianguloStrip()
    trianguloFan()
    cuadradoStrip() # no anda  
    poligono() # no anda 
    glutSwapBuffers()

#---Section 3---

glutInit()
glutInitDisplayMode(GLUT_RGBA) # Set the display mode to be colored
glutInitWindowSize(w, h)   # Set the w and h of your window
glutInitWindowPosition(1000, 100)   # Set the position at which this windows should appear
wind = glutCreateWindow("Dibujar primitivas") # Set a window title
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen) # Keeps the window open
glutMainLoop()  # Keeps the above created window displaying/running in a loop