from states.state import State
from database import database_func as db
from states import constants as c
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

class InventoryState(State):
    def __init__(self, window):
        super().__init__("InventoryState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)
        self.colors = self.window.style.colors

        #test data
        coldata = [
            {"text": "Nombre de Producto", "stretch":True},
            {"text": "Cantidad", "stretch":True},
            {"text": "Precio", "stretch":True},
            {"text": "Tipo", "stretch":True},
        ]
        rowdata = [
            ("pan", "10", "100", "food"),
            ("potato", "20", "200", "food"),
            ("tomato", "30", "300", "food"),
            ("sandwich", "69", "420", "food")
        ]

        #displays the inventory in a table
        self.table_frame = ttk.Frame(self.canvas)
        self.table_frame.place(relx=0.5, rely=0.6, relwidth=0.9, anchor="center")
        self.InventoryTable = Tableview(
            self.table_frame,
            paginated=True,
            searchable=True,
            coldata=coldata,
            rowdata=rowdata,
            yscrollbar=True,
            stripecolor=(self.colors.active, None),
            height=20
        )
        self.InventoryTable.pack(fill="x", expand=True)

        self.addButton = ttk.Button(self.canvas, text="Agregar/Aumentar Producto", command=lambda:self.add_popup())
        self.addButton.pack()

        self.removeButton = ttk.Button(self.canvas, text="Quitar/Disminuir producto", command=lambda:self.take_popup())
        self.removeButton.pack()


        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
        self.backButton.pack()


        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.addButton.place(relx=0.05,rely=0.2, anchor="nw")
        self.removeButton.place(relx=0.2, rely=0.2, anchor="nw")

        self.canvas.pack(fill='both', expand=YES)