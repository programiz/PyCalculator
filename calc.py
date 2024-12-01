import tkinter as tk
from tkinter import ttk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

# Constantes pour les textes des boutons
CLEAR_BUTTON_TEXT = "C"
SQUARE_BUTTON_TEXT = "x\u00b2"
SQRT_BUTTON_TEXT = "\u221ax"
EQUALS_BUTTON_TEXT = "="

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")

        self.total_expression = ""
        self.current_expression = ""

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        self.create_display()
        self.create_buttons()

    def create_display(self):
        self.display_frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        self.display_frame.pack(expand=True, fill="both")

        self.total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        self.total_label.pack(expand=True, fill='both')

        self.label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        self.label.pack(expand=True, fill='both')

    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(expand=True, fill="both")

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    def create_button(self, frame, text, bg, fg, font, command, row, column, columnspan=1, sticky="nsew"):
        button = ttk.Button(frame, text=text, command=command)
        self.style.configure(f"TButton", background=bg, foreground=fg, font=font)
        button.grid(row=row, column=column, columnspan=columnspan, sticky=sticky)
        return button

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            self.create_button(self.buttons_frame, str(digit), WHITE, LABEL_COLOR, DIGITS_FONT_STYLE,
                               lambda x=digit: self.add_to_expression(x), grid_value[0], grid_value[1])

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            self.create_button(self.buttons_frame, symbol, OFF_WHITE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                               lambda x=operator: self.append_operator(x), i, 4)
            i += 1

    def create_special_buttons(self):
        self.create_button(self.buttons_frame, CLEAR_BUTTON_TEXT, OFF_WHITE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                           self.clear, 0, 1)
        self.create_button(self.buttons_frame, EQUALS_BUTTON_TEXT, LIGHT_BLUE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                           self.evaluate, 4, 3, columnspan=2)
        self.create_button(self.buttons_frame, SQUARE_BUTTON_TEXT, OFF_WHITE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                           self.square, 0, 2)
        self.create_button(self.buttons_frame, SQRT_BUTTON_TEXT, OFF_WHITE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                           self.sqrt, 0, 3)
        self.create_button(self.buttons_frame, "⌫", OFF_WHITE, LABEL_COLOR, DEFAULT_FONT_STYLE,
                           self.backspace, 4, 1)  # Ajout du bouton Backspace

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.backspace())  # Bind pour backspace
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        if self.current_expression:  # Empêche d'ajouter un opérateur si current_expression est vide
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def backspace(self):  # Fonction pour effacer le dernier caractère
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def square(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**2"))
        except (SyntaxError, TypeError, ValueError):
            self.current_expression = "Error"
        finally:
            self.update_label()

    def sqrt(self):
        try:
            value = eval(self.current_expression)
            if value >= 0:
                self.current_expression = str(value**0.5)
            else:
                self.current_expression = "Error: Racine carrée de nombre négatif"
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
            self.current_expression = f"Error: {e}"
        finally:
            self.update_label()

    def evaluate(self):
        if self.current_expression:  # Permet d'effectuer un calcul avec seulement current_expression
            self.total_expression += self.current_expression
        if self.total_expression:  # Vérifie si total_expression n'est pas vide avant d'évaluer
            self.update_total_label()
            try:
                self.current_expression = str(eval(self.total_expression))
                self.total_expression = ""
            except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
                self.current_expression = f"Error: {e}"
            finally:
                self.update_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
