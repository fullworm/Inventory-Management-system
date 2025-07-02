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

        self.current_canvas = ""
        self.show_canvas("LoginState")


    def show_canvas(self, state_name):
        # Hide current state if exists
        if self.current_canvas:
            self.current_canvas.canvas.pack_forget()
        if state_name == "LoginState":
            self.current_canvas = loginState.loginState(self.master)
        elif state_name == "MenuState":
            self.current_canvas = menuState.MenuState(self.master)
        elif state_name == "InventoryState":
            self.current_canvas = inventoryState.InventoryState(self.master)
        elif state_name == "SaleState":
            self.current_canvas = saleState.SaleState(self.master)

        self.current_canvas.canvas.pack(fill=BOTH, expand=YES)
        
        self.check_state_transition()

    def check_state_transition(self):
        if self.current_canvas:
            next_state = self.current_canvas.getNextState()
            self.current_canvas.setNextState(None)
            if next_state:
                self.show_canvas(next_state)
        self.master.after(100, self.check_state_transition)


if __name__ == "__main__":
    if not os.path.exists(db.DATABASE_PATH):
        db.setup_database()

    app = ttk.Window(themename="solar")
    app.geometry("1920x1080")
    main_app = App(app)
    app.mainloop()