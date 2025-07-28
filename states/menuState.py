from states.state import State
import ttkbootstrap as ttk
import const as c
from PIL import Image, ImageTk
import json
class MenuState(State):
    def __init__(self,window, username):
        super().__init__("MenuState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)
        self.username = username
        self.images = {}
        self.load_user_prefs()
        #Buttons
        self.inventoryButton = ttk.Button(self.canvas, text="Inventario", command=lambda:self.setNextState("InventoryState"))
        self.inventoryButton.pack()
        self.orderButton = ttk.Button(self.canvas, text="Ordenes", command=lambda:self.setNextState("SaleState"))
        self.orderButton.pack()
        self.historyButton = ttk.Button(self.canvas, text="Historial", command=lambda:self.setNextState("HistoryState"))
        self.historyButton.pack()
        self.settingsButton = ttk.Button(self.canvas, text="Configuraciones", command=lambda:self.setNextState("SettingState"))
        self.settingsButton.pack()
        self.profilePic = ttk.Label(self.canvas, image=self.images['userIcon'])
        self.profilePic.pack()

        #setting position on canvas

        self.inventoryButton.place(relx=0.5, y=100, anchor="center")
        self.orderButton.place(relx=0.5, y=150, anchor="center")
        self.historyButton.place(relx=0.5, y=200, anchor="center")
        self.settingsButton.place(relx=0.5, y=250, anchor="center")
        self.profilePic.place(relx= 0.9, anchor="ne" , y=100)

        self.canvas.pack()
    def load_user_prefs(self):
        with open('users.json', 'r') as u:
            users = json.load(u)
            pfpPath = users[self.username]['Profile Picture Small']
            theme = users[self.username]['Chosen Theme']
            self.window.style.theme_use(theme)
            self.images['userIcon'] = ImageTk.PhotoImage(Image.open(pfpPath))

