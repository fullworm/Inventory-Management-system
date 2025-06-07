import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog

class AddProductPopup(QueryDialog):
    def __init__(self, window, name="Add Product", **kwargs):
        super().__init__(window, name, kwargs)

        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="x", padx=20, pady=10)


        self.menuSelect = ttk.Menubutton(self.frame, text="Select Product")
        self.menuSelect.pack(fill="x", pady=5)

        ttk.Label(self.frame, text="Quantity:").pack(fill="x", pady=5)
        self.quantity_entry = ttk.Entry(self.frame)
        self.quantity_entry.pack(fill="x", pady=5)

        self.confirmButton = ttk.Button(self.frame, text="Confirm", command=lambda:self.getValues)
        self.denyButton = ttk.Button(self.frame, text="Cancel", command=lambda:self.destroy)

        self.frame.pack()


    def getValues(self):
        self.frame.destroy()
        return {
            "product": self.menuSelect.cget("text"),
            "quantity": self.quantity_entry.get()
        }
