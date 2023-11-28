import numpy as np
from manim import *
from scipy import integrate
from scipy.stats import norm


class Trapecios(Scene):
    def construct(self):
        intervalo_A = -1
        intervalo_B = 1
        ax = Axes(
            x_range=[intervalo_A - 1, intervalo_B + 1, 1],
            y_range=[0, 1, 0.5],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))

        ##datos random con distrib normal // aca ingresarian los datos del usuario
        datos_muestreados = np.random.normal(loc=0, scale=1, size=1000)

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
                
    
        graph = ax.plot(lambda x: distribucion_normal(x), x_range=[intervalo_A - 1, intervalo_B + 1], color=RED)
        ejex = ax.plot(lambda x: 0, x_range=[intervalo_A - 1, intervalo_B + 1], color=BLUE)
        self.play(Create(graph))

        t = MathTex(r"f(x) = \frac{exp(x^2 / 2)}{\sqrt{2\pi}}")
        t.scale(0.9)
        t.set_x(3)
        t.set_y(3)

        mu = MathTex(fr"\mu = {{{round(media,3)}}}")
        mu.scale(1)
        mu.set_x(-3)
        mu.set_y(3)

        sigma = MathTex(fr"\sigma = {{{round(desviacion_estandar,3)}}}")
        sigma.scale(1)
        sigma.set_x(-3)
        sigma.set_y(2)        
        
        ar = MathTex(fr"\int_{{{intervalo_A}}}^{{{intervalo_B}}} f(x) dx = ", str(round(integrate.quad(lambda x : distribucion_normal(x),intervalo_A, intervalo_B)[0],3)))
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(2)
        ar.set_z_index(3)

        self.play(Write(t))
        self.play(Write(mu))
        self.play(Write(sigma))
        self.play(Create(ax.get_area(graph, [intervalo_A, intervalo_B])))
        self.play(Write(ar))

        traps = VGroup()
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace(1, 1/32, num=6):
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

            area = MathTex(fr"\int_{{{intervalo_A}}}^{{{intervalo_B}}} Trapecios = ",str(round(integrate.trapezoid(y,x),3)))
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


        self.wait(2)
