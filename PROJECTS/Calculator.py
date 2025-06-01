import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.bind_keyboard_events()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"350x500+{x}+{y}")
        
    def setup_variables(self):
        """Initialize calculator state variables"""
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.should_reset_display = False
        self.history = ""
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Calculator",
            font=('Segoe UI', 18, 'normal'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        
        # History display
        self.history_label = tk.Label(
            display_frame,
            text="",
            font=('Consolas', 12),
            fg='#888888',
            bg='#1a1a1a',
            anchor='e',
            height=1
        )
        self.history_label.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        # Current display
        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=('Consolas', 24, 'bold'),
            fg='white',
            bg='#1a1a1a',
            anchor='e',
            height=2
        )
        self.display_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for responsive design
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
            
        # Button definitions (text, row, col, colspan, style)
        buttons = [
            ('AC', 0, 0, 1, 'clear'),
            ('CE', 0, 1, 1, 'clear'),
            ('±', 0, 2, 1, 'function'),
            ('÷', 0, 3, 1, 'operator'),
            
            ('7', 1, 0, 1, 'number'),
            ('8', 1, 1, 1, 'number'),
            ('9', 1, 2, 1, 'number'),
            ('×', 1, 3, 1, 'operator'),
            
            ('4', 2, 0, 1, 'number'),
            ('5', 2, 1, 1, 'number'),
            ('6', 2, 2, 1, 'number'),
            ('-', 2, 3, 1, 'operator'),
            
            ('1', 3, 0, 1, 'number'),
            ('2', 3, 1, 1, 'number'),
            ('3', 3, 2, 1, 'number'),
            ('+', 3, 3, 1, 'operator'),
            
            ('0', 4, 0, 2, 'number'),
            ('.', 4, 2, 1, 'number'),
            ('=', 4, 3, 1, 'equals'),
        ]
        
        # Create buttons
        self.buttons = {}
        for text, row, col, colspan, style in buttons:
            btn = self.create_button(buttons_frame, text, style)
            btn.grid(row=row, column=col, columnspan=colspan, 
                    padx=3, pady=3, sticky='nsew')
            self.buttons[text] = btn
            
    def create_button(self, parent, text, style):
        """Create a styled button based on its type"""
        styles = {
            'number': {'bg': '#34495e', 'fg': 'white', 'hover': '#4a6074'},
            'operator': {'bg': '#e74c3c', 'fg': 'white', 'hover': '#c0392b'},
            'equals': {'bg': '#27ae60', 'fg': 'white', 'hover': '#229954'},
            'clear': {'bg': '#f39c12', 'fg': 'white', 'hover': '#e67e22'},
            'function': {'bg': '#9b59b6', 'fg': 'white', 'hover': '#8e44ad'}
        }
        
        style_config = styles.get(style, styles['number'])
        
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 14, 'bold'),
            bg=style_config['bg'],
            fg=style_config['fg'],
            relief=tk.FLAT,
            border=0,
            cursor='hand2',
            command=lambda t=text: self.button_click(t)
        )
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=style_config['hover'])
            
        def on_leave(e):
            btn.configure(bg=style_config['bg'])
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def button_click(self, text):
        """Handle button click events"""
        if text.isdigit():
            self.input_number(text)
        elif text == '.':
            self.input_decimal()
        elif text in ['+', '-', '×', '÷']:
            self.input_operator(text)
        elif text == '=':
            self.calculate()
        elif text == 'AC':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '±':
            self.toggle_sign()
            
    def input_number(self, num):
        """Handle number input"""
        if self.should_reset_display:
            self.current_input = num
            self.should_reset_display = False
        else:
            if self.current_input == "0":
                self.current_input = num
            else:
                self.current_input += num
        self.update_display()
        
    def input_operator(self, op):
        """Handle operator input"""
        if self.previous_input and self.operator and not self.should_reset_display:
            self.calculate()
            
        self.previous_input = self.current_input
        self.operator = op
        self.should_reset_display = True
        self.update_display()
        
    def input_decimal(self):
        """Handle decimal point input"""
        if self.should_reset_display:
            self.current_input = "0."
            self.should_reset_display = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        self.update_display()
        
    def toggle_sign(self):
        """Toggle the sign of current number"""
        if self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
        self.update_display()
        
    def clear_all(self):
        """Clear all calculator state"""
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.should_reset_display = False
        self.history = ""
        self.display_label.configure(fg='white')
        self.update_display()
        
    def clear_entry(self):
        """Clear only current entry"""
        self.current_input = "0"
        self.display_label.configure(fg='white')
        self.update_display()
        
    def calculate(self):
        """Perform calculation"""
        if not self.previous_input or not self.operator:
            return
            
        try:
            prev = float(self.previous_input)
            current = float(self.current_input)
            
            if self.operator == '+':
                result = prev + current
            elif self.operator == '-':
                result = prev - current
            elif self.operator == '×':
                result = prev * current
            elif self.operator == '÷':
                if current == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = prev / current
            else:
                return
                
            # Format result to avoid floating point errors
            result = round(result, 10)
            
            # Handle very large or very small numbers
            if abs(result) > 1e15 or (abs(result) < 1e-10 and result != 0):
                result_str = f"{result:.5e}"
            else:
                # Remove trailing zeros
                if result == int(result):
                    result_str = str(int(result))
                else:
                    result_str = f"{result:g}"
                    
            self.current_input = result_str
            self.previous_input = ""
            self.operator = ""
            self.should_reset_display = True
            self.display_label.configure(fg='white')
            
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            self.current_input = "Error"
            self.display_label.configure(fg='#e74c3c')
            self.previous_input = ""
            self.operator = ""
            self.should_reset_display = True
            
        self.update_display()
        
    def update_display(self):
        """Update the calculator display"""
        # Update current display
        display_text = self.current_input
        if len(display_text) > 15:
            display_text = display_text[:12] + "..."
        self.display_label.configure(text=display_text)
        
        # Update history display
        if self.previous_input and self.operator:
            history_text = f"{self.previous_input} {self.operator}"
            if len(history_text) > 20:
                history_text = history_text[:17] + "..."
            self.history_label.configure(text=history_text)
        else:
            self.history_label.configure(text="")
            
    def bind_keyboard_events(self):
        """Bind keyboard events for calculator input"""
        self.root.bind('<Key>', self.handle_keypress)
        self.root.focus_set()
        
    def handle_keypress(self, event):
        """Handle keyboard input"""
        key = event.char
        keysym = event.keysym
        
        if key.isdigit():
            self.input_number(key)
        elif key == '.':
            self.input_decimal()
        elif key == '+':
            self.input_operator('+')
        elif key == '-':
            self.input_operator('-')
        elif key == '*':
            self.input_operator('×')
        elif key == '/':
            self.input_operator('÷')
        elif key in ['=', '\r']:  # Enter key
            self.calculate()
        elif keysym == 'Escape' or key.lower() == 'c':
            self.clear_all()
        elif keysym == 'BackSpace':
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = "0"
            self.update_display()
            
    def run(self):
        """Start the calculator application"""
        self.root.mainloop()

def main():
    """Main function to run the calculator"""
    try:
        calculator = Calculator()
        calculator.run()
    except Exception as e:
        print(f"Error starting calculator: {e}")

if __name__ == "__main__":
    main()