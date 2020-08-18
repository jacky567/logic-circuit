import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window

import circuit
import boolean


# class to displays the title of the app
class Title(Label):

    def __init__(self, **kwargs):
        super(Title, self).__init__(**kwargs)
        self.text = "LOGIC CIRCUIT"
        self.text_size = self.size
        self.font_size = 25
        self.halign = 'center'
        self.valign = 'middle'


# class for the menu bar
class Menu(BoxLayout):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.clear = Button(text="Clear")
        # self.settings = Button(text="Settings")
        self.hlp = Button(text="Help")
        # self.about = Button(text="About")
        self.add_widget(self.clear)
        # self.add_widget(self.settings)
        self.add_widget(self.hlp)
        # self.add_widget(self.about)
        self.clear.bind(on_press=self.clear_all)

    def clear_all(self, obj):
        root.drawingboard.clear_widgets()
        root.taskpanel.inp.text = ""


# class for the task panel
class TaskPanel(FloatLayout):

    def __init__(self, **kwargs):
        super(TaskPanel, self).__init__(**kwargs)
        self.lab = Label(text="Enter Boolean Expression:", size_hint_x=0.2, size_hint_y=0.2, pos_hint={'x': .25, 'y': .85})
        self.inp = TextInput(size_hint_x=0.9, size_hint_y=0.1, pos_hint={'x': .05, 'y': .8}, font_size=25)
        self.error = Label(size_hint_x=0.2, size_hint_y=0.2, pos_hint={'x': .25, 'y': .68}, color=(1, 0, 0, 1))
        self.simplify = Button(text="Simplify", size_hint_x=0.8, size_hint_y=0.1, pos_hint={'x': .1, 'y': .6})
        self.truthtable = Button(text="Truth Table", size_hint_x=0.8, size_hint_y=0.1, pos_hint={'x': .1, 'y': .4})
        self.logiccircuit = Button(text="Logic Circuit", size_hint_x=0.8, size_hint_y=0.1, pos_hint={'x': .1, 'y': .2})
        self.add_widget(self.lab)
        self.add_widget(self.inp)
        self.add_widget(self.error)
        self.add_widget(self.simplify)
        self.add_widget(self.truthtable)
        self.add_widget(self.logiccircuit)
        self.simplify.bind(on_press=self.simplify_expression)
        self.truthtable.bind(on_press=self.draw_truthtable)
        self.logiccircuit.bind(on_press=self.draw_circuit)

    def simplify_expression(self, obj):
        try:
            txt = self.inp.text
            db = root.drawingboard
            sim_exp = boolean.parse(txt)
            exp = Label(text=str(sim_exp), pos=self.pos, size=self.size, font_size=75, color=[0, 0, 0, 1])
            db.clear_widgets()
            db.add_widget(exp)
            self.error.text = ""
        except:
            error = "Invalid Expression"
            self.error.text = error

    def draw_truthtable(self, obj):
        try:
            txt = self.inp.text
            table = TruthTable(txt)
            db = root.drawingboard
            db.clear_widgets()
            db.add_widget(table)
            self.error.text = ""
        except:
            error = "Invalid Expression"
            self.error.text = error

    def draw_circuit(self, obj):
        txt = self.inp.text
        db = root.drawingboard
        cir = circuit.renderable_components(txt)
        cir.pos = self.pos
        x = cir.size[0] + 200
        y = cir.size[1] + 100
        if x < 500:
            x = 500
        if y < 500:
            y = 500
        cir.size_hint_x = None
        cir.size_hint_y = None
        cir.size = (x, y)
        db.clear_widgets()
        db.add_widget(cir)
        self.error.text = ""
        # try:
        #     txt = self.inp.text
        #     db = root.drawingboard
        #     cir = circuit.renderable_components(txt)
        #     cir.pos = self.pos
        #     x = cir.size[0] + 200
        #     y = cir.size[1] + 100
        #     if x < 500:
        #         x = 500
        #     if y < 500:
        #         y = 500
        #     print(x)
        #     cir.size_hint_x = None
        #     cir.size_hint_y = None
        #     cir.size = (x, y)
        #     print("fghj")
        #     print(cir.size)
        #     db.clear_widgets()
        #     db.add_widget(cir)
        #     self.error.text = ""
        # except:
        #     error = "Invalid Expression"
        #     self.error.text = error


# class for the display board
class DrawingBoard(ScrollView):

    def __init__(self, **kwargs):
        super(DrawingBoard, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.size = (Window.width, Window.height)
        self.do_scroll_x: True
        self.do_scroll_y: True

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# class Circuit(Widget):
#
#     def __init__(self, expression, **kwargs):
#         super(Circuit, self).__init__(**kwargs)
#         self.expression = expression
#         self.render_circuit()
#         with self.canvas.before:
#             Color(1, 1, 1, 1)
#             self.rect = Rectangle(size=self.size, pos=self.pos)
#         self.bind(size=self._update_rect, pos=self._update_rect)
#         self.size_hint_x=None
#         self.size_hint_y=None
#         self.size = (100, 100)
#         self.size_hint_min = (0.1, 0.1)
#
#     def _update_rect(self, instance, value):
#         self.rect.pos = instance.pos
#         self.rect.size = instance.size
#
#     def render_circuit(self):
#         exp = self.expression
#         cir = circuit.renderable_components(exp)
#         self.add_widget(cir)


# class for displaying truth table
class TruthTable(GridLayout):

    def __init__(self, expression, **kwargs):
        super(TruthTable, self).__init__(**kwargs)
        self.expression = self.expression(expression)
        self.table = self.table(self.expression)
        self.draw_table(self.table)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.bind(minimum_height=self.setter('height'))
        self.bind(minimum_width=self.setter('width'))
        self.size_hint_x=None
        self.size_hint_y=None

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def expression(self, expression):
        if isinstance(expression, str):
            expression = boolean.parse(expression, False)
        if not isinstance(expression, boolean.Expression):
            raise TypeError(
                "Argument must be str or Expression but it is {}"
                .format(expression.__class__))
        return expression

    def table(self, table):
        if isinstance(table, str):
            table = boolean.parse(table, False)
        if isinstance(table, boolean.Expression):
            table = boolean.truth_table(table)
        else:
            raise TypeError(
                "Argument must be Expression but it is {}"
                .format(table.__class__))
        # Table should not be directly modified
        return tuple(table)

    def no_cols(self, table):
        return len(table[0])

    def draw_table(self, table):
        self.cols = self.no_cols(table)
        for sym in sorted(table[0].keys()):
            self.add_widget(Label(text=str(sym), pos=self.pos, size_hint_y=None, height=40, size_hint_x=None, width=100, font_size=20, color=[0,0,0,1]))
        for dic in table:
            for key in sorted(dic.keys()):
                self.add_widget(Label(text=str(dic[key]), pos=self.pos, size_hint_y=None, height=40, size_hint_x=None, width=100, font_size=20, color=[0, 0, 0, 1]))


# class for the main window
class MainWindow(GridLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 2
        self.title = Title(size_hint_x=None, size_hint_y=None, width=350, height=50)
        self.menu = Menu(size_hint_y=None, height=50)
        self.taskpanel = TaskPanel(size_hint_x=None, width=350)
        self.drawingboard = DrawingBoard()
        self.add_widget(self.title)
        self.add_widget(self.menu)
        self.add_widget(self.taskpanel)
        self.add_widget(self.drawingboard)


# Main app class
class LogicCircuitApp(App):

    def build(self):
        global root
        root = MainWindow()
        return root


# Entering point to the app
if __name__ == '__main__':
    LogicCircuitApp().run()
