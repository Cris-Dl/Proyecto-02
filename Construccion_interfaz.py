import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root=root
        self.root.title("TIENDITA SIN NOMBRE")
        self.root.geometry("900x500")
        self.root.configure(bg="#1E90FF")
        self.root.resizable(False, False)
        self.COLOR_FONDO = "#1E90FF"
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_INPUT = "#E6F3FF"
        self.COLOR_BOTON = "#007BFF"


        self.panel_left=tk.Frame(self.root, bg=self.COLOR_FONDO, width=400, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.titulo=tk.Label(self.panel_left, text="TIENDITA SIN NOMBRE", font=("Arial", 18, "bold"), bg=self.COLOR_FONDO, fg="white")
        self.titulo.place(x=50, y=100)

        self.imagen=tk.PhotoImage(file="Logo2.png")
        self.label_logo=tk.Label(self.panel_left, image=self.imagen, bg=self.COLOR_FONDO)
        self.label_logo.place(x=100, y=200)

        self.panel_rigth=tk.Frame(self.root, bg=self.COLOR_BLANCO, width=500, height=500)
        self.panel_rigth.pack(side="right", fill="both", expand=True)

        self.titulo2=tk.Label(self.panel_rigth, text="BIENVENIDO", font=("Arial", 22,"bold"), bg=self.COLOR_BLANCO, fg="#333333")
        self.titulo2.place(x=167, y=60)

        tk.Label(self.panel_rigth, text="USUARIO", font=("Arial", 10), bg=self.COLOR_BLANCO).place(x=150,y=160)
        self.entry_user=tk.Entry(self.panel_rigth, width=30, bg=self.COLOR_INPUT,relief="flat", font=("Arial", 10))
        self.entry_user.place(x=150, y=180 , height=30)

        tk.Label(self.panel_rigth, text="CONTRASEÑA", font=("Arial", 10), bg=self.COLOR_BLANCO).place(x=150, y=220)
        self.entry_password=tk.Entry(self.panel_rigth, show="*", width=30, bg=self.COLOR_INPUT, relief="flat", font=("Arial", 10))
        self.entry_password.place(x=150, y=240, height=30)

        self.boton_login=tk.Button(self.panel_rigth, text="INICIAR SESIÓN", bg=self.COLOR_BOTON, fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25, command=self.login)
        self.boton_login.place(x=150, y=300, height=35)


    def login(self):
        user=self.entry_user.get()
        password=self.entry_password.get()
        if user =="ADMIN" and password=="1234":
            self.root.destroy()
            app2=App()
            app2.mainloop()
        else:
            messagebox.showerror("Error en sus credenciales, inténtelo de nuevo.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tiendita")
        self.geometry("900x600")
        self.resizable(True, True)

        tab_control=ttk.Notebook(self)
        self.tab_productos= ttk.Frame(tab_control)
        self.tab_ventas= ttk.Frame(tab_control)
        self.tab_reportes= ttk.Frame(tab_control)
        tab_control.add(self.tab_productos, text="Agregar productos")
        tab_control.add(self.tab_ventas, text='Ventas')
        tab_control.add(self.tab_reportes, text='Reportes')
        tab_control.pack(expand=1, fill='both')

        self._build_productos_tab()
    def _build_productos_tab(self):
        frame_left= ttk.Frame(self.tab_productos, padding=10)
        frame_left.pack(side="left", fill="y")

        ttk.Label(frame_left, text="Código:").pack(anchor='w')
        self.entry_codigo = ttk.Entry(frame_left)
        self.entry_codigo.pack(fill='x')

        ttk.Label(frame_left, text="Nombre:").pack(anchor='w')
        self.entry_nombre = ttk.Entry(frame_left)
        self.entry_nombre.pack(fill='x')

        ttk.Label(frame_left, text="Existencias:").pack(anchor='w')
        self.entry_existencia = ttk.Entry(frame_left)
        self.entry_existencia.pack(fill='x')

        buton=tk.Button(frame_left, text="Guardar", bg="#2779F5")
        buton.place(x=10, y=130,)

    def ventas(self):
        frame=ttk.Frame(self.tab_ventas, padding=10)
        frame.pack(side="right", fill="y")

        ttk.Label(frame, text="Reporte").pack(anchor='w')



if __name__ == "__main__":
    root=tk.Tk()
    app=Login(root)
    root.mainloop()
