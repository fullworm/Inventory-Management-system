import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog    
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

class AddOrder(QueryDialog):
    _instance_count = 0
    def __init__(self, window, title, products = [], prodData = {}):
        AddOrder._instance_count += 1
        super().__init__(parent=window, prompt=title)
        self.products = products
        self.prodData = prodData
        self.coldata = [
            {"text": "Nombre de Producto", "stretch":True},
            {"text": "Cantidad", "stretch":True},
            {"text": "Precio", "stretch":True}
        ]
        self.rowdata = []


        self.show()

    


    def create_body(self, master):
        self._toplevel.resizable(False, False)
        self._toplevel.protocol("WM_DELETE_WINDOW", self.on_cancel)
        master.configure(width=600, height=750)

        master.pack_propagate(False)  # Prevent the frame from shrinking

        ttk.Label(master, text="Nombre de Orden").pack(fill="x", pady=5)
        self.nameEntry = ttk.Entry(master)
        self.nameEntry.pack(fill="x",pady=5, anchor='nw')

        ttk.Label(master, text="Escoge Producto").pack(fill="x", pady=5)
        self.prodMenu = ttk.Menubutton(master, text="...", width=15)
        self.prodMenu.pack(fill="x",pady=5, anchor='nw')

        # Create menu for the menubutton
        menu = ttk.Menu(self.prodMenu)
        self.prodMenu['menu'] = menu

        # Add products to menu
        for product in self.products:
            menu.add_command(
                label=product,
                command=lambda p=product: self.prodMenu.configure(text=p)
            )
        ttk.Label(master, text="Cantidad de Producto").pack(fill="x", pady=5)
        self.quantityEntry = ttk.Entry(master)
        self.quantityEntry.pack(fill="x",pady=5, anchor='nw')
        
        ttk.Label(master, text='Escoge fecha').pack(fill="x", pady=5)
        self.dateEntry = ttk.DateEntry(master,bootstyle="success")
        self.dateEntry.pack(fill="x",pady=5, anchor='nw')


        ttk.Label(master, text="Productos en la orden").pack(fill="x", pady=5)
        self.saleProducts = Tableview(master, coldata=self.coldata, rowdata=self.rowdata)
        self.saleProducts.pack(fill="x",pady=5, expand=True, anchor='nw')
        self._toplevel.update_idletasks()
        self._toplevel.place_window_center()

    def create_buttonbox(self, master):
        frame = ttk.Frame(master)
        frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(frame, text="Add", command=lambda:self.add_prod()).pack(side="left", padx=5, pady=5)

        ttk.Button(frame, text="Completar Orden", command=lambda:self.on_submit).pack(side="left", padx=5, pady=5)

        ttk.Button(frame, text="Cancelar Orden", command=lambda:self.on_cancel).pack(side="left", padx=5, pady=5)

        frame.place(relx=0.2, rely= 0.9)
        
    def on_submit(self, *_):
        AddOrder._instance_count -= 1

        self._toplevel.destroy()
    def on_cancel(self, *_):
        AddOrder._instance_count -= 1
        self._toplevel.destroy()
    

    def add_prod(self):
        try:
            name = self.prodMenu.cget("text")
            quantity = float(self.quantityEntry.get())
            price = self.prodData[name][1]
            if not name:
                raise ValueError("Porfavor escoja un producto.")
            if not quantity or quantity < 0 or type(quantity) != int:
                raise ValueError("Porfavor entre una cantidad valida de producto.")
            
            self.rowdata.append([name, quantity, price*quantity])

            self.saleProducts.build_table_data(self.coldata, self.rowdata)
        except ValueError as e:
            Messagebox.show_error(parent=self.master, title="Error", message=f'{e}')

        

    @classmethod
    def get_count(cls):
        return cls._instance_count