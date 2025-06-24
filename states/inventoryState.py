from states.state import State
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from states.Popup import product_modification as adp
from states.Popup import add_new_product as anp
from states.Popup import remove_prod as rdb
import const as c
from database.database_func import get_db_connection
class InventoryState(State):
    def __init__(self, window):
        super().__init__("InventoryState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT)
        self.colors = self.window.style.colors


        self.coldata = [
            {"text": "Nombre de Producto", "stretch":True},
            {"text": "Cantidad", "stretch":True},
            {"text": "Precio", "stretch":True},
            {"text": "Tipo", "stretch":True}
        ]
        self.rowdata = self.load_products()

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
            height=20,
            autoalign=False,
            pagesize=20
        )
        self.InventoryTable.pack(fill=BOTH, expand=True)

        self.addButton = ttk.Button(self.canvas, text="Agregar/Aumentar Producto", command=lambda:self.modify_inventory(True, "Agregar Producto")) 

        self.removeButton = ttk.Button(self.canvas, text="Quitar/Disminuir producto", command=lambda:self.modify_inventory(False, "Remover Producto"))

        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
    
        self.AddNewButton = ttk.Button(self.canvas, text="Crear Nuevo Producto", command=lambda:self.add_new())

        self.RemoveProdPerm = ttk.Button(self.canvas, text='Borrar producto', command=lambda:self.delete_prod())


        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.addButton.place(relx=0.05,rely=0.2, anchor="nw")
        self.removeButton.place(relx=0.2, rely=0.2, anchor="nw")
        self.AddNewButton.place(relx=0.35, rely=0.2, anchor="nw")
        self.RemoveProdPerm.place(relx=0.5, rely=0.2, anchor='nw')

        self.canvas.pack(fill='both', expand=True)

    def modify_inventory(self, add:bool, title):
        if adp.ModifyProductPopup.get_count() > 0:
            return

        existing_products = [row[0] for row in self.rowdata]

        popup = adp.ModifyProductPopup(self.window, products=existing_products, name=title)

        if popup.result is None:
            return

        product = popup.result["product"]
        quantity = popup.result["quantity"]
        price = popup.result["price"]


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
                if price:
                    p[2] = price

        self.InventoryTable.build_table_data(
            self.coldata, self.rowdata
        )

        self.update_products(self.rowdata)

        return
    
    def add_new(self):
        if anp.AddNewProduct.get_count() > 0:
            return

        existing_products = [row[0] for row in self.rowdata]
        popup = anp.AddNewProduct(self.window,name="Crear Producto Nuevo", products=existing_products)
        result = popup.result

        if popup.result is None:
            return

        self.rowdata.append([result["name"], result["quantity"], result["price"], result["type"]])

        self.InventoryTable.build_table_data(self.coldata, self.rowdata)

        self.update_products(self.rowdata)

        return
    
    def delete_prod(self):
        if rdb.removeDb.get_count() > 0:
            return
        popup = rdb.removeDb(self.window, title='Borrar producto', products=[row[0] for row in self.rowdata])
        result = popup.result

        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute(f'DELETE FROM INVENTORY WHERE product_name = {result}')
            for i in range(len(self.rowdata)):
                if self.rowdata[i][0] == result:
                    self.rowdata.pop(i)
                    self.InventoryTable.build_table_data(self.coldata, self.rowdata)
            db.commit()


    @staticmethod
    def load_products():
        with get_db_connection() as db:
            new = []
            cursor = db.cursor()
            cursor.execute("SELECT * FROM INVENTORY")
            tables = cursor.fetchall()
            for row in tables:
                if row:
                    #price divided by 100 because it was stored as an integer by multiplying by 100
                    new.append([row[1], row[2], float(row[3])/100, row[4]])

            return new
    @staticmethod
    def update_products(rowdata):
        with get_db_connection() as db:
            cursor = db.cursor()
            for p in rowdata:
                name = p[0]
                cursor.execute("SELECT COUNT(*) FROM INVENTORY WHERE product_name = ?", (name,))
                #prices are multiplied by 100 to keep them stored in the db as an integer
                if cursor.fetchone()[0] > 0:
                    cursor.execute("UPDATE INVENTORY SET amount = ?, price = ? WHERE product_name = ?", (p[1], p[2]*100, name))
                else:
                    #product thats been added and doesnt exist in the db yet
                    cursor.execute('INSERT INTO INVENTORY (product_name, amount, price, type)VALUES (?, ?, ?, ?)', (name, p[1], p[2]*100, p[3]))

            db.commit()