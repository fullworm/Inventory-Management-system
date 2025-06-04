from states import state
import ttkbootstrap as ttk
from states import constants as c

class loginState(state.State):
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

        self.passwordEntry = ttk.Entry(self.canvas, show="*")  # show="*" for password masking
        self.passwordLabel = ttk.Label(self.canvas, text="Password")
        self.passwordEntry.pack()

        self.loginButton = ttk.Button(self.canvas, text="Login", command=self.handle_login)
        self.loginButton.pack()

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
        print(f"Login attempt - Username: {username}, Password: {password}")
        self.next_state = "MenuState"
