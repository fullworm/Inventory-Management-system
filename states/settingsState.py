from states.state import State
import json
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryDialog
import os
from states.Popup.crop_image import CropImage
from tkinter import Toplevel, Button
from PIL import Image, ImageTk
from database.database_func import get_db_connection 
from database.users import hash_password
from bcrypt import checkpw
class SettingState(State):
     def __init__(self, window, username):
        super().__init__('SettingState', None)

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as f:
                 json.dump({},f)
                 f.close()

        self.window = window
        self.canvas = ttk.Canvas(self.window)
        self.images = {}
        self.username = username
        self.set_user_prefs()
        self.userIcon = ttk.Label(self.canvas, image=self.images['userIcon'])
        self.changeUserIcon = ttk.Button(self.canvas, text='chang', command=lambda:self.changePfp())

        self.pfpPath= ''
        self.MenuPfpPath = ''
        self.themes = []
        self.themeMenu = ttk.Combobox(self.canvas, text='...', values=self.themes)

        self.changeName = ttk.Entry(self.canvas)
        self.changePassword = ttk.Entry(self.canvas)

        self.backButton = ttk.Button(self.canvas, text='Regresar', command=lambda:self.setNextState('MenuState'))
        self.applyButton = ttk.Button(self.canvas, text='Aplicar cambios', command=lambda:self.apply_changes())

        self.userIcon.place(relx=0.5, rely=0.15, anchor='center')
        self.changeUserIcon.place(relx=0.7, rely=0.15)
        self.themeMenu.place(relx=0.05, rely=0.2)
        self.applyButton.place(relx=0.05, rely=0.4)

        self.backButton.place(x=10, y=10, anchor='nw')

        self.changeName.place(rely=0.3, relx=0.05)
        self.changePassword.place(rely=0.3, relx=0.2)

        self.canvas.pack(fill='both', expand=True)

     def changePfp(self):
        toplevel = Toplevel(self.window)
        crop = CropImage(toplevel, self.username)

     def apply_changes(self):
        q = QueryDialog(parent =self.window,prompt='Enter Password',title='Confirm Password', datatype=str)
        q.show()
        result = str(q.result)
        with get_db_connection() as db:
            cursor = db.cursor()
            curPass = cursor.execute('SELECT password FROM USERS WHERE name = ?', (self.username,)).fetchone()[0]
            if checkpw(result.encode('utf-8'), curPass):
                if self.changePassword.get() != '':
                    cursor.execute('UPDATE password FROM USERS WHERE name = ?', (hash_password(self.changePassword.get()),self.username,))
                if self.changeName.get() != '':
                    cursor.execute('UPDATE name = ? FROM USERS WHERE name = ?', (self.changeName.get(), self.username,))
                with open('users.json', 'w+') as u:
                    users = json.load(u)
                    if self.pfpPath and self.MenuPfpPath:
                        users[self.username]['Profile Picture'] = self.pfpPath
                        users[self.username]['Profile Picture Menu'] = self.MenuPfpPath
                        self.userIcon.configure(image=self.pfpPath)
                    if self.themeMenu.get() != '':
                        users[self.username]['Chosen Theme'] = self.themeMenu.get()
                        self.window.style.theme_use(self.themeMenu.get())
                    json.dump(users, u)
                    u.close()
                self.set_user_prefs()

     def set_user_prefs(self):
        with open('users.json', 'r') as u:
            users = json.load(u)
            pfpPath = users[self.username]['Profile Picture']
            theme = users[self.username]['Chosen Theme']
            self.window.style.theme_use(theme)
            self.images['userIcon'] = ImageTk.PhotoImage(Image.open(pfpPath))

