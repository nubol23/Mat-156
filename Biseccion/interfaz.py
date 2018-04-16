import tkinter as tk
#import sympy as sym
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
from sympy.utilities import lambdify
from fractions import Fraction

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import numpy as np

def mostrar_tabla(table, out):
    if out != '':
        out += '\n'
    for (i, row) in enumerate(table):
        #print('[' + str(i + 1) + ']', row)
        out += '[' + str(i + 1) + ']'.join(row)+'\n'

    return out

def prepocess_input(inp):
    in_str = ''
    res_str = ''
    inp = inp.replace(' ','')
    decomp = inp.split('e')
    print(decomp)

    for v in decomp:
        if v == '':
            continue
        elif v[0] == 'x' and v[1] == 'p':
            print('entre1')
            res_str = res_str + 'e' + v
        else:
            if v[0] == '^':
                print('entre2')
                res_str = res_str + 'exp' + v[1:]
            else:
                print('entre3')
                res_str += v
        print('res_str:', res_str)
    for ch in res_str:
        if ch == '^':
            in_str += '**'
        else:
            in_str += ch

    print('final value:',in_str)
    return in_str

def solve_math_errors(f, a, eps):
    sw = False
    while sw == False:
        try:
            f((a-1)+eps)
            sw = True
        except ValueError:
            a += 1
    return a

def intersecciones(f, a, b, eps):
    intersect = []

    a = solve_math_errors(f, a, eps)

    prev = f((a-1)+eps)
    for x_i in range(a,b+1):

        act = f(x_i+eps)

        if act*prev <= 0 + eps:
            intersect.append((x_i - 1 + eps, x_i + eps))
        prev = act

    xs = np.linspace(-5,5, 100)
    ys = []
    for x_i in xs:
        ys.append(f(x_i))
    return intersect, xs, ys

def biseccion(a, b, its, f):
    a_orig, b_orig = a,b
    sw = False

    im_X_m = a_orig
    m_prev = nan
    while sw == False:

        table = []
        for it in range(its):

            X_m = (a + b) / 2.0

            res = X_m

            if res == m_prev:
                break

            im_a, im_b, im_X_m = f(a), f(b), f(X_m)

            table.append([str(a) + (' ^+' if im_a > 0 else ' ^-'),
                         str(b) + (' ^+' if im_b > 0 else ' ^-'),
                         str(X_m) + (' ^+' if im_X_m > 0 else ' ^-')])

            if im_X_m > 0:
                b = X_m
            else:
                a = X_m

            m_prev = X_m

        if abs(round(f(res),2)) <= round(0.1,2):
            sw = True
        else:
            b = a_orig
            a = b_orig

    return res, (True if (f(res) == 0) else False), table

class GUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Biseccion')

        self.grid()

        self.out = tk.StringVar()
        self.out.set("")
        self.lbl = tk.Label(self, text="f(x) = ")

        self.in_str = tk.Entry(self)

        self.button = tk.Button(self, text='Resolver', cursor='hand1', command=self.process)

        self.lbl.grid(row=0, sticky='nsew')
        self.in_str.grid(row=0, column=1, sticky='nsew')
        self.button.grid(row=1, columnspan=2, sticky='nsew')

        self.lbl.config(font=("Ubuntu Mono", 30) , bg='white')
        self.in_str.config(font=("Ubuntu Mono", 30), bg='white')
        self.button.config(font=("Ubuntu Mono", 30), bg='white')

        self.labels = {}
        self.s_tbl = ''
        #self.bool_table = False
        self.r = 0

        self.table_shown = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def show_tables(self, event=None):
        # Configurando las tablas
        print(self.table_shown)
        if self.table_shown == False:
            tab = tk.Text(self)
            tab.grid(row=self.r + 2, columnspan=2)
            vsb = tk.Scrollbar(self, orient='vertical', command=tab.yview)
            tab.configure(yscrollcommand=vsb.set)
            # vsb.grid(row=r+1, column=3)
            tab.insert(tk.END, self.s_tbl)

            self.labels['tab'] = tab
            self.table_shown = True
        else:
            self.labels['tab'].delete(1.0, tk.END)
            self.labels['tab'].destroy()
            self.table_shown = False

    def process(self, event = None):
        self.table_shown = False

        self.s_tbl = ''
        eps = 1e-9
        iters = 100
        for (k,v) in self.labels.items():
            if k == 'graph':
                v.get_tk_widget().destroy()
            else:
                v.destroy()

        func = prepocess_input(self.in_str.get().lower())

        transformations = (standard_transformations + (implicit_multiplication_application,))

        X = Symbol('x')
        func = parse_expr(func, transformations=transformations)
        func = lambdify((X), func)

        intersect, xs, ys = intersecciones(func, -50, 50, eps)
        self.out.set(intersect)

        # row number (starting in 2 because of inputs)
        self.r = 2
        self.grid_rowconfigure(self.r, weight=1)
        print(intersect)
        if len(intersect) == 0:
            label = tk.Label(self, text='No se encontraron soluciones')
            label.grid(row=self.r, columnspan=2, sticky='nsew')
            label.config(font=("Ubuntu Mono", 30), bg='white')
            self.labels['lbl0'] = label

        px,py = [],[]

        for e in intersect:
            res, sw, tbl = biseccion(e[0], e[1], iters, func)

            self.s_tbl = mostrar_tabla(tbl,self.s_tbl)
            #print(res, '->', abs(round(func(res), 2)))
            px.append(res)
            py.append(0)

            label = tk.Label(self, text='x'+str(self.r-1)+': '+str(res))
            print(abs(round(func(res), 2)))
            label.grid(row=self.r, columnspan=2, sticky='W')
            label.config(font=("Ubuntu Mono", 30))
            self.labels['lbl' + str(self.r - 2)] = label

            self.grid_rowconfigure(self.r, weight=1)

            self.r += 1

        fig = Figure(figsize=(5,4), dpi = 120)
        a = fig.add_subplot(111)
        a.plot(xs,ys)
        a.plot(px,py, 'ro')
        a.axhline(y=0, linewidth=0.5, color='k')
        a.axvline(x=0, linewidth=0.5,color='k')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().grid(row=self.r, columnspan=2 , sticky = 'nsew')

        self.labels['graph'] = canvas

        m_tbl = tk.Button(self, text='Mostrar Tabla', cursor='hand1', command=self.show_tables)
        m_tbl.grid(row=self.r+1, columnspan=2, sticky='nsew')
        m_tbl.config(font=("Ubuntu Mono", 30), bg='white')

        self.labels['most_tbl'] = m_tbl
        self.grid_rowconfigure(self.r+1, weight=1)

if __name__ == "__main__":
    MainWindow = GUI()
    MainWindow.bind('<Return>', MainWindow.process)
    MainWindow.mainloop()



"""
def biseccion(a, b, its, f):
    a_orig, b_orig = a,b
    sw = False

    im_X_m = a_orig
    while sw == False:
        table = [[] for i in range(its)]
        for it in range(its):

            X_m = (Decimal(a) + Decimal(b)) / 2

            res = Decimal(X_m)

            im_a, im_b, im_X_m = f(Decimal(a)), f(Decimal(b)), f(Decimal(X_m))

            table[it] = [str(Fraction(a)) + (' ^+' if im_a > 0 else ' ^-'),
                         str(Fraction(b)) + (' ^+' if im_b > 0 else ' ^-'),
                         str(Fraction(X_m)) + (' ^+' if im_X_m > 0 else ' ^-')]

            if Decimal(im_X_m) > 0:
                b = Decimal(X_m)
            else:
                a = Decimal(X_m)

        if abs(round(Decimal(f(res)),2)) <= round(Decimal(0.1),2):
            sw = True
        else:
            b = a_orig
            a = b_orig

    return Decimal(res), (True if (f(Decimal(res)) == 0) else False)
"""

"""def prepocess_input(str):
    in_str = ''
    for ch in str:
        if ch == '^':
            in_str += '**'
        else:
            in_str += ch

    return in_str"""