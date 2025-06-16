from states.state import State
import ttkbootstrap as ttk
import const as c
from ttkbootstrap.constants import *
from database.database_func import get_db_connection
from states.Popup import add_order as ao


class SaleState(State):
    def __init__(self, window):
        super().__init__("SaleState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)
        self.colors = self.window.style.colors

        self.pendingOrders = ttk.Treeview(self.canvas, columns=("Nombre de orden","Producto", "Cantidad", "Precio"), show="headings")
        self.pendingOrders.heading("Nombre de orden", text="Nombre de orden")
        self.pendingOrders.heading("Producto", text="Producto")
        self.pendingOrders.heading("Cantidad", text="Cantidad")
        self.pendingOrders.heading("Precio", text="Precio")
        self.pendingOrders.place(relx=0.5, rely=0.6, anchor="center")

        self.pendingOrders.insert("", "end", values=("Birthday Party", "", "", "10000"), iid=0)
        self.pendingOrders.insert("0", "end", values=("", "pan", "100", "100"))

        self.prodData = self.load_prod()
 


        self.orderButton = ttk.Button(self.canvas, text="Hacer Orden", command=lambda:self.add_order())
        self.orderButton.pack()

        self.cancelButton = ttk.Button(self.canvas, text="Cancelar Orden")
        self.cancelButton.pack()

        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
        self.backButton.pack()

        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.orderButton.place(relx=0.05,rely=0.2, anchor="nw")
        self.cancelButton.place(relx=0.2, rely=0.2, anchor="nw")
        

        self.canvas.pack(fill='both', expand=YES)

    
    def load_orders(self):
        ...
    def add_order(self):
        if ao.AddOrder.get_count() > 0:
            return
        popup = ao.AddOrder(self.window, "Agregar Orden", list(self.prodData.keys()), self.prodData)
        result = popup.result

    def remove_order(self):
        ...
    @staticmethod
    def load_prod():
        new = {}
        with get_db_connection() as db:
            cursor = db.cursor()

            cursor.execute("SELECT product_name, amount, price, type FROM INVENTORY")
            data = cursor.fetchall()

            for row in data:
                new[row[0]] = [row[1], float(row[2])/100, row[3]]
        return new
    

        


