from manim import *
from scipy.interpolate import lagrange
from scipy import integrate
from numpy.polynomial.polynomial import Polynomial
import numpy as np

class Rectangulos(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1, 7, 1],
            y_range=[0, 14, 2],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))
        
        def f(x):
            return -0.25*(x-3)**4 + 3*(x-3)**2 + x - 2
    
        graph = ax.plot(lambda x: f(x), x_range=[-1, 7], color=RED)
        ejex = ax.plot(lambda x: 0, x_range=[-1, 7], color=BLUE)
        self.play(Create(graph))

        t = MathTex(r"f(x) = -0.25(x-3)^4 + 3(x-3)^2 + x - 2")
        t.scale(0.9)
        t.set_x(3)
        t.set_y(3)
        
        ar = MathTex(r"\int_0^6 f(x) dx = 35.699")
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(2)
        ar.set_z_index(3)
        self.play(Write(t))
        self.play(Create(ax.get_area(graph, [0,6])))
        self.play(Write(ar))

        rects = VGroup()
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace(1, 0.0625, num=5):
            rect = ax.get_riemann_rectangles(
                graph,
                x_range=[0,6],
                dx=dx,
                stroke_width=4*dx,
            )
            x = np.arange(0,6,dx)
            y = [f(a) for a in x]

            area = MathTex(r"\int_0^6 Rectangulos = ",str(round(rectangulo(x,y),3)))
            area.scale(0.9)
            area.set_x(3)
            area.set_y(0.8)

            error = MathTex("Error = ",str(round(abs(rectangulo(x,y) - 35.699),3)))
            error.scale(0.7)
            error.set_x(3)
            error.set_y(-0.2)

            ns.append(MathTex("n = ",str(round(6/dx))).scale(0.7).set_x(3).set_y(0.3))
            areas.append(area)
            errores.append(error)
            rects.add(rect)

        self.play(
            DrawBorderThenFill(
                rects[0],
                run_time=2,
                rate_func=smooth,
                lag_ratio=0.5,
            ),
            Write(areas[0]),
            Write(ns[0]),
            Write(errores[0])
        )
        self.wait()

        for i in range(1, len(rects)):
            self.play(
                Transform(
                    rects[0], rects[i],
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

class Trapecios(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1, 7, 1],
            y_range=[0, 14, 2],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))
        
        def f(x):
            return -0.25*(x-3)**4 + 3*(x-3)**2 + x - 2
    
        graph = ax.plot(lambda x: f(x), x_range=[-1, 7], color=RED)
        ejex = ax.plot(lambda x: 0, x_range=[-1, 7], color=BLUE)
        self.play(Create(graph))

        t = MathTex(r"f(x) = -0.25(x-3)^4 + 3(x-3)^2 + x - 2")
        t.scale(0.9)
        t.set_x(3)
        t.set_y(3)
        
        ar = MathTex(r"\int_0^6 f(x) dx = 35.699")
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(2)
        ar.set_z_index(3)

        self.play(Write(t))
        self.play(Create(ax.get_area(graph, [0,6])))
        self.play(Write(ar))

        traps = VGroup()
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace(1, 0.0625, num=5):
            i = 0
            trap = VGroup()
            for i in np.arange(0,6,dx):
                b = i + dx
                trapact = Polygon(ax.i2gp(i, graph), ax.i2gp(b, graph), ax.i2gp(b, ejex), ax.i2gp(i, ejex))
                trap.add(trapact)
            trap.set_fill(color_gradient([BLUE,GREEN], int(6/dx)),1,True)
            x = np.arange(0,6,dx)
            y = [f(a) for a in x]

            area = MathTex(r"\int_0^6 Trapecios = ",str(round(integrate.trapezoid(y,x),3)))
            area.scale(0.9)
            area.set_x(3)
            area.set_y(0.8)
            area.set_z_index(3)

            error = MathTex("Error = ",str(round(abs(integrate.trapezoid(y,x) - 35.699),3)))
            error.scale(0.7)
            error.set_x(3)
            error.set_y(-0.2)

            ns.append(MathTex("n = ",str(round(6/dx))).scale(0.7).set_x(3).set_y(0.3))
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

class Simpson(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1, 7, 1],
            y_range=[0, 14, 2],
            tips=False,
            axis_config={"include_numbers": True},
        )
        self.play(Create(ax))
        
        def f(x):
            return -0.25*(x-3)**4 + 3*(x-3)**2 + x - 2
    
        graph = ax.plot(lambda x: f(x), x_range=[-1, 7], color=RED)
        ejex = ax.plot(lambda x: 0, x_range=[-1, 7], color=BLUE)
        self.play(Create(graph))

        t = MathTex(r"f(x) = -0.25(x-3)^4 + 3(x-3)^2 + x - 2")
        t.scale(0.9)
        t.set_x(3)
        t.set_y(3)
        
        ar = MathTex(r"\int_0^6 f(x) dx = 35.699")
        ar.scale(1)
        ar.set_x(3)
        ar.set_y(2)
        self.play(Write(t))
        self.play(Create(ax.get_area(graph, [0,6])))
        self.play(Write(ar))

        polys = []
        areas = []
        errores = []
        ns = []
        for dx in np.geomspace(0.5, 0.0625, num=4):
            poly = VGroup()
            for i in np.arange(dx*2,6+dx,dx*2):
                x = [i-dx*2,i-dx,i]
                y = [f(a) for a in x]
                coefs = Polynomial(lagrange(x,y)).coef
                polyact = ax.plot(lambda t: coefs[0] *(t**2) + coefs[1] * t + coefs[2],x_range = [i-dx*2,i], color = color_gradient([BLUE,GREEN], int(5/dx)))
                polyact = ax.get_area(polyact, [i-dx*2,i])
                poly.add(polyact)
            x = np.arange(0,6,dx)
            y = [f(a) for a in x]
        
            area = MathTex(r"\int_0^6 Simpson = ",str(round(integrate.simpson(y,x),3)))
            area.scale(0.9)
            area.set_x(3)
            area.set_y(0.78)

            error = MathTex("Error = ",str(round(abs(integrate.simpson(y,x) - 35.699),3)))
            error.scale(0.7)
            error.set_x(3)
            error.set_y(-0.2)

            ns.append(MathTex("n = ",str(round(6/dx))).scale(0.7).set_x(3).set_y(0.3))
            areas.append(area)
            errores.append(error)
            polys.append(poly)
        
        self.play(
            Create(polys[0]),
            Write(areas[0]),
            Write(ns[0]),
            Write(errores[0])
        )
        self.wait()

        for i in range(1, len(polys)):
            self.play(
                Transform(
                    polys[0], polys[i],
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

def rectangulo(x,y):
    n = len(x) - 1
    suma = 0
    for i in range(1,n):
        suma = suma + (x[i] - x[i-1]) * y[i-1]
    return suma
        