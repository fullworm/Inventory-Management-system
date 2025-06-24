import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog    
from ttkbootstrap.dialogs import Messagebox

class removeDb(QueryDialog):
    _instance_count = 0
    def __init__(self, window, title, products):
        removeDb._instance_count += 1
        super().__init__(parent=window, prompt=title)
        self.products = products
        self.show()
    def create_body(self, master):
        self._toplevel.resizable(False, False)
        self._toplevel.protocol("WM_DELETE_WINDOW", self.on_cancel)
        master.configure(width=300, height=200)
        master.pack_propagate(False)

        ttk.Label(master, text='Producto para eliminar:').pack(fill="x", pady=5)
        self.prodSelect = ttk.Combobox(master, values=self.products)
        self.prodSelect.pack(fill='x', pady=5)

    def create_buttonbox(self, master):
        frame = ttk.Frame(master)

        ttk.Button(frame, text='Ok', command=lambda:self.on_submit()).pack(side='left',pady=10, padx=10)  

        ttk.Button(frame, text='Cancelar', command=lambda:self.on_cancel()).pack(side='left', pady=10)

        frame.place(relx=0.5, rely=0.9, anchor='center')
    
    def on_submit(self, *_):
        try:
            prod = self.prodSelect.get()

            if not prod:
                raise ValueError('Escoge un producto.')
            if prod not in self.products:
                raise ValueError('Escoge un producto valido.')
            
            self._result = prod

            removeDb._instance_count -= 1
            self._toplevel.destroy()
            self.apply()

        except ValueError as e:
            Messagebox.show_error(parent=self.master, title='Error!', message=e)

    def on_cancel(self, *_):
        removeDb._instance_count -= 1
        self._toplevel.destroy()

    @classmethod
    def get_count(cls):
        return cls._instance_count    