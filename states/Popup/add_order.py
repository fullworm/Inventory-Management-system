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
        master.configure(width=605, height=750)
        master.pack_propagate(False)

        # Create left frame for main content
        left_frame = ttk.Frame(master)
        left_frame.pack(side='left', fill='y', expand=True, padx=10)

        # Create right frame for meter
        right_frame = ttk.Frame(master)
        right_frame.pack(side='right', fill='y', padx=10)

        # Add widgets to left frame
        ttk.Label(left_frame, text="Nombre de Orden").pack(fill="x", pady=5)
        self.nameEntry = ttk.Entry(left_frame, width=25)
        self.nameEntry.pack(pady=5, anchor='nw')

        ttk.Label(left_frame, text="Escoge Producto").pack(fill="x", pady=5)
        self.prodMenu = ttk.Combobox(left_frame, text="...", width=25, values=self.products)
        self.prodMenu.pack(pady=5, anchor='nw')

        ttk.Label(left_frame, text="Cantidad de Producto").pack(fill="x", pady=5)
        self.quantityEntry = ttk.Entry(left_frame, width=25)
        self.quantityEntry.pack(pady=5, anchor='nw')
        
        ttk.Label(left_frame, text='Escoge fecha').pack(fill="x", pady=5)
        self.dateEntry = ttk.DateEntry(left_frame, bootstyle="success", dateformat="%m-%d-%Y") #month/day/year
        self.dateEntry['width'] = 25
        self.dateEntry.pack(pady=5, anchor='nw')

        ttk.Label(left_frame, text="Productos en la orden").pack(fill="x", pady=5)
        self.saleProducts = Tableview(left_frame, coldata=self.coldata, rowdata=self.rowdata)
        self.saleProducts.pack(pady=5, expand=True, fill='both')

        # Add meter to right frame
        self.priceMeter = ttk.Meter(
            right_frame,
            subtext='Precio total',
            textright='$',
            amounttotal=self.getTprice(),
            amountused=0,
            stripethickness=2,
            metertype='semi',
            subtextstyle='success',
            metersize=180,
            padding=20,
            amountformat='{:.2f}'
        )
        self.priceMeter.pack(anchor='center')

        right_frame.place(relx=0.6, rely=0.15)
        left_frame.place(relx=0)

        self._toplevel.update_idletasks()
        self._toplevel.place_window_center()

    def create_buttonbox(self, master):
        frame = ttk.Frame(master)
        frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(frame, text="Add", command=lambda:self.add_prod()).pack(side="left", padx=5, pady=5)

        ttk.Button(frame, text="Completar Orden", command=lambda:self.on_submit()).pack(side="left", padx=5, pady=5)

        ttk.Button(frame, text="Cancelar Orden", command=lambda:self.on_cancel()).pack(side="left", padx=5, pady=5)

        frame.place(relx=0.2, rely= 0.9)
        
    def on_submit(self, *_):
        AddOrder._instance_count -= 1
        try:
            name =self.nameEntry.get()
            if not name:
                raise ValueError("Nombre vacio de orden!")
            if not self.rowdata:
                raise ValueError("Orden vacia!")
            self._result = {
                "Order_name": self.nameEntry.get(),   
                "data": self.rowdata,
                "date": self.dateEntry.entry.get(),
                "prod": self.prodData,
                "total": self.priceMeter.amountuseddisplayvar.get()
            }

            self._toplevel.destroy()
            self.apply()
        except ValueError as e:
            Messagebox.show_error(self.master, message=e, title='Error!')

        
    def on_cancel(self, *_):
        AddOrder._instance_count -= 1
        self._toplevel.destroy()
    

    def add_prod(self):
        try:
            name = self.prodMenu.get()
            try:
                quantity = int(self.quantityEntry.get()) or 0
            except ValueError:
                raise ValueError("Porfavor entre una cantidad numerica valida.")
            price = self.prodData[name][1]

            if not name:
                raise ValueError("Porfavor escoja un producto.")
            if name not in self.products:
                raise ValueError("Producto escogido no existe.")
            if not quantity or quantity < 0:
                raise ValueError("Porfavor entre una cantidad valida de producto.")
            if quantity > self.prodData[name][0]:
                raise ValueError(f"Cantidad escogida de producto es mayor que del inventario.\nCantidad actual disponible: {self.prodData[name][0]}")
            

            self.prodData[name][0] -= quantity

            self.rowdata.append([name, quantity, price*float(quantity)])

            self.saleProducts.build_table_data(self.coldata, self.rowdata)
            tVal = sum([row[2] for row in self.rowdata])
            
            self.priceMeter.configure(amountused=tVal)
        except ValueError as e:
            Messagebox.show_error(parent=self.master, title="Error!", message=f'{e}')
    def getTprice(self):
        sum = 0
        for key in self.prodData.keys():
            sum += self.prodData[key][0] * self.prodData[key][1] # amount * price
        return sum

        

    @classmethod
    def get_count(cls):
        return cls._instance_count
    
