import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty
from kivy.graphics import Rectangle, Color

import boolean

Builder.load_file('gates.kv')


class Gate(Widget):

    def __init__(self, pos=(0, 0), **kwargs):
        super(Gate, self).__init__(**kwargs)
        self.pos = pos
        self.center_x = pos[0]
        self.center_y = pos[1]

    def get_pos(self):
        return self.pos


class NotGate(Gate):
    name = StringProperty("")

    def __init__(self, name, **kwargs):
        super(NotGate, self).__init__(**kwargs)
        self.name = name

    def get_output(self):
        output = (self.center_x + 35, self.center_y)
        return output

    def get_input(self):
        input = (self.center_x - 35, self.center_y)
        return input


class OrGate(Gate):
    name = StringProperty("")

    def __init__(self, name, **kwargs):
        super(OrGate, self).__init__(**kwargs)
        self.name = name

    def get_output(self):
        output = (self.center_x + 35, self.center_y)
        return output

    def get_input1(self):
        input = (self.center_x - 35, self.center_y + 15)
        return input

    def get_input2(self):
        input = (self.center_x - 35, self.center_y - 15)
        return input


class AndGate(Gate):
    name = StringProperty("")

    def __init__(self, name, **kwargs):
        super(AndGate, self).__init__(**kwargs)
        self.name = name

    def get_output(self):
        output = (self.center_x + 35, self.center_y)
        return output

    def get_input1(self):
        input = (self.center_x - 35, self.center_y + 15)
        return input

    def get_input2(self):
        input = (self.center_x - 35, self.center_y - 15)
        return input


class Symbol(Gate):
    name = StringProperty("")

    def __init__(self, name, **kwargs):
        super(Symbol, self).__init__(**kwargs)
        self.name = name

    def get_output(self):
        output = (self.center_x + 50, self.center_y)
        return output


class Output(Gate):
    name = StringProperty("")

    def __init__(self, name, **kwargs):
        super(Output, self).__init__(**kwargs)
        self.name = name

    def get_input(self):
        output = (self.center_x - 35, self.center_y)
        return output


class Temp(Gate):

    def __init__(self, output=(0,0), **kwargs):
        super(Temp, self).__init__(**kwargs)
        self.output = output

    def get_output(self):
        return self.output


class Wire(Widget):
    start_x = NumericProperty(0)
    start_y = NumericProperty(0)
    stop_x = NumericProperty(0)
    stop_y = NumericProperty(0)
    exp = StringProperty("")

    def __init__(self, exp, start=(0, 0), stop=(0, 0), **kwargs):
        super(Wire, self).__init__(**kwargs)
        self.exp = str(exp)
        self.start_x = start[0]
        self.start_y = start[1]
        self.stop_x = stop[0]
        self.stop_y = stop[1]


def renderable_components(expression):
    """
    Returns an list of renderable components when given an expression.
    """
    if isinstance(expression, str):
        expression = boolean.parse(expression, eval=False)
    if not isinstance(expression, boolean.Expression):
        raise TypeError(
            "Argument must be str or Expression but it is {}"
            .format(expression.__class__))


    def get_max_depth(e, max_depth, depth):
        if isinstance(e, boolean.Symbol):
            if max_depth < depth:
                max_depth += 1
            return max_depth
        elif isinstance(e, boolean.NOT):
            if max_depth < depth:
                max_depth += 1
            max_d = get_max_depth(e.args[0], max_depth, depth+1)
        elif isinstance(e, boolean.DualBase):
            if len(e.args) != 2:
                new_expr = e.__class__(e.args[0], e.args[1])
                for i in range(2, len(e.args)):
                    new_expr = e.__class__(new_expr, e.args[i], eval=False)
                e = new_expr
            if max_depth < depth:
                max_depth += 1
            max_d0 = get_max_depth(e.args[0], max_depth, depth+1)
            max_d1 = get_max_depth(e.args[1], max_depth, depth+1)
            if max_d1 > max_d0:
                max_d = max_d1
            else:
                max_d = max_d0
        return max_d

    max_depth = get_max_depth(expression, 0, 0)
    width = (50 * (2 ** max_depth))/2
    no_component = [0]
    symbols = {}
    no_symbols = [0]

    print(max_depth)
    print(width)


    def recursive_components(e, depth, width):
        # This function can be used if there is ever the want to attempt to make the
        # converted logic circuit look nicer by spacing the components

        if isinstance(e, boolean.Symbol):
            if e in symbols.keys():
                pos = symbols[e]
                rc = Symbol(str(e), pos=pos)
                print("sym")
                print(no_symbols[0])
            else:
                x = 20
                y = width
                pos = (x + (no_symbols[0] * 10), 35 + y)
                rc = Symbol(str(e), pos=pos)
                symbols[e] = pos
                no_symbols[0] += 1
                print("sym")
                print(no_symbols[0])
        elif isinstance(e, boolean.NOT):
            x = 35 + (120 * (max_depth - depth))
            y = width
            pre = recursive_components(e.args[0], depth+1, width)
            print(max_depth)
            print(depth)
            pos = (x, 35 + y)
            print(pos)
            no = str(no_component[0])
            no_component[0] += 1
            g = NotGate("N"+no, pos=pos)
            start = pre.get_output()
            stop = g.get_input()
            output = g.get_output()
            w = Wire(e.args[0], start, stop)
            temp = Temp(output=output)
            temp.add_widget(pre)
            temp.add_widget(w)
            temp.add_widget(g)
            rc = temp
        elif isinstance(e, boolean.DualBase):
            if len(e.args) != 2:
                new_expr = e.__class__(e.args[0], e.args[1])
                for i in range(2, len(e.args)):
                    new_expr = e.__class__(new_expr, e.args[i], eval=False)
                e = new_expr

            x = 35 + (120 * (max_depth - depth))
            y = width
            w = ((50 * (2 ** (max_depth - depth)))/2)
            print(y)
            print(w)

            pre0 = recursive_components(e.args[0], depth + 1, width + w/2)
            pre1 = recursive_components(e.args[1], depth + 1, width - w/2)
            print(max_depth)
            print(depth)

            pos = (x, 35 + y)
            print(pos)
            no = str(no_component[0])
            no_component[0] += 1

            if isinstance(e, boolean.AND):
                g = AndGate("A"+no, pos=pos)
            elif isinstance(e, boolean.OR):
                g = OrGate("O"+no, pos=pos)
            start0 = pre0.get_output()
            stop0 = g.get_input1()
            start1 = pre1.get_output()
            stop1 = g.get_input2()
            output = g.get_output()
            w0 = Wire(e.args[0], start0, stop0)
            w1 = Wire(e.args[1], start1, stop1)
            temp = Temp(output=output)
            temp.add_widget(pre0)
            temp.add_widget(pre1)
            temp.add_widget(w0)
            temp.add_widget(w1)
            temp.add_widget(g)
            rc = temp
        return rc

    rc = recursive_components(expression, 0, width)
    pos = (35 + (120 * (max_depth + 1)), width + 35)
    print("jj")
    print(pos)
    g = Output(str(expression), pos=pos)
    start = rc.get_output()
    stop = g.get_input()
    w0 = Wire("", start, stop)
    temp = Temp(height=2*width, width=max_depth*120+35)
    temp.add_widget(g)
    temp.add_widget(rc)
    temp.add_widget(w0)
    # temp.size = (max_depth * 125, width)
    print(temp.size)
    return temp

