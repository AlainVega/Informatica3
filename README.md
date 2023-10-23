# Informatica3
Repositorio para alojar los trabajos practicos de la materia Informatica 3 (computacion grafica)

# Probar el proyecto
Realizar los pasos en orden.
### 1. Instalar git
Para distros basadas en ubuntu, para otras distrubuciones o sistemas operativos ver en el [sitio oficial](https://git-scm.com/)
```
apt install git
```
### 2. Instalar python
Para distros basadas en ubuntu: para otras distrubuciones o sistemas operativos ver en el [sitio oficial](https://www.python.org/)
```
apt install python3
```
### 3. Crear entorno virtual y activarlo
En linux, para otros sistemas operativos ver en: https://docs.python.org/3/library/venv.html
```
python -m venv <ruta>
source <ruta>/bin/activate
```
### 4. Instalar PyOpenGL y PyOpenGL_accelerate
```
git clone https://github.com/mcfletch/pyopengl.git
cd pyopengl
pip install -e .
cd accelerate
pip install -e .
```
### 5. Clonar repositorio
```
git clone https://github.com/AlainVega/Informatica3.git
```
Nota: si es que se tienen warnings en el editor de vscode es porque, vscode
no sabe donde esta la ruta al paquete PyOpenGL y PyOpenGL_accelerate, para solucionar esto se debe:
1. ejecutar ```pip show PyOpenGL PyOpenGL_accelerate``` y copiar la ruta que dice editable
2. abrir la configuracion de vscode
3. buscar "extra paths"
4. agregar la ruta copiada en 1.

Nota: si es que se tiene problemas al ejecutar los .py puede deberse al gestor de ventanas wayland, cambiar este gestor por otro como x11,
[mas informacion aqui](https://helpdesk.psionline.com/hc/en-gb/articles/13470827149332-How-to-perform-the-switch-from-the-Wayland-display-server-to-Xorg-X11-on-Linux-Ubuntu-22-04-LTS) (en ubuntu)

