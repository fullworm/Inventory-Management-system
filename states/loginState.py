from states.state import State
import ttkbootstrap as ttk
from states import constants as c
from database import users as u
from tkinter import messagebox

class loginState(State):
    def __init__(self, window):
        super().__init__("LoginState", None) #calling parent state class
        self.username = ""
        self.password = ""
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)

        #buttons and entries
        self.usernameEntry = ttk.Entry(self.canvas)
        self.usernameLabel = ttk.Label(self.canvas, text="Username")
        self.usernameEntry.pack()
        self.usernameEntry.focus()

        self.validate_cmd = self.window.register(u.validate_password)
        self.passwordEntry = ttk.Entry(
            self.canvas,
            show="*",
            validate='key',
            validatecommand=(self.validate_cmd, '%P')
        )

        # show="*" for password masking
        self.passwordLabel = ttk.Label(self.canvas, text="Password")
        self.passwordEntry.pack()

        self.loginButton = ttk.Button(self.canvas, text="Login", command=self.handle_login)
        self.loginButton.pack()

        self.window.bind("<Return>", lambda event: self.handle_login())

        #setting position on canvas
        self.usernameLabel.place(relx=0.5, y=60, anchor="center")
        self.usernameEntry.place(relx=0.5, y=100, anchor="center")
        self.passwordLabel.place(relx=0.5, y=150, anchor="center")
        self.passwordEntry.place(relx=0.5, y=190, anchor="center")
        self.loginButton.place(relx=0.5, y=250, anchor="center")

        self.canvas.pack()



    def handle_login(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if not username or not password:  # Check for empty fields
            messagebox.showerror("Error", "Please fill in all fields")
            return
        try:
            if u.user_login(username, password):
                self.next_state = "MenuState"
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.passwordEntry.delete(0, 'end')  # Clear password field

        except Exception as e:
            messagebox.showerror("Error", "Login failed. Please try again.")
            print(f"Login error: {str(e)}")  # For debugging



