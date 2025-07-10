import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from states import loginState
from states import menuState
from states import inventoryState
from states import saleState
import const as c
from database import database_func as db

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Manejador de inventario y ordenes")

        self.states = {
            "LoginState": loginState.loginState(self.master),
            "MenuState": menuState.MenuState(self.master),
            "InventoryState": inventoryState.InventoryState(self.master),
            "SaleState": saleState.SaleState(self.master)
        }
        self.current_canvas = ""
        self.show_canvas("LoginState")

    def show_canvas(self, state_name):
        # Hide current state if exists
        if self.current_canvas:
            self.current_canvas.canvas.pack_forget()

        self.current_canvas = self.states[state_name]
        self.current_canvas.canvas.pack(fill=BOTH, expand=YES)

        # Set up state checking
        self.check_state_transition()

    def check_state_transition(self):
        def check():
            if self.current_canvas:
                next_state = self.current_canvas.getNextState()
                if next_state and next_state in self.states:
                    self.current_canvas.setNextState(None)
                    self.show_canvas(next_state)
            self.master.after(100, check)
        self.master.after(100, check)


if __name__ == "__main__":
    if not os.path.exists(db.DATABASE_PATH):
        db.setup_database()

    app = ttk.Window(themename="solar")
    app.geometry("1920x1080")
    main_app = App(app)
    app.mainloop()