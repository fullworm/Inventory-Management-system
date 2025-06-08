import ttkbootstrap as ttk

from ttkbootstrap.dialogs import QueryDialog

window = ttk.Window()

dialog = QueryDialog(window,"Add Product")

window.mainloop()