import tkinter as tk
import re  # CHANGE: Added re module for handling leading zeros in evaluate method

# CHANGE: Replaced individual font constants with a nested Fonts class for better organization
# CHANGE: Reduced font sizes for better scaling in smaller windows
class Config:
    class Fonts:
        LARGE = ("Arial", 24, "bold")  # Changed from 40 to 24
        SMALL = ("Arial", 12)  # Changed from 16 to 12
        DIGITS = ("Arial", 16, "bold")  # Changed from 24 to 16
        DEFAULT = ("Arial", 14)  # Changed from 20 to 14

    # CHANGE: Replaced individual color constants with nested Light and Dark classes for theme support
    class Colors:
        class Light:
            BG = "#FFFFFF"  # Equivalent to the original WHITE
            FG = "#000000"  # New: Added foreground color
            BUTTON_BG = "#F0F0F0"  # Similar to original OFF_WHITE
            BUTTON_FG = "#000000"  # New: Added button foreground color
            OPERATOR_BG = "#E0E0E0"  # New: Added operator button background
            DISPLAY_BG = "#F5F5F5"  # Equivalent to the original LIGHT_GRAY
            EQUALS_BG = "#90CAF9"  # Similar to original LIGHT_BLUE

        # CHANGE: Added Dark theme colors
        class Dark:
            BG = "#121212"
            FG = "#FFFFFF"
            BUTTON_BG = "#1E1E1E"
            BUTTON_FG = "#FFFFFF"
            OPERATOR_BG = "#2C2C2C"
            DISPLAY_BG = "#1A1A1A"
            EQUALS_BG = "#1976D2"

# CHANGE: Removed individual color constants (OFF_WHITE, WHITE, LIGHT_BLUE, LIGHT_GRAY, LABEL_COLOR)

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        # CHANGE: Reduced minimum size for smaller form factor and made window resizable
        self.window.minsize(200, 300)  # Changed from fixed geometry "375x667"
        self.window.resizable(True, True)  # Changed from (0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        
        # CHANGE: Added theme support
        self.theme = "light"
        self.colors = Config.Colors.Light

        # CHANGE: Renamed method for clarity and to reflect new structure
        self.create_gui()
        self.bind_keys()

    # CHANGE: New method to create GUI elements
    def create_gui(self):
        self.create_display()
        self.create_buttons()
        
        # CHANGE: Added weight configuration for resizable layout
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    # CHANGE: Renamed from create_display_frame and modified for resizable layout
    def create_display(self):
        self.display_frame = tk.Frame(self.window, bg=self.colors.DISPLAY_BG)
        self.display_frame.grid(row=0, column=0, sticky="nsew")  # Changed from pack
        
        # CHANGE: Added weight configuration for resizable layout
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(1, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        # CHANGE: Separated label creation for clarity
        self.create_display_labels()

    # CHANGE: New method for creating display labels
    def create_display_labels(self):
        self.total_label = tk.Label(
            self.display_frame, 
            text=self.total_expression, 
            anchor=tk.E, 
            bg=self.colors.DISPLAY_BG,
            fg=self.colors.FG, 
            padx=5,  # CHANGE: Reduced padding from 24 to 5
            font=Config.Fonts.SMALL
        )
        self.total_label.grid(row=0, column=0, sticky="nsew")  # Changed from pack

        self.label = tk.Label(
            self.display_frame, 
            text=self.current_expression, 
            anchor=tk.E, 
            bg=self.colors.DISPLAY_BG,
            fg=self.colors.FG, 
            padx=5,  # CHANGE: Reduced padding from 24 to 5
            font=Config.Fonts.LARGE
        )
        self.label.grid(row=1, column=0, sticky="nsew")  # Changed from pack

    # CHANGE: Modified to use grid instead of pack and configure for resizable layout
    def create_buttons(self):
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")  # Changed from pack

        # CHANGE: Simplified row and column configuration
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

    # CHANGE: Modified to use updated color scheme and add padding
    def create_digit_buttons(self):
        digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)
        }
        for digit, grid_value in digits.items():
            button = tk.Button(
                self.buttons_frame, 
                text=str(digit), 
                bg=self.colors.BUTTON_BG, 
                fg=self.colors.BUTTON_FG, 
                font=Config.Fonts.DIGITS,
                borderwidth=0, 
                command=lambda x=digit: self.add_to_expression(x)
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky="nsew", padx=1, pady=1)  # CHANGE: Added padding

    # CHANGE: Modified to use updated color scheme, changed layout, and add padding
    def create_operator_buttons(self):
        operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        i = 1
        for operator, symbol in operations.items():
            button = tk.Button(
                self.buttons_frame, 
                text=symbol, 
                bg=self.colors.OPERATOR_BG, 
                fg=self.colors.BUTTON_FG, 
                font=Config.Fonts.DEFAULT,
                borderwidth=0, 
                command=lambda x=operator: self.append_operator(x)
            )
            button.grid(row=i, column=3, sticky="nsew", padx=1, pady=1)  # CHANGE: Changed column to 3 and added padding
            i += 1

    # CHANGE: No significant changes to this method
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_theme_switch_button()  # CHANGE: Added theme switch button

    # CHANGE: Modified to use updated color scheme and layout
    def create_clear_button(self):
        button = tk.Button(
            self.buttons_frame, 
            text="C", 
            bg=self.colors.OPERATOR_BG, 
            fg=self.colors.BUTTON_FG, 
            font=Config.Fonts.DEFAULT,
            borderwidth=0, 
            command=self.clear
        )
        button.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)  # CHANGE: Changed position and added padding

    # CHANGE: Modified to use updated color scheme and layout
    def create_equals_button(self):
        button = tk.Button(
            self.buttons_frame, 
            text="=", 
            bg=self.colors.EQUALS_BG, 
            fg=self.colors.BUTTON_FG, 
            font=Config.Fonts.DEFAULT,
            borderwidth=0, 
            command=self.evaluate
        )
        button.grid(row=4, column=2, columnspan=2, sticky="nsew", padx=1, pady=1)  # CHANGE: Changed position and added padding

    # CHANGE: Modified to use updated color scheme and layout
    def create_square_button(self):
        button = tk.Button(
            self.buttons_frame, 
            text="x\u00b2", 
            bg=self.colors.OPERATOR_BG, 
            fg=self.colors.BUTTON_FG, 
            font=Config.Fonts.DEFAULT,
            borderwidth=0, 
            command=self.square
        )
        button.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)  # CHANGE: Changed position and added padding

    # CHANGE: Modified to use updated color scheme and layout
    def create_sqrt_button(self):
        button = tk.Button(
            self.buttons_frame, 
            text="\u221ax", 
            bg=self.colors.OPERATOR_BG, 
            fg=self.colors.BUTTON_FG, 
            font=Config.Fonts.DEFAULT,
            borderwidth=0, 
            command=self.sqrt
        )
        button.grid(row=0, column=3, sticky="nsew", padx=1, pady=1)  # CHANGE: Changed position and added padding

    # CHANGE: Added new method for theme switch button
    def create_theme_switch_button(self):
        button = tk.Button(
            self.buttons_frame, 
            text="🌓", 
            bg=self.colors.OPERATOR_BG, 
            fg=self.colors.BUTTON_FG, 
            font=Config.Fonts.DEFAULT,
            borderwidth=0, 
            command=self.toggle_theme
        )
        button.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

    # CHANGE: Added new method for toggling theme
    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.colors = Config.Colors.Dark
        else:
            self.theme = "light"
            self.colors = Config.Colors.Light
        self.update_colors()

    # CHANGE: Added new method for updating colors when theme is switched
    def update_colors(self):
        self.window.configure(bg=self.colors.BG)
        self.display_frame.configure(bg=self.colors.DISPLAY_BG)
        self.total_label.configure(bg=self.colors.DISPLAY_BG, fg=self.colors.FG)
        self.label.configure(bg=self.colors.DISPLAY_BG, fg=self.colors.FG)
        
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, tk.Button):
                if widget.cget('text') in ['+', '-', '*', '/', 'C', 'x²', '√x', '🌓']:
                    widget.configure(bg=self.colors.OPERATOR_BG)
                elif widget.cget('text') == '=':
                    widget.configure(bg=self.colors.EQUALS_BG)
                else:
                    widget.configure(bg=self.colors.BUTTON_BG)
                widget.configure(fg=self.colors.BUTTON_FG)

    # CHANGE: Added backspace key binding
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<Escape>", lambda event: self.clear())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        
        for key in '0123456789.+-*/':
            self.window.bind(key, lambda event, digit=key: self.add_to_expression(digit))

    # CHANGE: No significant changes to this method
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    # CHANGE: No significant changes to this method
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # CHANGE: No significant changes to this method
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    # CHANGE: Added new method for backspace functionality
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    # CHANGE: Modified to use try-except for error handling
    def square(self):
        try:
            result = eval(self.current_expression) ** 2
            self.current_expression = str(result)
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    # CHANGE: Modified to use try-except for error handling
    def sqrt(self):
        try:
            result = eval(self.current_expression) ** 0.5
            self.current_expression = str(result)
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    # CHANGE: Modified to handle leading zeros and use try-except for error handling
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            expression = re.sub(r'\b0+(\d+)', r'\1', self.total_expression)  # Remove leading zeros
            self.current_expression = str(eval(expression))
        except Exception:
            self.current_expression = "Error"
        finally:
            self.total_expression = ""
            self.update_label()

    # CHANGE: No significant changes to this method
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in {"/": "÷", "*": "×"}.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    # CHANGE: No significant changes to this method
    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    # CHANGE: No changes to this method
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()