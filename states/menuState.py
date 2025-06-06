

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
        self.inventoryButton = ttk.Button(self.canvas, text="Inventario", command=self.setNextState("InventoryState"))
        self.orderButton = ttk.Button(self.canvas, text="Ordenes", command=self.setNextState("OrderState"))
        self.historyButton = ttk.Button(self.canvas, text="Historial", command=self.setNextState("HistoryState"))
        self.settingsButton = ttk.Button(self.canvas, text="Configuraciones", command=self.setNextState("SettingsState"))
        self.profileButton = ttk.Button(self.canvas,bootstyle="success-circle") # supposed to be circle but doesnt work for some reason

        #setting position on canvas

        self.inventoryButton.place(relx=0.5, y=100, anchor="center")
        self.orderButton.place(relx=0.5, y=150, anchor="center")
        self.historyButton.place(relx=0.5, y=200, anchor="center")
        self.settingsButton.place(relx=0.5, y=250, anchor="center")
        self.profileButton.place(relx= 0.8, anchor="ne" , y=100)

        self.canvas.pack()

