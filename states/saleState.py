from states.state import State
import ttkbootstrap as ttk
import const as c
from ttkbootstrap.constants import *
from database.database_func import get_db_connection
from states.Popup import add_order as ao
from copy import deepcopy


class SaleState(State):
    def __init__(self, window):
        super().__init__("SaleState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT,)
        self.colors = self.window.style.colors

        self.idN = 0

        self.context_menu = ttk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Edit")
        self.context_menu.add_command(label="Delete", command=lambda: self.remove_order())
        
        self.pendingOrders = ttk.Treeview(self.canvas, columns=("Nombre de orden","Producto", "Cantidad", "Precio", "Fecha de entrega"), show="headings")
        self.pendingOrders.heading("Nombre de orden", text="Nombre de orden")
        self.pendingOrders.heading("Producto", text="Producto")
        self.pendingOrders.heading("Cantidad", text="Cantidad")
        self.pendingOrders.heading("Precio", text="Precio")
        self.pendingOrders.heading('Fecha de entrega', text='Fecha de entrega')
        for col in self.pendingOrders["columns"]:
            self.pendingOrders.column(col, anchor="center")
            self.pendingOrders.heading(col, anchor="center")

        self.pendingOrders.tag_configure('oddrow', background=self.colors.active)
        self.pendingOrders.tag_configure('evenrow', background=self.colors.dark)
        
        self.pendingOrders.place(relx=0.5, rely=0.6, anchor="center")

        self.prodData = self.load_prod()

        self.orderButton = ttk.Button(self.canvas, text="Hacer Orden", command=lambda:self.add_order())
        self.orderButton.pack()

        # self.cancelButton = ttk.Button(self.canvas, text="Cancelar Orden")
        # self.cancelButton.pack()

        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
        self.backButton.pack()

        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.orderButton.place(relx=0.05,rely=0.2, anchor="nw")
        # self.cancelButton.place(relx=0.2, rely=0.2, anchor="nw")

        self.pendingOrders.bind('<Button-3>', self.on_right_click)
        

        self.canvas.pack(fill='both', expand=YES)

    def add_order(self):
        if ao.AddOrder.get_count() > 0:
            return
        popup = ao.AddOrder(self.window, "Agregar Orden", list(self.prodData.keys()), deepcopy(self.prodData))
        result = popup.result
        tag = 'evenrow' if self.idN % 2 == 0 else 'oddrow'
        self.prodData = result['prod']
        self.pendingOrders.insert('', 'end', values=(
            result['Order_name'], 
            '        ', 
            '        ', 
            result['total'], 
            result['date']
            ), 
            iid=self.idN,
            tags=(tag,)
        )
        for i, row in enumerate(result['data']):
            child_tag = 'evenrow' if (self.idN + i + 1) % 2 == 0 else 'oddrow'
            self.pendingOrders.insert(f'{self.idN}', 'end', values=('', row[0], row[1], row[2]), tags=(child_tag,))
        self.idN += 1

    def on_right_click(self, event):
        # Identify the row under the cursor
        item = self.pendingOrders.identify_row(event.y)
        print(item)
        if item:
            self.pendingOrders.selection_set(item)
            # Show context menu
            self.context_menu.tk_popup(event.x_root, event.y_root)
            

    def remove_order(self):
        item = self.pendingOrders.selection()
        if item:
            order_id = item[0]
            
            # add stock to products on canceled order
            for id in self.pendingOrders.get_children(f'{order_id}'):
                prod = self.pendingOrders.item(id, 'values')
                quantity = int(prod[2])
                self.prodData[prod[1]][0] += quantity
            self.pendingOrders.delete(order_id)

            
        
    @staticmethod
    def load_pending_orders():
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
    
    def update_orders(self):
        ...

        


