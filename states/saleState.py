from states.state import State
import ttkbootstrap as ttk
import const as c
from ttkbootstrap.constants import *
from database.database_func import get_db_connection
from states.Popup import add_order as ao
from copy import deepcopy
import csv
from tkinter.filedialog import asksaveasfilename
import json

class SaleState(State):
    def __init__(self, window):
        super().__init__("SaleState", None)
        self.window = window
        self.canvas = ttk.Canvas(self.window, width=c.WIDTH, height=c.HEIGHT,)
        self.colors = self.window.style.colors

        self.id_orders = 0
        self.id_past = 0

        self.tabs = ttk.Notebook(self.canvas)

        self.orderFrame = ttk.Frame(self.window)
        self.historyFrame = ttk.Frame(self.window)
        
        ### Orders
        self.context_menu = ttk.Menu(self.orderFrame, tearoff=0)
        self.context_menu.add_command(label="Edit", command=lambda:self.edit_order())
        self.context_menu.add_command(label="Delete", command=lambda: self.remove_order())
        self.context_menu.add_command(label='Mark Done', command=lambda: self.mark_done())
        
        self.pendingOrders = ttk.Treeview(self.orderFrame, columns=("Nombre de orden","Producto", "Cantidad", "Precio", "Fecha de entrega"), show="headings")
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
        
        

        self.prodData = self.load_prod()

        self.orderButton = ttk.Button(self.orderFrame, text="Hacer Orden", command=lambda:self.add_order())
        self.orderButton.pack()
        ###

        ### Past Orders
        self.completedOrders = ttk.Treeview(self.historyFrame, columns=("Nombre de orden","Producto", "Cantidad", "Precio", "Fecha de entrega"), show="headings")
        self.completedOrders.heading("Nombre de orden", text="Nombre de orden")
        self.completedOrders.heading("Producto", text="Producto")
        self.completedOrders.heading("Cantidad", text="Cantidad")
        self.completedOrders.heading("Precio", text="Precio")
        self.completedOrders.heading('Fecha de entrega', text='Fecha de entrega')

        for col in self.completedOrders["columns"]:
            self.completedOrders.column(col, anchor="center")
            self.completedOrders.heading(col, anchor="center")

        self.completedOrders.tag_configure('oddrow', background=self.colors.active)
        self.completedOrders.tag_configure('evenrow', background=self.colors.dark)

        self.exportRecords = ttk.Button(self.historyFrame, text='Export Records', command=lambda:self.export_records())
        self.exportRecords.place(relx=0.05, rely=0.2, anchor='nw')

        ###


        self.backButton = ttk.Button(self.canvas, text="Regresar", command=lambda:self.setNextState("MenuState"))
        self.backButton.pack()

        #widget positions
        self.backButton.place(x=10, y=10, anchor="nw")
        self.orderButton.place(relx=0.05,rely=0.2, anchor="nw")
        self.pendingOrders.place(relx=0.5, rely=0.6, anchor="center")
        self.completedOrders.place(relx=0.5, rely=0.6, anchor="center")

        self.tabs.place(rely=0.5, relx=0.5, anchor='center')

        self.orderFrame.configure(width=1200, height=800)
        self.historyFrame.configure(width=1200, height=800)

        self.pendingOrders.bind('<Button-3>', self.on_right_click)
        self.window.protocol("WM_DELETE_WINDOW", lambda: (self.save_pending_orders(), self.window.destroy()))

        self.tabs.add(self.orderFrame, text="Ordenes")
        self.tabs.add(self.historyFrame, text='Historial')

        self.load_order_data(finished=False)
        self.load_order_data(finished=True)
        

        self.canvas.pack(fill='both', expand=YES)

    def add_order(self):
        if ao.AddOrder.get_count() > 0:
            return
        
        popup = ao.AddOrder(self.window, "Agregar Orden", list(self.prodData.keys()), deepcopy(self.prodData))
        result = popup.result

        if not result:
            return
        
        tag = 'evenrow' if self.id_orders % 2 == 0 else 'oddrow' # generating tag so it knows what color to give the row in the table
        self.prodData = result['prod']

        self.pendingOrders.insert('', 'end', values=(
            result['Order_name'], 
            '', 
            '', 
            result['total'], 
            result['date']
            ), 
            iid=self.id_orders,
            tags=(tag,)
        )

        for i, row in enumerate(result['data']):
            child_tag = 'evenrow' if (self.id_orders + i + 1) % 2 == 0 else 'oddrow'
            self.pendingOrders.insert(f'{self.id_orders}', 'end', values=('', row[0], row[1], row[2]), tags=(child_tag,))
        self.id_orders += 1
        self.update_stock()

    # right click menu
    def on_right_click(self, event):
        # Identify the row under the cursor
        item = self.pendingOrders.identify_row(event.y)
        if item:
            self.pendingOrders.selection_set(item)
            # Show context menu
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def remove_order(self):
        item = self.pendingOrders.selection()
        if item:
            order_id = item[0]

            parent_order = self.pendingOrders.item(order_id, 'values')
            
            #if removing unfinished order thats already in db
            with get_db_connection() as db:
                cursor = db.cursor()
                row = cursor.execute('SELECT id FROM ORDERS WHERE name = ?', (parent_order[0],)).fetchone()
                if row:
                    sale_id = row[0]
                    cursor.execute('DELETE FROM ORDERS WHERE id = ?', (sale_id,))
                    cursor.execute('DELETE FROM ORDER_ITEMS WHERE order_id = ?', (sale_id,))
                db.commit()


            
            # add stock to products on canceled order
            for id in self.pendingOrders.get_children(order_id):
                prod = self.pendingOrders.item(id, 'values')
                quantity = int(prod[2])
                self.prodData[prod[1]][0] += quantity
            self.pendingOrders.delete(order_id)
            self.update_stock()

    def edit_order(self):
        item = self.pendingOrders.selection()
        if item:
            with get_db_connection() as db:
                cursor = db.cursor()

                order_id = item[0]

                parent = self.pendingOrders.item(order_id, 'values')
                result = cursor.execute(
                    'SELECT id FROM ORDERS WHERE name = ? AND total_price = ? AND date = ?',
                    (parent[0], float(parent[3]) * 100, parent[4])
                ).fetchone()
                sale_id = result[0] if result else None
                
                child_items = []
                for id in self.pendingOrders.get_children(order_id):
                    child_items.append(list(self.pendingOrders.item(id, 'values'))[1:4])
                
                popup = ao.AddOrder(self.window, "Agregar Orden", list(self.prodData.keys()), deepcopy(self.prodData), editData=child_items, edit=True)
                result = popup.result

                if not result:
                    return
            
                self.prodData = result['prod']

                self.pendingOrders.item(order_id, values=(
                    result['Order_name'], 
                    '', 
                    '', 
                    result['total'], 
                    result['date']
                    )
                )

                # delete existing child items
                for child_id in self.pendingOrders.get_children(order_id):
                    self.pendingOrders.delete(child_id)
                
                # insert new child items
                for i, row in enumerate(result['data']):
                    child_tag = 'evenrow' if (int(order_id) + i + 1) % 2 == 0 else 'oddrow'
                    self.pendingOrders.insert(
                        order_id,
                        'end',
                        values=('', row[0], row[1], row[2]),
                        tags=(child_tag,)
                    )
                
                # edit the db accordingly if it exist already
                if sale_id:
                    parent = self.pendingOrders.item(order_id, 'values')

                    cursor.execute("UPDATE ORDERS SET name = ?, total_price = ?, date = ? WHERE id = ?", (parent[0], float(parent[3])*100, parent[4], sale_id,))
                    cursor.execute("DELETE FROM ORDER_ITEMS WHERE order_id = ?", (sale_id,))
                    
                    for id in self.pendingOrders.get_children(order_id):
                        child = self.pendingOrders.item(id, 'values')
                        cursor.execute('INSERT INTO ORDER_ITEMS (order_id ,product_name, quantity, price) VALUES (?,?,?,?)', (sale_id, child[1], int(child[2]), float(child[3])*100))
                db.commit()

        
        self.update_stock()
    
    def mark_done(self):
        item = self.pendingOrders.selection()
        if item:
            order_id = item[0]

            parent_val = self.pendingOrders.item(order_id, 'values')

            self.completedOrders.insert('', 'end', values=parent_val, iid=self.id_past)

            child_items = []
            for id in self.pendingOrders.get_children(order_id):
                child_items.append(list(self.pendingOrders.item(id, 'values'))[1:4])

            with get_db_connection() as db:
                cursor = db.cursor()
                cursor.execute(
                    '''
                       INSERT INTO ORDERS 
                       (name, finished, total_price, date) 
                       VALUES (?,?,?,?)
                    ''', 
                       (parent_val[0], 1, float(parent_val[3])*100, parent_val[4])
                    )
                sale_id = cursor.lastrowid
                
                for item in child_items:
                    cursor.execute(
                        '''
                        INSERT INTO ORDER_ITEMS 
                        (order_id, product_name, quantity, price) 
                        VALUES (?,?,?,?)
                        ''', 
                        (sale_id, item[0], int(item[1]), float(item[2])*100)
                    )
                    self.completedOrders.insert(self.id_past, 'end', values=('', item[0], item[1], item[2], ''))
                self.pendingOrders.delete(order_id)
                self.id_past += 1
            self.update_stock()
                
        
    def load_order_data(self, finished:bool) -> None:
        with get_db_connection() as db:
            cursor = db.cursor()
            parent_orders = cursor.execute('''SELECT * FROM ORDERS WHERE finished = ?''', (finished,)).fetchall()
            if parent_orders:
                if finished:
                    for parent in parent_orders:
                        order_items = cursor.execute('SELECT product_name, quantity, price FROM ORDER_ITEMS WHERE order_id = ?', (parent[0],)).fetchall()
                        self.pendingOrders.insert('', 'end', values=(parent[1], '', '', parent[3]/100, parent[4]), iid=self.id_orders)
                        for item in order_items:
                            self.pendingOrders.insert(self.id_orders, 'end', values = ('', item[0], item[1], item[2]/100, ''))
                        self.id_orders += 1
                else:
                    for parent in parent_orders:
                        order_items = cursor.execute('SELECT product_name, quantity, price FROM ORDER_ITEMS WHERE order_id = ?', (parent[0],)).fetchall()
                        self.completedOrders.insert('', 'end', values=(parent[1], '','', parent[3], parent[4]), iid=self.id_past)
                        for item in order_items:
                            self.completedOrders.insert(self.id_past, 'end', values=('', item[0], item[1], item[2], ''))
                        self.id_past += 1
    
    def setNextState(self, state):
        self.save_pending_orders()
        self.next_state = state

    def save_pending_orders(self):
        # Put orders that aren't finished in the db
        with get_db_connection() as db:
            cursor = db.cursor()
            parent_ids = self.pendingOrders.get_children('')
            if parent_ids:
                for id in parent_ids:
                    parent_info = self.pendingOrders.item(id, 'values')
                    # Check for existing unfinished order with the same name
                    cursor.execute('''SELECT id FROM ORDERS WHERE name = ? AND finished = 0''', (parent_info[0],))
                    existing_order = cursor.fetchone()
                    if not existing_order:
                        cursor.execute(
                            '''
                                INSERT INTO ORDERS 
                                (name, finished, total_price, date) 
                                VALUES (?,?,?,?)
                            ''', 
                            (parent_info[0], 0, float(parent_info[3])*100, parent_info[4]) #price multiplied by 100 because we/i want to store it as an integer
                        )
                        sale_id = cursor.lastrowid

                        for child in self.pendingOrders.get_children(id):
                            child_info = self.pendingOrders.item(child, 'values')
                            cursor.execute(
                                '''
                                INSERT INTO ORDER_ITEMS 
                                (order_id, product_name, quantity, price) VALUES (?,?,?,?)
                                ''', 
                                (sale_id, child_info[1], int(child_info[2]), float(child_info[3])*100) #price multiplied by 100 because we/i want to store it as an integer
                            )
            db.commit()

        return 

    def update_stock(self):
        with get_db_connection() as db:
            cursor = db.cursor()
            for prod in list(self.prodData.keys()):
                cursor.execute('UPDATE INVENTORY SET amount = ? WHERE product_name = ?', (self.prodData[prod][0], prod))
            db.commit()

    def export_records(self):
        filename = asksaveasfilename(
            defaultextension="csv",
            filetypes=[("CSV files", "*.csv"), ('JSON files', '*.json')],
            initialfile="historial.csv",
            initialdir='/home/adriel'
        )
        if filename:
            if filename.lower().endswith('.csv'):
                csv_data = [
                    #headers
                    ['Order name', 'Order date', 'Total cost', 'Product name','quantity','Price']
                ]
                for id in self.completedOrders.get_children(''):
                    parent = self.completedOrders.item(id, 'values')
                    for c in self.completedOrders.get_children(id):
                        child = self.completedOrders.item(c, 'values')
                        csv_data.append([parent[0], parent[4], parent[3], child[1], child[2], child[3]])
                        with open(filename, 'w', newline='', encoding='utf-8') as f:
                            file = csv.writer(f)
                            file.writerows(csv_data)

            elif filename.lower().endswith('.json'):
                data = {
                    'orders': []
                }
                for id in self.completedOrders.get_children(''):
                    temp = {}
                    parent = self.completedOrders.item(id, 'values')
                    temp['Order name'] = parent[0]
                    temp['Order Date'] = parent[4]
                    temp['Order price'] = float(parent[3])
                    temp['Order items'] = []
                    for c in self.completedOrders.get_children(id):
                        child = self.completedOrders.item(c, 'values')
                        temp['Order items'].append({
                            'Product name': child[1], 
                            'Quantity': int(child[2]), 
                            'Price': child[3]
                        })
                    data['orders'].append(temp)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
            else:
                return
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