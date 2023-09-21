from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

w,h = 800, 800

def square(r,g,b):
    glColor3f(r,g,b);  # Set the color for the square.
    glBegin(GL_TRIANGLE_FAN);
    glVertex3f(-0.5, -0.5, 0.5);
    glVertex3f(0.5, -0.5, 0.5);
    glVertex3f(0.5, 0.5, 0.5);
    glVertex3f(-0.5, 0.5, 0.5);
    glEnd();

def cube(size):
    # Draws a cube with side length = size.
    glPushMatrix();  # Save a copy of the current matrix.
    glScalef(size,size,size); # Scale unit cube to desired size.
    
    square(1, 0, 0); # red front face
    
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    square(0, 1, 0); # green right face
    glPopMatrix();
    
    glPushMatrix();
    glRotatef(-90, 1, 0, 0);
    square(0, 0, 1); # blue top face
    glPopMatrix();
    
    glPushMatrix();
    glRotatef(180, 0, 1, 0);
    square(0, 1, 1); # cyan back face
    glPopMatrix();
    
    glPushMatrix();
    glRotatef(-90, 0, 1, 0);
    square(1, 0, 1); # magenta left face
    glPopMatrix();
    
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    square(1, 1, 0); # yellow bottom face
    glPopMatrix();
    
    glPopMatrix(); # Restore matrix to its state before cube() was called.

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
    cube(5) # Draw a square using our function
    glutSwapBuffers()

#---Section 3---

glutInit()
glutInitDisplayMode(GLUT_RGBA) # Set the display mode to be colored
glutInitWindowSize(w, h)   # Set the w and h of your window
glutInitWindowPosition(1000, 100)   # Set the position at which this windows should appear
wind = glutCreateWindow("Cubo") # Set a window title
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen) # Keeps the window open
glutMainLoop()  # Keeps the above created window displaying/running in a loop