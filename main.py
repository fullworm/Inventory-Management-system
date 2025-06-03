import ttkbootstrap as ttk
from tkinter import Canvas
from ttkbootstrap.constants import *

class App:
    def __init__(self, master):
        self.master = master
        master.title("Canvas Switching App")

        self.canvas1 = Canvas(master, width=400, height=300, bg="lightblue")
        self.canvas1.create_text(200, 150, text="Canvas 1 (Inventory)", font=("Helvetica", 16))

        self.canvas2 = Canvas(master, width=400, height=300, bg="lightgreen")
        self.canvas2.create_text(200, 150, text="Canvas 2 (Map)", font=("Helvetica", 16))

        self.canvas3 = Canvas(master, width=400, height=300, bg="lightcoral")
        self.canvas3.create_text(200, 150, text="Canvas 3 (Stats)", font=("Helvetica", 16))

        self.current_canvas = None
        self.show_canvas(self.canvas1) # Start with Canvas 1

        # Navigation buttons
        button_frame = ttk.Frame(master)
        button_frame.pack(pady=10)

        btn_canvas1 = ttk.Button(button_frame, text="Show Inventory", command=lambda: self.show_canvas(self.canvas1), bootstyle=PRIMARY)
        btn_canvas1.pack(side=LEFT, padx=5)

        btn_canvas2 = ttk.Button(button_frame, text="Show Map", command=lambda: self.show_canvas(self.canvas2), bootstyle=INFO)
        btn_canvas2.pack(side=LEFT, padx=5)

        btn_canvas3 = ttk.Button(button_frame, text="Show Stats", command=lambda: self.show_canvas(self.canvas3), bootstyle=WARNING)
        btn_canvas3.pack(side=LEFT, padx=5)

    def show_canvas(self, canvas_to_show):
        if self.current_canvas:
            self.current_canvas.pack_forget() # Hide the currently visible canvas

        canvas_to_show.pack(fill=BOTH, expand=YES) # Show the new canvas
        self.current_canvas = canvas_to_show

if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    main_app = App(app)
    app.mainloop()