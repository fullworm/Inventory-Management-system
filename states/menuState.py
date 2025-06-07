

from states.state import State
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from states import constants as c

class MenuState(State):
    def __init__(self,window):
        super().__init__("MenuState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)

        #Buttons
        self.inventoryButton = ttk.Button(self.canvas, text="Inventario", command=lambda:self.setNextState("InventoryState"))
        self.inventoryButton.pack()
        self.orderButton = ttk.Button(self.canvas, text="Ordenes", command=lambda:self.setNextState("OrderState"))
        self.orderButton.pack()
        self.historyButton = ttk.Button(self.canvas, text="Historial", command=lambda:self.setNextState("HistoryState"))
        self.historyButton.pack()
        self.settingsButton = ttk.Button(self.canvas, text="Configuraciones", command=lambda:self.setNextState("SettingsState"))
        self.settingsButton.pack()
        self.profileButton = ttk.Button(self.canvas, text="Profile Photo",bootstyle="success-circle") # supposed to be circle but doesnt work for some reason
        self.profileButton.pack()

        #setting position on canvas

        self.inventoryButton.place(relx=0.5, y=100, anchor="center")
        self.orderButton.place(relx=0.5, y=150, anchor="center")
        self.historyButton.place(relx=0.5, y=200, anchor="center")
        self.settingsButton.place(relx=0.5, y=250, anchor="center")
        self.profileButton.place(relx= 0.8, anchor="ne" , y=100)

        self.canvas.pack()

