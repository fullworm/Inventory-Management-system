import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog
from ttkbootstrap.dialogs import Messagebox


class ModifyProductPopup(QueryDialog):
    _instance_count = 0
    def __init__(self, window,name, products, **kwargs):
        self.products = products
        ModifyProductPopup._instance_count += 1

        kwargs['title'] = name
        super().__init__(
            parent=window,
            prompt=name,
            **kwargs
        )

        self.show()

    def create_body(self, master):
        # Create product selection


        self._toplevel.resizable(False, False)
        self._toplevel.protocol("WM_DELETE_WINDOW", self.on_cancel)
        master.configure(width=400, height=300)

        master.pack_propagate(False)  # Prevent the frame from shrinking

        ttk.Label(master, text="Select Product:").pack(fill="x", pady=5)
        self.menuSelect = ttk.Menubutton(master, text="Select Product")
        self.menuSelect.pack(fill="both", pady=5)

        # Create menu for the menubutton
        menu = ttk.Menu(self.menuSelect)
        self.menuSelect['menu'] = menu

        # Add products to menu
        for product in self.products:
            menu.add_command(
                label=product,
                command=lambda p=product: self.menuSelect.configure(text=p)
            )

        # Create quantity entry
        ttk.Label(master, text="Quantity:").pack(fill="x", pady=5)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.pack(fill="x", pady=5)

        self._toplevel.update_idletasks()
        self._toplevel.place_window_center()

    def create_buttonbox(self, master):
        box = ttk.Frame(master)
        box.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            master=box,
            text="Confirm",
            command=self.on_submit,
        ).pack(side="right", padx=5)

        ttk.Button(
            master=box,
            text="Cancel",
            command=self.on_cancel,
        ).pack(side="right", padx=5)

        box.place(relx=0.5, rely=0.7, anchor="center")


    def on_submit(self, *_):

        try:
            product = self.menuSelect.cget("text")
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            if product == "Select Product":
                raise ValueError("Please select a product")

            self._result = {
                "product": product,
                "quantity": quantity
            }
            ModifyProductPopup._instance_count -= 1
            self._toplevel.destroy()
            self.apply()
        except ValueError as e:
            Messagebox.show_error(
                title="Error",
                message=str(e)
            )

    def on_cancel(self):
        ModifyProductPopup._instance_count -= 1  # Decrement before destroying
        self._toplevel.destroy()


    @classmethod
    def get_count(cls):
        return cls._instance_count

