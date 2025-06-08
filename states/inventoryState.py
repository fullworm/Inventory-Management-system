from states.state import State
from states import constants as c
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from states.Popup import product_modification_popup as adp

class InventoryState(State):
    def __init__(self, window):
        super().__init__("InventoryState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)
        self.colors = self.window.style.colors

        #test data
        self.coldata = [
            {"text": "Nombre de Producto", "stretch":True},
            {"text": "Cantidad", "stretch":True},
            {"text": "Precio", "stretch":True},
            {"text": "Tipo", "stretch":True}
        ]
        self.rowdata = [
            ["pan", 10, 100, "food"],
            ["potato", 20, 200, "food"],
            ["tomato", 30, 300, "food"],
            ["sandwich", 69, 420, "food"]
        ]

        #displays the inventory in a table
        self.table_frame = ttk.Frame(self.canvas)
        self.table_frame.place(relx=0.5, rely=0.6, relwidth=0.9, anchor="center")
        self.InventoryTable = Tableview(
            self.table_frame,
            paginated=True,
            searchable=True,
            coldata=self.coldata,
            rowdata=self.rowdata,
            yscrollbar=True,
            stripecolor=(self.colors.active, None),
            height=20
        )
        self.InventoryTable.pack(fill="x", expand=True)

        self.addButton = ttk.Button(self.canvas, text="Agregar/Aumentar Producto", command=lambda:self.modify_inventory(True, "Agregar Producto"))
        self.addButton.pack()

        self.removeButton = ttk.Button(self.canvas, text="Quitar/Disminuir producto", command=lambda:self.modify_inventory(False, "Remover Producto"))
        self.removeButton.pack()


        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
        self.backButton.pack()


        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.addButton.place(relx=0.05,rely=0.2, anchor="nw")
        self.removeButton.place(relx=0.2, rely=0.2, anchor="nw")

        self.canvas.pack(fill='both', expand=YES)

    def modify_inventory(self, add:bool, title):

        if adp.ModifyProductPopup.get_count() > 0:
            return

        existing_products = [row[0] for row in self.rowdata]

        popup = adp.ModifyProductPopup(self.canvas, products=existing_products, name=title)

        if popup.result is None:
            return

        product = popup.result["product"]
        quantity = popup.result["quantity"]

        # Update product table
        for p in self.rowdata:
            if p[0] == product:
                if add:
                    p[1] += quantity
                else:
                    if p[1] < quantity:
                        p[1] = 0
                    else:
                        p[1] -= quantity
        self.InventoryTable.build_table_data(
            self.coldata, self.rowdata
        )


        return






