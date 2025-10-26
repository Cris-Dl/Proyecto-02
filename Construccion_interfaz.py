import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root=root
        self.root.title("MINIMARKET")
        self.root.geometry("900x500")
        self.root.configure(bg="#1E90FF")
        self.root.resizable(False, False)
        self.COLOR_FONDO = "#1E90FF"
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_INPUT = "#E6F3FF"
        self.COLOR_BOTON = "#007BFF"


        self.panel_left=tk.Frame(self.root, bg=self.COLOR_FONDO, width=400, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.titulo=tk.Label(self.panel_left, text="BIENVENIDO", font=("Arial", 27, "bold"), bg=self.COLOR_FONDO, fg="black")
        self.titulo.place(x=105, y=140)

        self.imagen=tk.PhotoImage(file="1.png")
        self.label_logo=tk.Label(self.panel_left, image=self.imagen, bg=self.COLOR_FONDO)
        self.label_logo.place(x=20, y=200)

        self.panel_rigth=tk.Frame(self.root, bg=self.COLOR_BLANCO, width=500, height=500)
        self.panel_rigth.pack(side="right", fill="both", expand=True)

        self.titulo2=tk.Label(self.panel_rigth, text="INICIO DE SESIÓN", font=("Arial", 22,"bold"), bg=self.COLOR_BLANCO, fg="#333333")
        self.titulo2.place(x=130, y=60)

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
            messagebox.showerror("ERROR","Error en sus credenciales, inténtelo de nuevo.")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniMarket")
        self.geometry("1200x600")
        self.resizable(True,True)
        self.configure(bg="#FFFFFF")
        self.COLOR_FONDO = "#1E90FF"
        self.COLOR_BOTON = "#007BFF"
        self.COLOR_SELECCION = "#0056b3"

        self.panel_left = tk.Frame(self, bg="#1E90FF", width=200, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.panel_right= tk.Frame(self, bg="#FFFFFF")
        self.panel_right.pack(side="right", fill="both", expand=True)

        self.imagen = tk.PhotoImage(file="2.png")
        self.label_logo = tk.Label(self.panel_left, image=self.imagen, bg="#1E90FF")
        self.label_logo.place(x=10, y=20)

        self.button_ventas=tk.Button(self.panel_left, text="VENTAS", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_ventas)
        self.button_ventas.place(x=0, y=150, height=35)

        self.button_buscar_venta = tk.Button(self.panel_left, text="BUSCAR VENTA", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_buscar_venta)
        self.button_buscar_venta.place(x=0, y=220, height=35)

        self.button_inventario = tk.Button(self.panel_left, text="INVENTARIO", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_inventario)
        self.button_inventario.place(x=0, y=290, height=35)

        self.button_proveedores = tk.Button(self.panel_left, text="PROVEEDORES", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_proveedores)
        self.button_proveedores.place(x=0, y=360, height=35)

        self.button_reportes = tk.Button(self.panel_left, text="REPORTES", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_reportes)
        self.button_reportes.place(x=0, y=430, height=35)

        self.button_close= tk.Button(self.panel_left, text="CERRAR SESIÓN", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25, command=self.cerrar_sesion)
        self.button_close.place(x=0, y=550, height=35)

        self.botones=[self.button_ventas, self.button_buscar_venta, self.button_inventario, self.button_proveedores, self.button_reportes]

    def activar_boton(self, boton):
        boton.config(bg=self.COLOR_SELECCION)

    def limpiar_panel(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

    def mostrar_ventas(self):
        self.activar_boton(self.button_ventas)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Sección de Ventas", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_buscar_venta(self):
        self.activar_boton(self.button_buscar_venta)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Buscar Venta", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_inventario(self):
        self.activar_boton(self.button_inventario)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Inventario de Productos", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_proveedores(self):
        self.activar_boton(self.button_proveedores)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Gestión de Proveedores", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_reportes(self):
        self.activar_boton(self.button_reportes)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Reportes del Sistema", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def cerrar_sesion(self):
        self.activar_boton(self.button_close)
        self.destroy()
        root = tk.Tk()
        Login(root)
        root.mainloop()


if __name__ == "__main__":
    root=tk.Tk()
    app=Login(root)
    root.mainloop()
