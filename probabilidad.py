import numpy as np
from manim import *
from scipy import integrate
from scipy.stats import norm


class Trapecios(Scene):
    def construct(self):

        valorA = input("Ingrese el valor A: ")
        valorB = input("Ingrese el valor B: ")

        if valorA == '' :
            valorA = 0
        else:
            valorA = float(valorA)

        if valorB == '' :
            valorB = 0
        else:
            valorB = float(valorB)

        ## Datos de Pases de Messi : https://fbref.com/es/jugadores/d70ce98e/partidos/2022-2023/passing/Registros-de-partidos-de-Lionel-Messi
        datos = [47,35,38,51,59,36,34,41,49,56,45,45,50,66,42,64,55,60,43,49,71,62,59,51,40,62,32,19,51,64,51,57,46,43,52,52,32,36,60,56,73,56,43,49,56,55,33,14,14,36,52,12,69,64,65,39,53,43,53,33,27,23,84,68,58,63,62,34,56,47,55,63,64,63,63,56,27,70,35,57,56,66,79,16,47,51,40,20]
        mediadatos = np.mean(datos)
        desvdatos = np.std(datos)

        if valorA == 0:
            intervalo_A = -3
        else:
            intervalo_A = (valorA - mediadatos)/desvdatos # normaliza los datos

        if valorB == 0:
            intervalo_B = 3
        else:
            intervalo_B = (valorB - mediadatos)/desvdatos # normaliza los datos

        datos_muestreados = (datos - mediadatos)/desvdatos # normaliza los datos


        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.5],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))

        media = np.mean(datos_muestreados) # calcula la media
        desviacion_estandar = np.std(datos_muestreados) ## calcula la desviac (chequear CUAL formula usa)

        def distribucion_normal(x):
            return norm.pdf(x, media, desviacion_estandar)

        # Cálculo de probabilidad usando la regla del trapecio con n = 1024
        x = np.arange(intervalo_A, intervalo_B,1/512)
        y = [distribucion_normal(a) for a in x]
        probabilidad = integrate.trapezoid(y,x)
        print("media: ", media)
        print("desviac: " , desviacion_estandar)
        print("La probabilidad es:", probabilidad)
                
    
        graph = ax.plot(lambda x: distribucion_normal(x), x_range=[-3, 3], color=RED)
        ejex = ax.plot(lambda x: 0, x_range=[-3, 3], color=BLUE)
        self.play(Create(graph))

        t = MathTex(r"f(x) = \frac{exp(x^2 / 2)}{\sqrt{2\pi}}")
        t.scale(0.9)
        t.set_x(3)
        t.set_y(3)

        if valorA == 0:
            valorA = r"-\infty"
        if valorB == 0:
            valorB = r"\infty"

        xa = MathTex(fr"x^a = {{{valorA}}}")
        xa.scale(0.8)
        xa.set_x(-3)
        xa.set_y(3)

        xb = MathTex(fr"x^b = {{{valorB}}}")
        xb.scale(0.8)
        xb.set_x(-3)
        xb.set_y(2)

        za = MathTex(fr"z^a = {{{round(intervalo_A,3)}}}")
        za.scale(0.8)
        za.set_x(-3)
        za.set_y(1)

        zb = MathTex(fr"z^b = {{{round(intervalo_B,3)}}}")
        zb.scale(0.8)
        zb.set_x(-3)
        zb.set_y(0)            
        
        ar = MathTex(fr"\int_{{{round(intervalo_A,3)}}}^{{{round(intervalo_B,3)}}} f(x) dx = ", str(round(integrate.quad(lambda x : distribucion_normal(x),intervalo_A, intervalo_B)[0],3)))
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(2)
        ar.set_z_index(3)

        self.play(Write(t))
        self.play(Write(xa))
        self.play(Write(xb))
        self.play(Write(za))
        self.play(Write(zb))
        self.play(Create(ax.get_area(graph, [intervalo_A, intervalo_B])))
        self.play(Write(ar))

        traps = VGroup()
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace((intervalo_B-intervalo_A)/2, (intervalo_B-intervalo_A)/64, num=6):
            i = 0
            trap = VGroup()
            for i in np.arange(intervalo_A, intervalo_B,dx):
                b = i + dx
                if b > intervalo_B:
                    b = intervalo_B
                trapact = Polygon(ax.i2gp(i, graph), ax.i2gp(b, graph), ax.i2gp(b, ejex), ax.i2gp(i, ejex))
                trap.add(trapact)
            trap.set_fill(color_gradient([BLUE,GREEN], int((intervalo_B-intervalo_A)/dx)),1,True)
            x = np.arange(intervalo_A, intervalo_B,dx)
            y = [distribucion_normal(a) for a in x]
            trapecio = round(integrate.trapezoid(y,x),3)
            area = MathTex(fr"\int_{{{round(intervalo_A,3)}}}^{{{round(intervalo_B,3)}}} Trapecios = ",str(trapecio))
            area.scale(0.9)
            area.set_x(3)
            area.set_y(0.8)
            area.set_z_index(3)

            error = MathTex("Error = ",str(round(abs(integrate.trapezoid(y,x) - probabilidad),3)))
            error.scale(0.7)
            error.set_x(3)
            error.set_y(-0.2)

            ns.append(MathTex("n = ",str(round((intervalo_B-intervalo_A)/dx))).scale(0.7).set_x(3).set_y(0.3))
            areas.append(area)
            errores.append(error)
            traps.add(trap)
        
        self.play(
            DrawBorderThenFill(
                traps[0],
                run_time=2,
                rate_func=smooth,
                lag_ratio=0.5,
            ),
            Write(areas[0]),
            Write(ns[0]),
            Write(errores[0])
        )
        self.wait()

        for i in range(1, len(traps)):
            self.play(
                Transform(
                    traps[0], traps[i],
                    run_time=1,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    areas[0][1], areas[i][1],
                    run_time=1,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    errores[0][1], errores[i][1],
                    run_time=1,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    ns[0][1], ns[i][1],
                    run_time=1,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
            )


        self.wait(1)

        pos = MathTex(fr"P({{{valorA}}}\le x<{{{valorB}}})={{{trapecio}}}")
        pos.scale(0.8)
        pos.set_x(-3)
        pos.set_y(2) 
        self.play(Unwrite(xa))
        self.play(Unwrite(xb))
        self.play(Unwrite(za))
        self.play(Unwrite(zb))
        self.play(Write(pos))

        self.wait(5)
