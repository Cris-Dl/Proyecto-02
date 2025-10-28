import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

DB_NAME = "productos.db"

class Productos:
    def __init__(self, codigo, nombre, precio, categoria, cantidad):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio
        self.__categoria = categoria
        self.__cantidad = cantidad

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, new_nombre):
        if new_nombre:
            self.__nombre = new_nombre
        else:
            print("El campo no puede estar vacio")

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, new_precio):
        if new_precio:
            self.__precio = new_precio
        else:
            print("El campo no puede estar vacio")

    @property
    def categoria(self):
        return self.__categoria

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, new_cantidad):
        if new_cantidad:
            self.__cantidad = new_cantidad
        else:
            print("El campo no puede estar vacio")

class ProductosDB:
    DB_NAME = "productos.db"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(ProductosDB.DB_NAME)
        conn.row_factory = sqlite3.Row
        #Tabla de productos
        conn.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    codigo TEXT NOT NULL,
                    precio REAL,
                    categoria TEXT NOT NULL,
                    cantidad REAL
                );
            """)

        # Tabla de Ventas
        conn.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_venta TEXT NOT NULL,
                    total_venta REAL NOT NULL,
                    detalle_productos TEXT 
                );
            """)
        conn.commit()
        return conn

    @staticmethod
    def guardar(producto: Productos):
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO productos (nombre, codigo, precio, categoria, cantidad) VALUES (?, ?, ?, ?, ?)",
                (producto.nombre, producto.codigo, producto.precio, producto.categoria, producto.cantidad)
            )


    @staticmethod
    def obtener_por_codigo(codigo: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            return cur.fetchone()

    @staticmethod
    def buscar_por_cadena(cadena: str):
        patron = '%' + cadena + '%'
        with ProductosDB._conn() as conn:
            cur = conn.execute(
                "SELECT nombre, codigo, categoria FROM productos WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ? LIMIT 15",
                (patron, patron, patron)
            )
            return cur.fetchall()

    @staticmethod
    def registrar_venta(total: float, detalle_productos: list):
        fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        detalle_str = " | ".join(detalle_productos)
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO ventas (fecha_venta, total_venta, detalle_productos) VALUES (?, ?, ?)",
                (fecha_actual, total, detalle_str)
            )
            conn.commit()


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
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)
        self.state('zoomed')

        self.panel_left = tk.Frame(self, bg="#1E90FF", width=200, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.panel_right= tk.Frame(self, bg="#FFFFFF")
        self.panel_right.pack(side="right", fill="both", expand=True)

        self.imagen = tk.PhotoImage(file="2.png")
        self.label_logo = tk.Label(self.panel_left, image=self.imagen, bg="#1E90FF")
        self.label_logo.place(x=10, y=20)
        self.label_logo.bind("<Button-1>", self.mostrar_menu_principal)

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

        self.mostrar_menu_principal()
    def activar_boton(self, boton):
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)
        boton.config(bg=self.COLOR_SELECCION)

    def limpiar_panel(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self, event=None):
        self.limpiar_panel()
        tk.Label(self.panel_right, text="MENÚ PRINCIPAL", font=("Arial", 22, "bold"), bg="#FFFFFF").pack(pady=50)
        tk.Label(self.panel_right, text="¡Bienvenido al MiniMarket!", font=("Arial", 16), bg="#FFFFFF").pack(pady=20)
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)

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
        tk.Label(self.panel_right, text="Inventario de Productos", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=0)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar=tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_BOTON, fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", width=25, command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=20)

    def mostrar_proveedores(self):
        self.activar_boton(self.button_proveedores)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Gestión de Proveedores", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_reportes(self):
        self.activar_boton(self.button_reportes)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="Reportes del Sistema", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=50)

    def mostrar_agregar_producto(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget,tk.Frame) and widget.winfo_y() > 150:
                widget.destroy()

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.place(x=300, y=150, width=600, height=330)
        panel_form._formulario = True

        tk.Label(panel_form, text="AGREGAR PRODUCTO AL INVENTARIO",font=("Arial", 14, "bold"), bg="#FFFFFF").place(x=130, y=10)

        tk.Label(panel_form, text="NOMBRE:", font=("Arial", 12, "bold"),bg="#FFFFFF").place(x=50, y=60)
        entry_nombre = tk.Entry(panel_form, width=40, bg="#E6F3FF",relief="flat", font=("Arial", 12))
        entry_nombre.place(x=200, y=60, height=25)

        tk.Label(panel_form, text="CÓDIGO:", font=("Arial", 12, "bold"),bg="#FFFFFF").place(x=50, y=100)
        entry_codigo = tk.Entry(panel_form, width=40, bg="#E6F3FF",relief="flat", font=("Arial", 12))
        entry_codigo.place(x=200, y=100, height=25)

        tk.Label(panel_form, text="PRECIO:", font=("Arial", 12, "bold"),bg="#FFFFFF").place(x=50, y=140)
        entry_precio = tk.Entry(panel_form, width=40, bg="#E6F3FF",relief="flat", font=("Arial", 12))
        entry_precio.place(x=200, y=140, height=25)

        tk.Label(panel_form, text="CATEGORÍA:", font=("Arial", 12, "bold"),bg="#FFFFFF").place(x=50, y=180)
        entry_categoria = tk.Entry(panel_form, width=40, bg="#E6F3FF",relief="flat", font=("Arial", 12))
        entry_categoria.place(x=200, y=180, height=25)

        tk.Label(panel_form, text="CANTIDAD:", font=("Arial", 12, "bold"),bg="#FFFFFF").place(x=50, y=220)
        entry_cantidad = tk.Entry(panel_form, width=40, bg="#E6F3FF",relief="flat", font=("Arial", 12))
        entry_cantidad.place(x=200, y=220, height=25)

        def guardar_producto():
            if not all([entry_codigo.get(), entry_nombre.get(), entry_precio.get(),entry_categoria.get(), entry_cantidad.get()]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            producto = Productos(codigo=entry_codigo.get(),nombre=entry_nombre.get(),precio=float(entry_precio.get()),categoria=entry_categoria.get(),cantidad=float(entry_cantidad.get()))
            ProductosDB.guardar(producto)
            messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' agregado correctamente.")

        tk.Button(panel_form, text="GUARDAR PRODUCTO", bg=self.COLOR_BOTON,fg="white", font=("Arial", 10, "bold"), relief="flat",cursor="hand2", command=guardar_producto).place(x=200, y=270, width=200, height=35)

    def mostrar_editar_producto(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_inventario)

        tk.Label(self.panel_right, text="Inventario de Productos", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=5)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar = tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_SELECCION, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=20)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_form, text="EDITAR PRODUCTO", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=5)

        tk.Label(panel_form, text="Buscar (nombre, código o categoría):", font=("Arial", 12, "bold"),bg="#FFFFFF").pack(pady=(5, 0))
        entry_buscar = tk.Entry(panel_form, width=50, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_buscar.pack(pady=5)

        lista_frame = tk.Frame(panel_form, bg="#FFFFFF")
        lista_frame.pack(pady=5)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack()

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="CATEGORÍA", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista_scroll, width=80, height=5, font=("Courier New", 10), yscrollcommand=scroll.set)
        lista.pack(side="left", padx=0)
        scroll.config(command=lista.yview)

        campos_frame = tk.Frame(panel_form, bg="#FFFFFF")
        campos_frame.pack(pady=10)

        etiquetas = ["NOMBRE:", "PRECIO:", "CATEGORÍA:", "CANTIDAD:"]
        entradas = []
        for i, texto in enumerate(etiquetas):
            tk.Label(campos_frame, text=texto, font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=i, column=0, padx=5,pady=5, sticky="e")
            e = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas.append(e)

        entry_nombre, entry_precio, entry_categoria, entry_cantidad = entradas

        btn_guardar = tk.Button(campos_frame, text="GUARDAR CAMBIOS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2")
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=15)

        def actualizar_lista(event=None):
            cadena = entry_buscar.get()
            resultados = ProductosDB.buscar_por_cadena(cadena) if cadena else []
            lista.delete(0, tk.END)
            for r in resultados:
                lista.insert(tk.END, f"{r['codigo']:<22}  {r['nombre']:<33}  {r['categoria']:<20}")

        def mostrar_campos_edicion(producto):
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, producto["nombre"])
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, producto["precio"])
            entry_categoria.delete(0, tk.END)
            entry_categoria.insert(0, producto["categoria"])
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, producto["cantidad"])
            panel_form.codigo_actual = producto["codigo"]

        def seleccionar_producto(event):
            if lista.curselection():
                seleccion = lista.get(lista.curselection())
                codigo = seleccion[:15].strip()
                producto = ProductosDB.obtener_por_codigo(codigo)
                if producto:
                    mostrar_campos_edicion(producto)

        def guardar_cambios():
            if not hasattr(panel_form, "codigo_actual"):
                messagebox.showerror("Error", "Seleccione un producto primero.")
                return

            nuevo_nombre = entry_nombre.get()
            nuevo_precio = entry_precio.get()
            nueva_categoria = entry_categoria.get()
            nueva_cantidad = entry_cantidad.get()

            if not all([nuevo_nombre, nuevo_precio, nueva_categoria, nueva_cantidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            with ProductosDB._conn() as conn:
                conn.execute("""
                    UPDATE productos
                    SET nombre=?, precio=?, categoria=?, cantidad=?
                    WHERE codigo=?
                """, (nuevo_nombre, float(nuevo_precio), nueva_categoria, float(nueva_cantidad),str(panel_form.codigo_actual)))
                conn.commit()

            messagebox.showinfo("Éxito", f"Producto '{nuevo_nombre}' actualizado correctamente.")
            entry_buscar.delete(0, tk.END)
            lista.delete(0, tk.END)

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista.bind("<<ListboxSelect>>", seleccionar_producto)
        btn_guardar.config(command=guardar_cambios)

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmación", "¿Está seguro que desea salir?")
        if respuesta:
            self.destroy()
            root = tk.Tk()
            Login(root)
            root.mainloop()
if __name__ == "__main__":
    root=tk.Tk()
    app=Login(root)
    root.mainloop()
