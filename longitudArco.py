import numpy as np
import math
from manim import *
from scipy import integrate
from scipy import interpolate as sc
from scipy.stats import norm


class Pato(Scene):
    def construct(self):


        xs=np.array([0.9,1.3,1.9,2.1,2.6,3.0,3.9,4.4,4.7,5.0,6.0,7.0,8.0,9.2,10.5,11.3,11.6,12.0,12.6,13.0,13.3])
        ys=np.array([1.3,1.5,1.85,2.1,2.6,2.7,2.4,2.15,2.05,2.1,2.25,2.3,2.25,1.95,1.4,0.9,0.7,0.6,0.5,0.4,0.25])
        cs=sc.CubicSpline(xs,ys,0)

        def csFunc(xi):
            return cs(xi)

        def csPrima(xi):
            return cs.derivative(1)(xi)

        def funcionIntegrando(xi):
            return math.sqrt(1+(csPrima(xi) ** 2))

        ax = Axes(
            x_range=[min(xs) - 1, max(xs) + 1, round(math.sqrt(max(xs) - min(xs))/2)],
            y_range=[min(ys) - 1, max(ys) + 1, round(math.sqrt(max(ys) - min(ys))/2)],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))

        graph = ax.plot(lambda x: csFunc(x), x_range=[min(xs), max(xs)], color=RED)
        der = ax.plot(lambda x: funcionIntegrando(x), x_range=[min(xs), max(xs)], color=GREEN)
        ejex = ax.plot(lambda x: 0, x_range=[min(xs), max(xs)], color=BLUE)
        self.play(Create(graph))
        self.play(Create(der))
        
        valorReal = integrate.quad(lambda x : funcionIntegrando(x),min(xs), max(xs))[0]
        ar = MathTex(fr"\int_{{{round(min(xs),3)}}}^{{{round(max(xs),3)}}}",r" \sqrt{1 + {f'(x)}^2} dx = " , str(round(valorReal,3)))
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(3)
        ar.set_z_index(3)
        areaDer = ax.get_area(der, [min(xs), max(xs)])
        self.play(Create(areaDer))
        self.play(Write(ar))

        
        traps = VGroup()
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace((max(xs)-min(xs))/2, (max(xs)-min(xs))/128, num=7):
            trap = VGroup()
            for i in np.arange(min(xs), max(xs),dx):
                b = i + dx
                if b > max(xs):
                    b = max(xs)
                trapact = Polygon(ax.i2gp(i, der), ax.i2gp(b, der), ax.i2gp(b, ejex), ax.i2gp(i, ejex))
                trap.add(trapact)
            trap.set_fill(color_gradient([BLUE,GREEN], int((max(xs)-min(xs))/dx)),1,True)
            xa = np.arange(min(xs), max(xs),dx)
            ya = [funcionIntegrando(a) for a in xa]
            trapecio = round(integrate.trapezoid(ya,xa),3)
            area = MathTex(fr"\int_{{{round(min(xs),3)}}}^{{{round(max(xs),3)}}} Trapecios = ",str(trapecio))
            area.scale(0.9)
            area.set_x(3)
            area.set_y(1.8)
            area.set_z_index(3)

            error = MathTex("Error = ",str(round(abs(integrate.trapezoid(ya,xa) - valorReal),3)))
            error.scale(0.7)
            error.set_x(3)
            error.set_y(0.8)

            ns.append(MathTex("n = ",str(round((max(xs)-min(xs))/dx))).scale(0.7).set_x(3).set_y(1.3))
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
                    run_time=1.5,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    areas[0][1], areas[i][1],
                    run_time=1.5,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    errores[0][1], errores[i][1],
                    run_time=1.5,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
                Transform(
                    ns[0][1], ns[i][1],
                    run_time=1.5,
                    rate_func=smooth,
                    lag_ratio=0.5,
                ),
            )

        self.wait(2)

        self.play(
            FadeOut(traps[0]),
            FadeOut(areas[0]),
            FadeOut(errores[0]),
            FadeOut(ns[0]),
            FadeOut(der),
            FadeOut(areaDer),
            Transform(ar,MathTex(fr"Longitud = {round(trapecio,3)}").scale(1).set_x(0).set_y(3).set_z_index(3)),
        )

        self.wait(5)
