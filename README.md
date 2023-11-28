# Presentación Métodos Numéricos - Integrales

Repositorio de la presentación de Métodos Numéricos, respecto al tema de Integrales.

## Autores

- Gonzalez Hormigo, Juan Cruz
- Gutiérrez, Lucas
- Llobeta, Bautista

## Instalación

Clonar el repositorio e instalar el administrador de paquetes Chocolatey:

```bash
  https://chocolatey.org/install
```

Con Chocolatey instalado, correr los siguientes comandos en un cmd como Administrador (Python 3.8 en adelante):

```bash
  choco install manimce
  choco install miktex.install
  choco install scipy
  choco install numpy
```

Para poder ver las animaciones, hay dos opciones, la primera (si tiene datos de entrada, la única) es correr el comando:

```bash
  manim -pql <archivo.py> <Clase>
```

La otra manera es, en Visual Studio, instalar la extensión Manim Sideview:

```bash
  https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview
```

Para compilar, dentro del archivo que contenga la animación, presionar el boton verde generado por la extensión, al lado del botón Run, y elegir la animación a compilar. Si ya se compiló una animación y se quiere ver otra, presionar en el botón azul con una cámara debajo del video para cambiar de animación.
