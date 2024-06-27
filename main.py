import tkinter as tk
from tkinter import messagebox
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("400x600")
        self.configure(bg="lightgrey")
        self.resizable(False, False)  # Make the window size fixed

        self.expression = ""
        self.result_var = tk.StringVar(value="0")
        self.new_input = True
        self.just_calculated = False

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Entry widget for display
        self.entry = tk.Entry(self, textvariable=self.result_var, font=('Arial', 20), bd=10, insertwidth=4, width=14, borderwidth=4, state=tk.DISABLED, disabledbackground="white", disabledforeground="black")
        self.entry.grid(row=0, column=0, columnspan=5, pady=20, sticky='nsew')

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('(', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), (')', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('^', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3), ('C', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3), ('exp', 5, 4),
            ('sqrt', 6, 0), ('ln', 6, 1), ('log2', 6, 2), ('!', 6, 3), ('π', 6, 4)
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col)

        # Configure grid to expand properly
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def create_button(self, text, row, col):
        button = tk.Button(self, text=text, padx=20, pady=20, font=('Arial', 18), command=lambda: self.on_button_click(text))
        button.grid(row=row, column=col, sticky='nsew')

    def on_button_click(self, char):
        if char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear_entry()
        elif char in ('sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'log2', '!'):
            self.calculate_function(char)
        elif char == 'π':
            self.result_var.set(str(math.pi))
            self.expression = str(math.pi)
            self.new_input = True
        else:
            if char in '0123456789.':
                if self.new_input or self.just_calculated:
                    self.result_var.set(char)
                    self.new_input = False
                    self.just_calculated = False
                else:
                    self.result_var.set(self.result_var.get() + char)
            else:
                if self.just_calculated:
                    self.expression = self.result_var.get()
                    self.just_calculated = False
                self.new_input = True
            self.expression += str(char)

    def calculate_result(self):
        try:
            expression = self.expression
            expression = expression.replace('sin', 'math.sin(math.radians')
            expression = expression.replace('cos', 'math.cos(math.radians')
            expression = expression.replace('tan', 'math.tan(math.radians')
            expression = expression.replace('log', 'math.log10')
            expression = expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('^', '**')
            expression = expression.replace('exp', 'math.exp')
            expression = expression.replace('ln', 'math.log')
            expression = expression.replace('log2', 'math.log2')
            if '!' in expression:
                expression = expression.replace('!', '')
                self.result_var.set(math.factorial(int(self.expression[:-1])))
            else:
                self.result_var.set(str(eval(expression)))
            self.expression = self.result_var.get()
            self.new_input = True
            self.just_calculated = True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.expression = ""

    def calculate_function(self, func):
        try:
            value = float(self.result_var.get())
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'exp':
                result = math.exp(value)
            elif func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'log2':
                result = math.log2(value)
            elif func == '!':
                result = math.factorial(int(value))
            self.result_var.set(str(result))
            self.expression = str(result)
            self.new_input = True
            self.just_calculated = True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.expression = ""

    def clear_entry(self):
        self.expression = ""
        self.result_var.set("0")
        self.new_input = True
        self.just_calculated = False

    def bind_keys(self):
        for key in '0123456789+-*/.^()':
            self.bind(f'<Key-{key}>', self.key_input)
        self.bind('<Return>', self.key_enter)
        # self.bind('<BackSpace>', self.key_backspace)
        self.bind('<=>', self.key_enter)
        self.bind('<c>', self.key_clear)
        self.bind('<Shift_L>', self.ignore_key)
        self.bind('<Shift_R>', self.ignore_key)

    def key_input(self, event):
        if event.char in '0123456789+-*/.^()':
            if event.char in '0123456789.':
                if self.new_input or self.just_calculated:
                    self.result_var.set(event.char)
                    self.new_input = False
                    self.just_calculated = False
                else:
                    self.result_var.set(self.result_var.get() + event.char)
            else:
                if self.just_calculated:
                    self.expression = self.result_var.get()
                    self.just_calculated = False
                self.new_input = True
            self.expression += event.char

    def key_enter(self, event):
        self.calculate_result()
        return "break"  # Prevent default behavior

    def key_backspace(self, event):
        if len(self.result_var.get()) > 1:
            self.result_var.set(self.result_var.get()[:-1])
        else:
            self.result_var.set("0")
        if len(self.expression) > 1:
            self.expression = self.expression[:-1]
        else:
            self.expression = ""
        self.new_input = False
        self.just_calculated = False

    def key_clear(self, event):
        self.clear_entry()

    def ignore_key(self, event):
        pass

if __name__ == "__main__":
    calculator = ScientificCalculator()
    calculator.mainloop()
