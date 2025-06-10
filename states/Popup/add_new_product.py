from ttkbootstrap.dialogs import QueryDialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

class AddNewProduct(QueryDialog):
    _instance_count = 0
    def __init__(self, window, name, products):
        super().__init__(parent=window, prompt=name)
        AddNewProduct._instance_count+=1
        self.products = products
        self.show()

    def create_body(self, master):
        self._toplevel.resizable(False, False)
        self._toplevel.protocol("WM_DELETE_WINDOW", self.on_cancel)
        master.configure(width=500, height=500)

        master.pack_propagate(False)  # Prevent the frame from shrinking

        ttk.Label(master, text="Nombre de Producto").pack(fill="x", pady=5)
        self.name_entry = ttk.Entry(master)
        self.name_entry.pack(fill="x", pady=5)

        ttk.Label(master, text="Precio").pack(fill="x", pady=5)
        self.price_entry = ttk.Entry(master)
        self.price_entry.pack(fill="x", pady=5)

        ttk.Label(master, text="Cantidad").pack(fill="x", pady=5)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.pack(fill="x", pady=5)


        ttk.Label(master, text="Tipo").pack(fill="x", pady=5)
        self.type_entry = ttk.Entry(master)
        self.type_entry.pack(fill="x", pady=5)


    def create_buttonbox(self, master):
        frame = ttk.Frame(master)
        frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(frame, text="Ok", command=self.on_submit).pack(side="right", padx=5)


        ttk.Button(frame, text="Cancelar", command=self.on_cancel).pack(side="right", padx=5)

        frame.place(relx=0.5, rely=0.8, anchor="center")

    def on_submit(self, *_):
        try:
            if self.name_entry.get() == "":
                raise ValueError("Por favor entre un nombre valido")
            elif self.name_entry.get() in self.products:
                raise ValueError("Producto ya existe")
            elif self.quantity_entry.get() == "":
                raise ValueError("Por favor entre un precio valido")
            elif self.type_entry.get() == "":
                raise ValueError("Por favor entre un tipo valido")

            self._result = {
                "name": str(self.name_entry.get()),
                "quantity": int(self.quantity_entry.get()),
                "price": float(self.price_entry.get()),
                "type": str(self.type_entry.get())
            }
            AddNewProduct._instance_count -=1
            self._toplevel.destroy()
            self.apply()
        except ValueError as e:
            Messagebox.show_error(title="Error", message=str(e))
    def on_cancel(self):
        AddNewProduct._instance_count-=1
        self._toplevel.destroy()

    @classmethod
    def get_count(cls):
        return cls._instance_count
