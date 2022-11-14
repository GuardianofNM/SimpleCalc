from decimal import Decimal, Context, setcontext, DecimalException
import tkinter as tk
from tkinter import messagebox, font
from functools import partial
from enum import Flag, auto
import operator
import Tester

class Status(Flag):
    OP = auto()
    DP = auto()
    DIGITS = auto()
    EQ = auto()
class Calculator:
    setcontext(Context(prec = 32))
    ops = {'*': operator.mul, '/':operator.truediv, '+':operator.add, '-':operator.sub}
    def __init__(self):
        self.stack = []
        self.status = ~(Status.OP | Status.DP | Status.DIGITS | Status.EQ)
    def calculation(self, i, pos):
        #print(self.stack)
        try:
            a = Decimal.normalize(Decimal(str(self.ops[self.stack[i]](Decimal(self.stack[i - 1]),Decimal(self.stack[i + 1])))))
            b = a.quantize(Decimal(1)) if a == a.to_integral() else a.normalize()
            self.stack[i - 1] = str(b)
            self.stack[i + 1] = ''
            self.stack[i] = ''
            self.stack.remove('')
            self.stack.remove('')
            for j in range(len(pos)):
                pos[j] -= 2
        except DecimalException:
            self.evaluation('C')
            messagebox.showerror('Error','Inputted value is too large.\nPlease retry.')
    def evaluation(self, buttonpressed):
        def reset(self):
            self.stack = []
            self.status = ~(Status.OP | Status.DP | Status.DIGITS | Status.EQ)
            expression.set('')
            result.set('')
        if buttonpressed == 'C': #RESET
            reset(self)
        elif buttonpressed == '.': #DECIMAL POINT
            if self.status & Status.DIGITS and '.' not in self.stack[-1]:
                self.stack[-1] += buttonpressed
                self.status = Status.DP & ~(Status.OP | Status.DIGITS | Status.EQ)
        elif buttonpressed == 'R': #REVERSE
            if self.status & (Status.DIGITS | Status.DP | Status.EQ):
                self.stack[-1] = str(self.ops['*'](Decimal(self.stack[-1]), -1))
        elif buttonpressed in self.ops: #ADD,SUB,MUL,DIV
            if self.status & (Status.DIGITS | Status.DP | Status.EQ):
                self.stack.append(buttonpressed)
                self.status = Status.OP & ~(Status.DP | Status.DIGITS | Status.EQ)
            elif self.status & Status.OP:
                self.stack[-1] = buttonpressed
                self.status = Status.OP & ~(Status.DP | Status.DIGITS | Status.EQ)
        elif buttonpressed == '=': #EQUALS
            if self.status & Status.OP:
                del self.stack[-1]
            fixedexpression.set(' '.join(self.stack))
            if len(self.stack) > 1:
                MULDIVpos = [i for i, x in enumerate(self.stack) if (x == '*' or x == '/')]
                for i in MULDIVpos:
                    if Decimal(self.stack[i + 1]) == 0 and self.stack[i] == '/':
                        messagebox.showerror('Error','Can\'t divide by 0.\nPlease input correct formula.')
                        reset(self)
                        break
                    self.calculation(i, MULDIVpos)
                ADDSUBpos = [i for i, x in enumerate(self.stack) if (x == '+' or x == '-')]
                for i in ADDSUBpos:
                    self.calculation(i, ADDSUBpos)
            result.set(' '.join(self.stack))
            self.status = self.status | Status.EQ
        elif buttonpressed.isdigit(): #DIGITS
            if self.status & (Status.DIGITS | Status.DP):
                self.stack[-1] += buttonpressed
                self.status = Status.DIGITS & ~(Status.DP | Status.OP | Status.EQ)
            else:
                if self.status & Status.EQ:
                    self.stack = []
                self.stack.append(buttonpressed)
                self.status = Status.DIGITS & ~(Status.DP | Status.OP | Status.EQ)
        #print(self.stack)
        expression.set(' '.join(self.stack))
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Simple Calculator")

    BUTTON_UNIT_WIDTH = 5
    BUTTON_UNIT_HEIGHT = 5
    DEFAULT_FONT = font.Font(size = 15)

    calc = Calculator()

    result = tk.StringVar()
    expression = tk.StringVar()
    resultlabel = tk.Label(root, textvariable = result, font = DEFAULT_FONT)
    resultlabel.grid(row = 1, column = 0, columnspan = 5, sticky=tk.N+tk.S)
    expressionlabel = tk.Label(root, textvariable = expression, font = DEFAULT_FONT)
    expressionlabel.grid(row = 0, column = 0, columnspan = 5, sticky = tk.E)
    buttons = [0] * 18
    fixedexpression = tk.StringVar()

    buttons[0] = tk.Button(root, text = '0', command = lambda : calc.evaluation('0'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT) # BUTTON 0
    buttons[0].grid(row = 6, column = 1)
    for i in range(9): #BUTTON 1 to 9
        buttons[i + 1] = tk.Button(root, text = i + 1, command = partial(calc.evaluation, str(i + 1)), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
        buttons[i + 1].grid(row = int((17 - i) / 3), column = 2 - ((17 - i) % 3))
    buttons[10] = tk.Button(root, text = '+/-', command = lambda : calc.evaluation('R'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[10].grid(row = 6, column = 0)
    buttons[11] = tk.Button(root, text = '+', command = lambda : calc.evaluation('+'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[11].grid(row = 3, column = 3)
    buttons[12] = tk.Button(root, text = '-', command = lambda : calc.evaluation('-'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[12].grid(row = 4, column = 3)
    buttons[13] = tk.Button(root, text = b'\xC3\x97'.decode('utf-8'), command = lambda : calc.evaluation('*'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[13].grid(row = 5, column = 3)
    buttons[14] = tk.Button(root, text = b'\xC3\xB7'.decode('utf-8'), command = lambda : calc.evaluation('/'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[14].grid(row = 6, column = 3)
    buttons[15] = tk.Button(root, text = b'\xE3\x83\xBB'.decode('utf-8'), command = lambda : calc.evaluation('.'), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[15].grid(row = 6, column = 2)
    buttons[16] = tk.Button(root, text = '=', command = lambda : calc.evaluation('='), width = BUTTON_UNIT_WIDTH, height = BUTTON_UNIT_HEIGHT, font = DEFAULT_FONT)
    buttons[16].grid(row = 3, column = 4, rowspan = 4, sticky=tk.N+tk.S)
    buttons[17] = tk.Button(root, text = 'AC', command = lambda : calc.evaluation('C'), width = BUTTON_UNIT_WIDTH, height = int(BUTTON_UNIT_HEIGHT / 3), font = DEFAULT_FONT)
    buttons[17].grid(row = 7, column = 0, columnspan = 5, sticky = tk.W + tk.E)

    #Tester.doTest(buttons, result, fixedexpression)
    root.update()
    root.mainloop()