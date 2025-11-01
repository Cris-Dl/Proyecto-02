import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


class Productos:
    def __init__(self, codigo, nombre, precio_compra, precio_venta, categoria, cantidad):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio_venta = precio_venta
        self.__precio_compra = precio_compra
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
    def precio_compra(self):
        return self.__precio_compra

    @precio_compra.setter
    def precio_compra(self, new_precio):
        if new_precio:
            self.__precio_compra = new_precio
        else:
            print("El campo no puede estar vacio")

    @property
    def precio_venta(self):
        return self.__precio_venta

    @precio_venta.setter
    def precio_venta(self, new_precio):
        if new_precio:
            self.__precio_venta = new_precio
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

class Proveedores:
    def __init__(self, nombre, codigo, telefono, ubicacion, informacion):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__telefono = telefono
        self.__ubicacion = ubicacion
        self.__informacion = informacion

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
    def codigo(self):
        return self.__codigo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, new_telefono):
        if new_telefono:
            self.__telefono = new_telefono
        else:
            print("El campo no puede estar vacio")

    @property
    def ubicacion(self):
        return self.__ubicacion

    @ubicacion.setter
    def ubicacion(self, new_ubicacion):
        if new_ubicacion:
            self.__ubicacion = new_ubicacion
        else:
            print("El campo no puede estar vacio")

    @property
    def informacion(self):
        return self.__informacion

    @informacion.setter
    def informacion(self, new_informacion):
        if new_informacion:
            self.__informacion = new_informacion
        else:
            print("El campo no puede estar vacio")


class ProductosDB:
    DB_NAME = "productos.db"

    @staticmethod
    def _conn():
        conn = sqlite3.connect(ProductosDB.DB_NAME)
        conn.row_factory = sqlite3.Row

        # 1. Tabla de productos
        conn.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id_num INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    codigo TEXT UNIQUE NOT NULL,
                    precio_venta REAL,
                    precio_compra REAL,
                    categoria TEXT NOT NULL,
                    cantidad REAL
                );
            """)
        # 2. Tabla de Ventas
        conn.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_venta TEXT NOT NULL,
                    total_venta REAL NOT NULL,
                    detalle_productos TEXT 
                );
            """)
        # 3. Tabla de Categorias
        conn.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL
                );
            """)
        # 4. Tabla proveedores
        conn.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    codigo TEXT UNIQUE NOT NULL,
                    telefono TEXT UNIQUE NOT NULL,
                    ubicacion TEXT NOT NULL,
                    informacion TEXT UNIQUE NOT NULL
                );
            """)

        conn.commit()
        return conn


class GuardarProducto(ProductosDB):
    @staticmethod
    def guardar(producto: Productos):
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, categoria, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
                (producto.nombre, producto.codigo, producto.precio_compra,producto.precio_venta, producto.categoria, producto.cantidad)
            )
            conn.commit()

class ObtenerCodigo(ProductosDB):
    @staticmethod
    def obtener_por_codigo(codigo: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            return cur.fetchone()

class Buscar(ProductosDB):
    @staticmethod
    def buscar_por_cadena(cadena: str):
        patron = '%' + cadena + '%'
        with ProductosDB._conn() as conn:
            cur = conn.execute(
                "SELECT nombre, codigo, precio_venta AS precio, categoria FROM productos WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ? LIMIT 10",
                (patron, patron, patron)
            )
            return cur.fetchall()

class RegistrarVenta(ProductosDB):
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
        print(f"Venta registrada: Total ${total:.2f}")

class ActualizarStock(ProductosDB):
    @staticmethod
    def actualizar_stock(codigo: str, cantidad_vendida: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?",
                (cantidad_vendida, codigo)
            )
            conn.commit()

class ModificarProducto(ProductosDB):
    @staticmethod
    def modificar_producto(codigo: str, nombre: str, precio_compra: float, precio_venta: float, categoria: str,cantidad: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET nombre=?, precio_compra=?, precio_venta=?, categoria=?, cantidad=? WHERE codigo=?",
                (nombre, precio_compra, precio_venta, categoria, cantidad, codigo)
            )
            conn.commit()

class AgregarStock(ProductosDB):
    @staticmethod
    def agregar_stock(codigo: str, cantidad_adicional: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET cantidad = cantidad + ? WHERE codigo = ?",
                (cantidad_adicional, codigo)
            )
            conn.commit()

class ObtenerCategorias(ProductosDB):
    @staticmethod
    def obtener_categorias():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT nombre FROM categorias ORDER BY nombre")
            return [row['nombre'] for row in cur.fetchall()]

class AgregarCategori(ProductosDB):
    @staticmethod
    def agregar_categoria(nombre: str):
        with ProductosDB._conn() as conn:
            conn.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
            conn.commit()

class GuardarProveedor(ProductosDB):
    @staticmethod
    def guardar(proveedor: Proveedores):
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO proveedores (nombre, codigo, telefono, ubicacion, informacion) VALUES (?, ?, ?, ?, ?)",
                (proveedor.nombre, proveedor.codigo, proveedor.telefono, proveedor.ubicacion, proveedor.informacion)
            )
            conn.commit()

class ObtenerProveedores(ProductosDB):
    @staticmethod
    def obtener_todos():
        with ProductosDB._conn() as conn:
            cur = conn.execute(
                "SELECT nombre, codigo, telefono, ubicacion, informacion FROM proveedores ORDER BY nombre"
            )
            return cur.fetchall()



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

        tk.Label(self.panel_right, text="SECCIÓN DE VENTAS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=20)
        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=0, pady=20)

        panel_buscar = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buscar.pack(pady=10)
        tk.Label(panel_buscar, text="Buscar producto:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=5)
        entry_buscar = tk.Entry(panel_buscar, width=50, bg="#E6F3FF", font=("Arial", 12))
        entry_buscar.grid(row=0, column=1, padx=5)

        lista_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        lista_frame.pack(pady=5)
        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="CATEGORÍA", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="PRECIO", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)
        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")
        lista_productos = tk.Listbox(frame_lista_scroll, width=100, height=8, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_productos.pack(side="left")
        scroll.config(command=lista_productos.yview)


        tk.Label(self.panel_right, text="CARRITO", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=(15, 5))
        carrito_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        carrito_frame.pack()
        encabezado_carrito = tk.Frame(carrito_frame, bg="#E6F3FF")
        encabezado_carrito.pack(fill="x")

        tk.Label(encabezado_carrito, text="CANTIDAD", font=("Arial", 11, "bold"), width=10, anchor="w",bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado_carrito, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w",bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado_carrito, text="PRECIO", font=("Arial", 11, "bold"), width=10, anchor="w",bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado_carrito, text="SUBTOTAL", font=("Arial", 11, "bold"), width=10, anchor="w",bg="#E6F3FF").pack(side="left")
        carrito = tk.Listbox(carrito_frame, width=100, height=6, font=("Courier New", 10))
        carrito.pack()

        subtotal_var = tk.DoubleVar(value=0.0)
        frame_total = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_total.pack(pady=5)

        tk.Label(frame_total, text="TOTAL Q.", font=("Arial", 12, "bold"), bg="#FFFFFF").pack(side="left", padx=(10, 5))
        tk.Label(frame_total, textvariable=subtotal_var, font=("Arial", 12, "bold"), bg="#FFFFFF").pack(side="left")

        self.carrito_items = []

        def actualizar_lista(event=None):
            cadena = entry_buscar.get()
            resultados = Buscar.buscar_por_cadena(cadena) if cadena else []
            lista_productos.delete(0, tk.END)
            for r in resultados:
                lista_productos.insert(tk.END,f"{r['codigo']:<22} {r['nombre']:<33} {r['categoria']:<20} Q.{r['precio']:<8.2f}")

        def agregar_al_carrito(event=None):
            if not lista_productos.curselection():
                return
            seleccion = lista_productos.get(lista_productos.curselection())
            codigo = seleccion[:22].strip()
            producto = ObtenerCodigo.obtener_por_codigo(codigo)
            if not producto:
                return
            stock_disponible = producto["cantidad"]
            cantidad_a_sumar = 1
            cantidad_en_carrito = 0
            item_existente = None
            for item in self.carrito_items:
                if item["codigo"] == producto["codigo"]:
                    cantidad_en_carrito = item["cantidad"]
                    item_existente = item
                    break
            total_solicitado = cantidad_en_carrito + cantidad_a_sumar
            if total_solicitado > stock_disponible:
                messagebox.showerror(
                    "Stock Agotado",
                    f"No se puede agregar más de {producto['nombre']}.\n\n"
                    f"Límite de stock: {stock_disponible}\n"
                    f"Actualmente en carrito: {cantidad_en_carrito}"
                )
                return
            if item_existente:
                item_existente["cantidad"] += cantidad_a_sumar
            else:
                self.carrito_items.append({
                    "codigo": producto["codigo"],
                    "nombre": producto["nombre"],
                    "precio": float(producto["precio_venta"]),
                    "cantidad": cantidad_a_sumar
                })
            carrito.delete(0, tk.END)
            total = 0
            for item in self.carrito_items:
                subtotal = item["cantidad"] * item["precio"]
                total += subtotal
                carrito.insert(tk.END,
                               f"{item['cantidad']:<11} {item['nombre']:<34} Q.{item['precio']:<9.2f} Q.{subtotal:<8.2f}")
            subtotal_var.set(total)

        def finalizar_venta():
            if not self.carrito_items:
                messagebox.showerror("Error", "El carrito está vacío.")
                return
            total = subtotal_var.get()
            detalle = [f"{i['cantidad']} x {i['nombre']} @Q.{i['precio']}" for i in self.carrito_items]
            RegistrarVenta.registrar_venta(total, detalle)

            for item in self.carrito_items:
                ActualizarStock.actualizar_stock(item['codigo'], item['cantidad'])

            messagebox.showinfo("Éxito", f"Venta registrada y stock actualizado. Total: Q.{total:.2f}")
            carrito.delete(0, tk.END)
            subtotal_var.set(0.0)
            self.carrito_items.clear()

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_productos.bind("<Double-Button-1>", agregar_al_carrito)

        tk.Button(self.panel_right, text="Finalizar Venta", bg=self.COLOR_BOTON, fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=finalizar_venta).pack(pady=10)

        actualizar_lista()

    def mostrar_buscar_venta(self):
        self.activar_boton(self.button_buscar_venta)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="BUSCAR VENTA", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=20)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

        panel_filtros = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_filtros.pack(pady=10)

        tk.Label(panel_filtros, text="Fecha (dd-mm-yyyy):", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0,column=0,padx=5)
        entry_fecha = tk.Entry(panel_filtros, width=20, bg="#E6F3FF", font=("Arial", 12))
        entry_fecha.grid(row=0, column=1, padx=5)

        tk.Button(panel_filtros, text="Buscar", bg=self.COLOR_BOTON, fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2",command=lambda: actualizar_lista(entry_fecha.get())).grid(row=0, column=2, padx=10)

        resumen_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        resumen_frame.pack(pady=5)


        COLOR_ENCABEZADO = "#E6F3FF"
        encabezado = tk.Frame(resumen_frame, bg=COLOR_ENCABEZADO)
        encabezado.pack(side="top", fill="x")


        tk.Label(encabezado, text="ID", font=("Arial", 11, "bold"), width=9, anchor="w", bg=COLOR_ENCABEZADO).pack(side="left")
        tk.Label(encabezado, text="FECHA Y HORA", font=("Arial", 11, "bold"), width=35, anchor="w", bg=COLOR_ENCABEZADO).pack(side="left")
        tk.Label(encabezado, text="TOTAL", font=("Arial", 11, "bold"), width=20, anchor="w", bg=COLOR_ENCABEZADO).pack(side="left")

        frame_lista_scroll_resumen = tk.Frame(resumen_frame)
        frame_lista_scroll_resumen.pack(side="top")

        scroll = tk.Scrollbar(frame_lista_scroll_resumen)
        scroll.pack(side="right", fill="y")

        lista_resumen = tk.Listbox(frame_lista_scroll_resumen, width=80, height=5, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_resumen.pack(side="left")
        scroll.config(command=lista_resumen.yview)

        tk.Label(self.panel_right, text="DETALLE DE LA VENTA", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=(15, 5))

        detalle_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        detalle_frame.pack(fill="x", padx=10)

        encabezado_detalle = tk.Frame(detalle_frame, bg="#E6F3FF")
        encabezado_detalle.pack(side="top")

        tk.Label(encabezado_detalle, text="CANTIDAD", font=("Arial", 10, "bold"), width=35, anchor="w",bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado_detalle, text="PRODUCTO", font=("Arial", 10, "bold"), width=35, anchor="w",bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado_detalle, text="PRECIO", font=("Arial", 10, "bold"), width=10, anchor="w",bg="#E6F3FF").pack(side="left")
        frame_lista = tk.Frame(detalle_frame)
        frame_lista.pack(pady=10)

        scroll_detalle = tk.Scrollbar(frame_lista)
        scroll_detalle.pack(side="right", fill="y")

        lista_detalle = tk.Listbox(frame_lista, width=80, height=6, font=("Courier New", 10),yscrollcommand=scroll_detalle.set)
        lista_detalle.pack(side="left")

        scroll_detalle.config(command=lista_detalle.yview)

        total_var = tk.DoubleVar(value=0.0)
        frame_total = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_total.pack(pady=5)

        tk.Label(frame_total, text="TOTAL Q.", font=("Arial", 12, "bold"), bg="#FFFFFF").pack(side="left", padx=(10, 5))
        tk.Label(frame_total, textvariable=total_var, font=("Arial", 12, "bold"), bg="#FFFFFF").pack(side="left")

        def actualizar_lista(fecha_buscar=""):
            lista_resumen.delete(0, tk.END)
            with ProductosDB._conn() as conn:
                if fecha_buscar:
                    cur = conn.execute("SELECT id_venta, fecha_venta, total_venta FROM ventas WHERE fecha_venta LIKE ?",('%' + fecha_buscar + '%',))
                else:
                    cur = conn.execute("SELECT id_venta, fecha_venta, total_venta FROM ventas ORDER BY id_venta DESC LIMIT 50")
                for v in cur.fetchall():
                    lista_resumen.insert(tk.END,f"{v['id_venta']:<10} {v['fecha_venta']:<40} Q.{v['total_venta']:<10.2f}")


        def mostrar_detalle(event):
            if not lista_resumen.curselection():
                return
            indice = lista_resumen.curselection()[0]
            seleccion = lista_resumen.get(indice)
            id_venta = int(seleccion[:10].strip())
            lista_detalle.delete(0, tk.END)
            with ProductosDB._conn() as conn:
                cur = conn.execute("SELECT detalle_productos, total_venta FROM ventas WHERE id_venta=?", (id_venta,))
                venta = cur.fetchone()
                if venta:
                    detalle_productos_str = venta['detalle_productos']
                    total_venta = venta['total_venta']

                    for item in detalle_productos_str.split(" | "):
                        try:
                            cantidad, info_producto = item.split(" x ", 1)
                            cantidad = cantidad.strip()

                            nombre, precio_unidad_str = info_producto.split(" @Q.", 1)
                            nombre = nombre.strip()
                            precio_unidad = float(precio_unidad_str.strip())

                            lista_detalle.insert(tk.END,f"{cantidad:<35} {nombre:<35} Q.{precio_unidad:<10.2f}")
                        except ValueError:
                            lista_detalle.insert(tk.END, f"ERROR DE FORMATO: {item}")

                    total_var.set(total_venta)

        lista_resumen.bind("<<ListboxSelect>>", mostrar_detalle)
        actualizar_lista()

    def mostrar_inventario(self):
        self.activar_boton(self.button_inventario)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="INVENTARIO DE PRODUCTOS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=0)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar=tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_BOTON, fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", width=25, command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(panel_buttons, text="ELIMINAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_eliminar_producto)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)

        btn_categorias = tk.Button(panel_buttons, text="CATEGORÍAS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_categorias)
        btn_categorias.grid(row=0, column=3, padx=10, pady=5)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=20)

    def mostrar_proveedores(self):
        self.activar_boton(self.button_proveedores)
        self.limpiar_panel()

        tk.Label(self.panel_right,text="GESTION DE PROVEEDORES",font=("Arial", 18, "bold"),bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=(0, 15))

        btn_agregar = tk.Button(frame_botones, text="AGREGAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_agregar_proveedor)
        btn_agregar.grid(row=0, column=0, padx=10)

        btn_editar = tk.Button(frame_botones, text="EDITAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_editar_proveedor)
        btn_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(frame_botones, text="ELIMINAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_eliminar_proveedor)
        btn_eliminar.grid(row=0, column=2, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)


    def mostrar_reportes(self):
        self.activar_boton(self.button_reportes)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="REPORTES DEL SISTEMA", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

    def mostrar_agregar_producto(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                widget.destroy()

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.place(x=300, y=200, width=600, height=400)
        panel_form._formulario = True

        tk.Label(panel_form, text="AGREGAR PRODUCTO AL INVENTARIO", font=("Arial", 14, "bold"), bg="#FFFFFF").place(x=130, y=0)

        tk.Label(panel_form, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=40)
        entry_nombre = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_nombre.place(x=200, y=40, height=25)

        tk.Label(panel_form, text="CÓDIGO:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=80)
        entry_codigo = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_codigo.place(x=200, y=80, height=25)

        tk.Label(panel_form, text="PRECIO COMPRA:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=120)
        entry_precio = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_precio.place(x=200, y=120, height=25)

        tk.Label(panel_form, text="PRECIO VENTA:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=160)
        entry_precio_venta = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_precio_venta.place(x=200, y=160, height=25)

        tk.Label(panel_form, text="CATEGORÍA:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=200)
        entry_categoria = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_categoria.place(x=200, y=200, height=25)

        tk.Label(panel_form, text="CANTIDAD:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=240)
        entry_cantidad = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_cantidad.place(x=200, y=240, height=25)

        def guardar_producto():
            if not all([entry_codigo.get(), entry_nombre.get(), entry_precio.get(), entry_categoria.get(),
                        entry_cantidad.get()]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            producto = Productos(codigo=entry_codigo.get(), nombre=entry_nombre.get(),precio_venta=float(entry_precio_venta.get()), precio_compra=float(entry_precio.get()),categoria=entry_categoria.get(), cantidad=float(entry_cantidad.get()))
            GuardarProducto.guardar(producto)
            messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' agregado correctamente.")

        tk.Button(panel_form, text="GUARDAR PRODUCTO", bg=self.COLOR_BOTON, fg="white", font=("Arial", 10, "bold"),relief="flat", cursor="hand2", command=guardar_producto).place(x=200, y=280, width=200, height=35)

    def mostrar_editar_producto(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_inventario)

        tk.Label(self.panel_right, text="INVENTARIO DE PRODUCTOS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=5)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar = tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(panel_buttons, text="ELIMINAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_producto)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)

        btn_categorias = tk.Button(panel_buttons, text="CATEGORÍAS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_categorias)
        btn_categorias.grid(row=0, column=3, padx=10, pady=5)

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

        etiquetas = ["NOMBRE:", "PRECIO COMPRA:", "PRECIO VENTA:", "CATEGORÍA:", "CANTIDAD:"]
        entradas = []
        for i, texto in enumerate(etiquetas):
            tk.Label(campos_frame, text=texto, font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=i, column=0, padx=5,pady=5, sticky="e")
            e = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas.append(e)

        entry_nombre, entry_precio_compra, entry_precio_venta, entry_categoria, entry_cantidad = entradas

        btn_guardar = tk.Button(campos_frame, text="GUARDAR CAMBIOS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2")
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=15)

        self.codigo_actual_edicion = None

        def actualizar_lista(event=None):
            cadena = entry_buscar.get()
            resultados = Buscar.buscar_por_cadena(cadena) if cadena else []
            lista.delete(0, tk.END)
            for r in resultados:
                lista.insert(tk.END, f"{r['codigo']:<22}  {r['nombre']:<33}  {r['categoria']:<20}")

        def mostrar_campos_edicion(producto):
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, producto["nombre"])
            entry_precio_compra.delete(0, tk.END)
            entry_precio_compra.insert(0, producto["precio_compra"])
            entry_precio_venta.delete(0, tk.END)
            entry_precio_venta.insert(0, producto["precio_venta"])
            entry_categoria.delete(0, tk.END)
            entry_categoria.insert(0, producto["categoria"])
            entry_cantidad.delete(0, tk.END)
            entry_cantidad.insert(0, producto["cantidad"])
            self.codigo_actual_edicion = producto["codigo"]

        def seleccionar_producto(event):
            if lista.curselection():
                seleccion = lista.get(lista.curselection())
                codigo = seleccion[:22].strip()
                producto = ObtenerCodigo.obtener_por_codigo(codigo)
                if producto:
                    mostrar_campos_edicion(producto)

        def guardar_cambios():
            if not self.codigo_actual_edicion:
                messagebox.showerror("Error", "Seleccione un producto primero.")
                return

            nuevo_nombre = entry_nombre.get().strip()
            nuevo_precio_compra = entry_precio_compra.get().strip()
            nuevo_precio_venta = entry_precio_venta.get().strip()
            nueva_categoria = entry_categoria.get().strip()
            nueva_cantidad = entry_cantidad.get().strip()

            if not all([nuevo_nombre, nuevo_precio_compra, nuevo_precio_venta, nueva_categoria, nueva_cantidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                ModificarProducto.modificar_producto(codigo=self.codigo_actual_edicion,nombre=nuevo_nombre,precio_compra=float(nuevo_precio_compra),precio_venta=float(nuevo_precio_venta),categoria=nueva_categoria,cantidad=float(nueva_cantidad))

                messagebox.showinfo("Éxito", f"Producto '{nuevo_nombre}' actualizado correctamente.")

                for e in entradas:
                    e.delete(0, tk.END)

                self.codigo_actual_edicion = None
                entry_buscar.delete(0, tk.END)
                actualizar_lista()

            except ValueError:
                messagebox.showerror("Error", "Los precios y cantidad deben ser números válidos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el producto: {str(e)}")

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista.bind("<<ListboxSelect>>", seleccionar_producto)
        btn_guardar.config(command=guardar_cambios)

    def mostrar_eliminar_producto(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_inventario)

        tk.Label(self.panel_right, text="INVENTARIO DE PRODUCTOS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=5)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar = tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(panel_buttons, text="ELIMINAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_producto)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)

        btn_categorias = tk.Button(panel_buttons, text="CATEGORÍAS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_categorias)
        btn_categorias.grid(row=0, column=3, padx=10, pady=5)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=20)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_form, text="ELIMINAR PRODUCTO", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=5)

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

        def actualizar_lista(event=None):
            try:
                cadena = entry_buscar.get().strip()
                resultados = Buscar.buscar_por_cadena(cadena) if cadena else []

                lista.delete(0, tk.END)

                for r in resultados:
                    lista.insert(tk.END, f"{r['codigo']:<22}  {r['nombre']:<33}  {r['categoria']:<20}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar lista: {str(e)}")

        def obtener_codigo_seleccionado():
            if not lista.curselection():
                return None
            seleccion = lista.get(lista.curselection())
            return seleccion[:22].strip()

        def eliminar_producto():
            codigo = obtener_codigo_seleccionado()

            if not codigo:
                messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
                return

            try:
                producto = ObtenerCodigo.obtener_por_codigo(codigo)
                nombre = producto['nombre'] if producto else codigo

                confirmar = messagebox.askyesno("Confirmar eliminación",f"¿Está seguro de eliminar el producto?\n\n"f"Código: {codigo}\n"f"Nombre: {nombre}\n\n"f"Esta acción no se puede deshacer.")

                if confirmar:
                    with ProductosDB._conn() as conn:
                        cursor = conn.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
                        conn.commit()

                        if cursor.rowcount > 0:
                            messagebox.showinfo("Éxito",f"Producto '{nombre}' eliminado correctamente.")
                            actualizar_lista()
                            entry_buscar.focus()
                        else:
                            messagebox.showerror("Error",f"No se encontró el producto con código {codigo}.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{str(e)}")

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista.bind("<Delete>", lambda e: eliminar_producto())
        lista.bind("<Double-Button-1>", lambda e: eliminar_producto())

        btn_eliminar_prod = tk.Button(panel_form,text="ELIMINAR PRODUCTO",bg=self.COLOR_BOTON,fg="white",font=("Arial", 11, "bold"),relief="flat",cursor="hand2",command=eliminar_producto)
        btn_eliminar_prod.pack(pady=15)
        entry_buscar.focus()

    def mostrar_agregar_proveedor(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_proveedores)

        tk.Label(self.panel_right, text="GESTION DE PROVEEDORES", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=(0, 15))

        btn_agregar = tk.Button(frame_botones, text="AGREGAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_proveedor)
        btn_agregar.grid(row=0, column=0, padx=10)

        btn_editar = tk.Button(frame_botones, text="EDITAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_editar_proveedor)
        btn_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(frame_botones, text="ELIMINAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25, command=self.mostrar_eliminar_proveedor)
        btn_eliminar.grid(row=0, column=2, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_form, text="AGREGAR NUEVO PROVEEDOR", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        campos_frame = tk.Frame(panel_form, bg="#FFFFFF")
        campos_frame.pack(pady=20)

        tk.Label(campos_frame, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0, padx=5,pady=10, sticky="e")
        entry_nombre = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_nombre.grid(row=0, column=1, padx=5, pady=10)

        tk.Label(campos_frame, text="CÓDIGO:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=1, column=0, padx=5,pady=10, sticky="e")
        entry_codigo = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_codigo.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(campos_frame, text="TELÉFONO:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=2, column=0, padx=5,pady=10, sticky="e")
        entry_telefono = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_telefono.grid(row=2, column=1, padx=5, pady=10)

        tk.Label(campos_frame, text="UBICACIÓN:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=3, column=0,padx=5, pady=10,sticky="e")
        entry_ubicacion = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_ubicacion.grid(row=3, column=1, padx=5, pady=10)

        tk.Label(campos_frame, text="INFORMACIÓN:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=4, column=0,padx=5, pady=10,sticky="e")
        entry_informacion = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_informacion.grid(row=4, column=1, padx=5, pady=10)

        def guardar_proveedor():
            nombre = entry_nombre.get().strip()
            codigo = entry_codigo.get().strip()
            telefono = entry_telefono.get().strip()
            ubicacion = entry_ubicacion.get().strip()
            informacion = entry_informacion.get().strip()

            if not all([nombre, codigo, telefono, ubicacion, informacion]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                proveedor = Proveedores(nombre=nombre, codigo=codigo, telefono=telefono,ubicacion=ubicacion, informacion=informacion)
                GuardarProveedor.guardar(proveedor)
                messagebox.showinfo("Éxito", f"Proveedor '{nombre}' agregado correctamente.")

                entry_nombre.delete(0, tk.END)
                entry_codigo.delete(0, tk.END)
                entry_telefono.delete(0, tk.END)
                entry_ubicacion.delete(0, tk.END)
                entry_informacion.delete(0, tk.END)
                entry_nombre.focus()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el proveedor:\n{str(e)}")

        btn_guardar = tk.Button(campos_frame, text="GUARDAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=guardar_proveedor, width=30)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)

        entry_nombre.focus()

    def mostrar_editar_proveedor(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_proveedores)

        tk.Label(self.panel_right, text="GESTION DE PROVEEDORES", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=(0, 15))

        btn_agregar = tk.Button(frame_botones, text="AGREGAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_proveedor)
        btn_agregar.grid(row=0, column=0, padx=10)

        btn_editar = tk.Button(frame_botones, text="EDITAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_proveedor)
        btn_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(frame_botones, text="ELIMINAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_proveedor)
        btn_eliminar.grid(row=0, column=2, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_form, text="EDITAR PROVEEDOR", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=5)

        tk.Label(panel_form, text="Buscar (nombre, código o teléfono):", font=("Arial", 12, "bold"),bg="#FFFFFF").pack(pady=(5, 0))
        entry_buscar = tk.Entry(panel_form, width=50, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_buscar.pack(pady=5)

        lista_frame = tk.Frame(panel_form, bg="#FFFFFF")
        lista_frame.pack(pady=5)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack()

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="TELÉFONO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista_scroll, width=80, height=5, font=("Courier New", 10), yscrollcommand=scroll.set)
        lista.pack(side="left", padx=0)
        scroll.config(command=lista.yview)

        campos_frame = tk.Frame(panel_form, bg="#FFFFFF")
        campos_frame.pack(pady=10)

        etiquetas = ["NOMBRE:", "TELÉFONO:", "UBICACIÓN:", "INFORMACIÓN:"]
        entradas = []
        for i, texto in enumerate(etiquetas):
            tk.Label(campos_frame, text=texto, font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=i, column=0, padx=5,pady=5, sticky="e")
            e = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
            e.grid(row=i, column=1, padx=5, pady=5)
            entradas.append(e)

        entry_nombre, entry_telefono, entry_ubicacion, entry_informacion = entradas

        btn_guardar = tk.Button(campos_frame, text="GUARDAR CAMBIOS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2")
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=15)

        self.codigo_actual_proveedor = None

        def actualizar_lista(event=None):
            try:
                cadena = entry_buscar.get().strip()
                lista.delete(0, tk.END)

                with ProductosDB._conn() as conn:
                    if cadena:
                        patron = '%' + cadena + '%'
                        cur = conn.execute(
                            "SELECT nombre, codigo, telefono, ubicacion, informacion FROM proveedores WHERE nombre LIKE ? OR codigo LIKE ? OR telefono LIKE ? LIMIT 10",
                            (patron, patron, patron)
                        )
                    else:
                        cur = conn.execute(
                            "SELECT nombre, codigo, telefono, ubicacion, informacion FROM proveedores ORDER BY nombre LIMIT 10")

                    for r in cur.fetchall():
                        lista.insert(tk.END, f"{r['codigo']:<22}  {r['nombre']:<33}  {r['telefono']:<20}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar lista: {str(e)}")

        def mostrar_campos_edicion(proveedor):
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, proveedor["nombre"])
            entry_telefono.delete(0, tk.END)
            entry_telefono.insert(0, proveedor["telefono"])
            entry_ubicacion.delete(0, tk.END)
            entry_ubicacion.insert(0, proveedor["ubicacion"])
            entry_informacion.delete(0, tk.END)
            entry_informacion.insert(0, proveedor["informacion"])
            self.codigo_actual_proveedor = proveedor["codigo"]

        def seleccionar_proveedor(event):
            if lista.curselection():
                seleccion = lista.get(lista.curselection())
                codigo = seleccion[:22].strip()

                with ProductosDB._conn() as conn:
                    cur = conn.execute("SELECT * FROM proveedores WHERE codigo = ?", (codigo,))
                    proveedor = cur.fetchone()
                    if proveedor:
                        mostrar_campos_edicion(proveedor)

        def guardar_cambios():
            if not self.codigo_actual_proveedor:
                messagebox.showerror("Error", "Seleccione un proveedor primero.")
                return

            nuevo_nombre = entry_nombre.get().strip()
            nuevo_telefono = entry_telefono.get().strip()
            nueva_ubicacion = entry_ubicacion.get().strip()
            nueva_informacion = entry_informacion.get().strip()

            if not all([nuevo_nombre, nuevo_telefono, nueva_ubicacion, nueva_informacion]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                with ProductosDB._conn() as conn:
                    conn.execute(
                        "UPDATE proveedores SET nombre=?, telefono=?, ubicacion=?, informacion=? WHERE codigo=?",
                        (nuevo_nombre, nuevo_telefono, nueva_ubicacion, nueva_informacion, self.codigo_actual_proveedor)
                    )
                    conn.commit()

                messagebox.showinfo("Éxito", f"Proveedor '{nuevo_nombre}' actualizado correctamente.")

                for e in entradas:
                    e.delete(0, tk.END)

                self.codigo_actual_proveedor = None
                entry_buscar.delete(0, tk.END)
                actualizar_lista()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {str(e)}")

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista.bind("<<ListboxSelect>>", seleccionar_proveedor)
        btn_guardar.config(command=guardar_cambios)

        actualizar_lista()

    def mostrar_eliminar_proveedor(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

        self.activar_boton(self.button_proveedores)

        tk.Label(self.panel_right, text="GESTION DE PROVEEDORES", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=(0, 15))

        btn_agregar = tk.Button(frame_botones, text="AGREGAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_proveedor)
        btn_agregar.grid(row=0, column=0, padx=10)

        btn_editar = tk.Button(frame_botones, text="EDITAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_proveedor)
        btn_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(frame_botones, text="ELIMINAR PROVEEDOR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_proveedor)
        btn_eliminar.grid(row=0, column=2, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_form, text="ELIMINAR PROVEEDOR", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=5)

        tk.Label(panel_form, text="Buscar (nombre, código o teléfono):", font=("Arial", 12, "bold"),bg="#FFFFFF").pack(pady=(5, 0))
        entry_buscar = tk.Entry(panel_form, width=50, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_buscar.pack(pady=5)

        lista_frame = tk.Frame(panel_form, bg="#FFFFFF")
        lista_frame.pack(pady=5)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack()

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="TELÉFONO", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista_scroll, width=80, height=5, font=("Courier New", 10), yscrollcommand=scroll.set)
        lista.pack(side="left", padx=0)
        scroll.config(command=lista.yview)

        def actualizar_lista(event=None):
            try:
                cadena = entry_buscar.get().strip()
                lista.delete(0, tk.END)

                with ProductosDB._conn() as conn:
                    if cadena:
                        patron = '%' + cadena + '%'
                        cur = conn.execute(
                            "SELECT nombre, codigo, telefono FROM proveedores WHERE nombre LIKE ? OR codigo LIKE ? OR telefono LIKE ? LIMIT 10",
                            (patron, patron, patron)
                        )
                    else:
                        cur = conn.execute("SELECT nombre, codigo, telefono FROM proveedores ORDER BY nombre LIMIT 10")

                    for r in cur.fetchall():
                        lista.insert(tk.END, f"{r['codigo']:<22}  {r['nombre']:<33}  {r['telefono']:<20}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar lista: {str(e)}")

        def obtener_codigo_seleccionado():
            if not lista.curselection():
                return None
            seleccion = lista.get(lista.curselection())
            return seleccion[:22].strip()

        def eliminar_proveedor():
            codigo = obtener_codigo_seleccionado()

            if not codigo:
                messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar.")
                return

            try:
                with ProductosDB._conn() as conn:
                    cur = conn.execute("SELECT nombre FROM proveedores WHERE codigo=?", (codigo,))
                    proveedor = cur.fetchone()
                    nombre = proveedor['nombre'] if proveedor else codigo

                    confirmar = messagebox.askyesno("Confirmar eliminación",
                                                    f"¿Está seguro de eliminar el proveedor?\n\n"
                                                    f"Código: {codigo}\n"
                                                    f"Nombre: {nombre}\n\n"
                                                    f"Esta acción no se puede deshacer.")

                    if confirmar:
                        cursor = conn.execute("DELETE FROM proveedores WHERE codigo=?", (codigo,))
                        conn.commit()

                        if cursor.rowcount > 0:
                            messagebox.showinfo("Éxito", f"Proveedor '{nombre}' eliminado correctamente.")
                            actualizar_lista()
                            entry_buscar.focus()
                        else:
                            messagebox.showerror("Error", f"No se encontró el proveedor con código {codigo}.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el proveedor:\n{str(e)}")

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista.bind("<Delete>", lambda e: eliminar_proveedor())
        lista.bind("<Double-Button-1>", lambda e: eliminar_proveedor())

        btn_eliminar_prov = tk.Button(panel_form,text="ELIMINAR PROVEEDOR",bg=self.COLOR_BOTON,fg="white",font=("Arial", 11, "bold"),relief="flat",cursor="hand2",command=eliminar_proveedor)
        btn_eliminar_prov.pack(pady=15)

        entry_buscar.focus()
        actualizar_lista()

    def mostrar_categorias(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                widget.destroy()

        panel_categorias = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_categorias.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(panel_categorias, text="GESTIÓN DE CATEGORÍAS", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        frame_acciones = tk.Frame(panel_categorias, bg="#FFFFFF")
        frame_acciones.pack(pady=10)

        btn_crear = tk.Button(frame_acciones, text="CREAR CATEGORÍA", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_crear_categoria)
        btn_crear.grid(row=0, column=0, padx=10)

        btn_eliminar_cat = tk.Button(frame_acciones, text="ELIMINAR CATEGORÍA", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_categoria)
        btn_eliminar_cat.grid(row=0, column=1, padx=10)

    def mostrar_crear_categoria(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and len(child.winfo_children()) > 0:
                        try:
                            if child.winfo_children()[0].cget("text") in ["CREAR NUEVA CATEGORÍA","ELIMINAR CATEGORÍA"]:
                                child.destroy()
                        except:
                            pass

        panel_categorias = None
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                panel_categorias = widget
                break

        if not panel_categorias:
            return

        panel_form = tk.Frame(panel_categorias, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel_form, text="CREAR NUEVA CATEGORÍA", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=10)

        campos_frame = tk.Frame(panel_form, bg="#FFFFFF")
        campos_frame.pack(pady=20)

        tk.Label(campos_frame, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0,column=0,padx=5,pady=10,sticky="e")
        entry_nombre = tk.Entry(campos_frame, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_nombre.grid(row=0, column=1, padx=5, pady=10)

        def guardar_categoria():
            nombre = entry_nombre.get().strip()

            if not nombre:
                messagebox.showerror("Error", "El nombre de la categoría es obligatorio.")
                return

            try:
                AgregarCategori.agregar_categoria(nombre)
                messagebox.showinfo("Éxito", f"Categoría '{nombre}' creada correctamente.")
                entry_nombre.delete(0, tk.END)
                entry_nombre.focus()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la categoría:\n{str(e)}\n\nPosiblemente ya existe.")

        btn_guardar = tk.Button(campos_frame, text="CREAR CATEGORÍA", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=guardar_categoria, width=20)
        btn_guardar.grid(row=1, column=0, columnspan=2, pady=20)

        entry_nombre.focus()

    def mostrar_eliminar_categoria(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and len(child.winfo_children()) > 0:
                        try:
                            if child.winfo_children()[0].cget("text") in ["CREAR NUEVA CATEGORÍA","ELIMINAR CATEGORÍA"]:
                                child.destroy()
                        except:
                            pass

        panel_categorias = None
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                panel_categorias = widget
                break

        if not panel_categorias:
            return

        panel_form = tk.Frame(panel_categorias, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(panel_form, text="ELIMINAR CATEGORÍA", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=5)

        tk.Label(panel_form, text="Seleccione la categoría a eliminar:", font=("Arial", 12, "bold"),bg="#FFFFFF").pack(pady=(10, 5))

        lista_frame = tk.Frame(panel_form, bg="#FFFFFF")
        lista_frame.pack(pady=5)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack()

        tk.Label(encabezado, text="NOMBRE:", font=("Arial", 11, "bold"), width=55, anchor="w",bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista = tk.Listbox(frame_lista_scroll, width=60, height=4, font=("Arial", 11), yscrollcommand=scroll.set)
        lista.pack(side="left", padx=0)
        scroll.config(command=lista.yview)

        def cargar_categorias():
            lista.delete(0, tk.END)
            categorias = ObtenerCategorias.obtener_categorias()
            for cat in categorias:
                lista.insert(tk.END, cat)

        def obtener_categoria_seleccionada():
            if not lista.curselection():
                return None
            return lista.get(lista.curselection())

        def eliminar_categoria():
            nombre = obtener_categoria_seleccionada()

            if not nombre:
                messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar.")
                return

            try:
                with ProductosDB._conn() as conn:
                    cur = conn.execute("SELECT COUNT(*) as total FROM productos WHERE categoria = ?", (nombre,))
                    resultado = cur.fetchone()
                    total_productos = resultado['total']

                    if total_productos > 0:
                        messagebox.showerror("Error",
                                             f"No se puede eliminar la categoría '{nombre}'.\n\n"
                                             f"Hay {total_productos} producto(s) usando esta categoría.\n"
                                             f"Elimine o reasigne esos productos primero.")
                        return

                    confirmar = messagebox.askyesno("Confirmar eliminación",
                                                    f"¿Está seguro de eliminar la categoría?\n\n"
                                                    f"Categoría: {nombre}\n\n"
                                                    f"Esta acción no se puede deshacer.")

                    if confirmar:
                        cursor = conn.execute("DELETE FROM categorias WHERE nombre=?", (nombre,))
                        conn.commit()

                        if cursor.rowcount > 0:
                            messagebox.showinfo("Éxito", f"Categoría '{nombre}' eliminada correctamente.")
                            cargar_categorias()
                        else:
                            messagebox.showerror("Error", f"No se encontró la categoría '{nombre}'.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría:\n{str(e)}")

        lista.bind("<Delete>", lambda e: eliminar_categoria())
        lista.bind("<Double-Button-1>", lambda e: eliminar_categoria())

        btn_eliminar_cat = tk.Button(panel_form,text="ELIMINAR CATEGORÍA",bg=self.COLOR_BOTON,fg="white",font=("Arial", 11, "bold"),relief="flat",cursor="hand2",command=eliminar_categoria)
        btn_eliminar_cat.pack(pady=15)

        cargar_categorias()

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

