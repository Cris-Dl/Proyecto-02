import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

def configurar_estilo_combobox():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('Custom.TCombobox',fieldbackground='#E6F3FF',background='#E6F3FF',bordercolor='#E6F3FF',arrowcolor='#333333',borderwidth=1,relief='flat',padding=5)

    style.map('Custom.TCombobox',fieldbackground=[('readonly', '#E6F3FF'), ('disabled', '#E6F3FF')],background=[('readonly', '#E6F3FF')],bordercolor=[('focus', '#E6F3FF')],relief=[('focus', 'flat')])

    style.configure('Custom.TCombobox.Listbox',background='#E6F3FF',fieldbackground='#E6F3FF',selectbackground='#007BFF',selectforeground='white')

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

def ordenamiento_burbuja(lista_productos):
    n = len(lista_productos)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_productos[j].nombre > lista_productos[j + 1].nombre:
                lista_productos[j], lista_productos[j + 1] = lista_productos[j + 1], lista_productos[j]
    return lista_productos

def ordenamiento_seleccion(lista_productos):
    n = len(lista_productos)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if lista_productos[j].nombre < lista_productos[min_idx].nombre:
                min_idx = j
        lista_productos[i], lista_productos[min_idx] = lista_productos[min_idx], lista_productos[i]
    return lista_productos

def ordenamiento_rapido(lista_productos):
    if len(lista_productos) <= 1:
        return lista_productos
    pivote = lista_productos[0]
    menores = []
    mayores = []
    for i in range(1, len(lista_productos)):
        if lista_productos[i].nombre < pivote.nombre:
            menores.append(lista_productos[i])
        else:
            mayores.append(lista_productos[i])
    return ordenamiento_rapido(menores) + [pivote] + ordenamiento_rapido(mayores)


def ordenamiento_shell(lista_productos):
    n = len(lista_productos)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lista_productos[i]
            j = i
            while j >= gap and lista_productos[j - gap].nombre > temp.nombre:
                lista_productos[j] = lista_productos[j - gap]
                j -= gap
            lista_productos[j] = temp
        gap //= 2
    return lista_productos

def busqueda_secuencial(lista_productos, criterio, valor):
    resultados = []
    valor_lower = valor.lower()

    for producto in lista_productos:
        if criterio == 'nombre' and valor_lower in producto.nombre.lower():
            resultados.append(producto)
        elif criterio == 'codigo' and valor_lower in producto.codigo.lower():
            resultados.append(producto)
        elif criterio == 'categoria' and valor_lower in producto.categoria.lower():
            resultados.append(producto)
    return resultados


def busqueda_binaria(lista_productos, nombre_buscado):
    lista_ordenada = ordenamiento_rapido(lista_productos[:])

    izquierda = 0
    derecha = len(lista_ordenada) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_medio = lista_ordenada[medio].nombre.lower()
        nombre_buscar = nombre_buscado.lower()

        if nombre_medio == nombre_buscar:
            return lista_ordenada[medio]
        elif nombre_medio < nombre_buscar:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None

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
                detalle_productos TEXT,
                nit_cliente TEXT DEFAULT 'C/F'
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

        # 5. Tabla clientes
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS clientes (
                            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                            nit TEXT UNIQUE NOT NULL,
                            nombre TEXT NOT NULL,
                            direccion TEXT NOT NULL
                        );
                    """)

        conn.execute("""
                    CREATE TABLE IF NOT EXISTS reportes_novedades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TIMESTAMP NOT NULL,
                        reporte TEXT NOT NULL
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

class BusquedaAvanzada(ProductosDB):
    @staticmethod
    def busqueda_secuencial_db(criterio: str, valor: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos")
            productos_db = cur.fetchall()

            lista_productos = []
            for p in productos_db:
                producto = Productos(
                    codigo=p['codigo'],
                    nombre=p['nombre'],
                    precio_venta=p['precio_venta'],
                    precio_compra=p['precio_compra'],
                    categoria=p['categoria'],
                    cantidad=p['cantidad']
                )
                lista_productos.append(producto)

            resultados = busqueda_secuencial(lista_productos, criterio, valor)

            return [{
                'codigo': p.codigo,
                'nombre': p.nombre,
                'precio': p.precio_venta,
                'precio_compra': p.precio_compra,  # AGREGADO
                'categoria': p.categoria,
                'cantidad': p.cantidad
            } for p in resultados]

    @staticmethod
    def busqueda_binaria_db(nombre: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos")
            productos_db = cur.fetchall()

            lista_productos = []
            for p in productos_db:
                producto = Productos(
                    codigo=p['codigo'],
                    nombre=p['nombre'],
                    precio_venta=p['precio_venta'],
                    precio_compra=p['precio_compra'],
                    categoria=p['categoria'],
                    cantidad=p['cantidad']
                )
                lista_productos.append(producto)

            resultado = busqueda_binaria(lista_productos, nombre)

            if resultado:
                return {
                    'codigo': resultado.codigo,
                    'nombre': resultado.nombre,
                    'precio': resultado.precio_venta,
                    'precio_compra': resultado.precio_compra,  # AGREGADO
                    'categoria': resultado.categoria,
                    'cantidad': resultado.cantidad
                }
            return None

class RegistrarVenta(ProductosDB):
    @staticmethod
    def registrar_venta(total: float, detalle_productos: list, nit_cliente: str = "C/F"):
        fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        detalle_str = " | ".join(detalle_productos)
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO ventas (fecha_venta, total_venta, detalle_productos, nit_cliente) VALUES (?, ?, ?, ?)",
                (fecha_actual, total, detalle_str, nit_cliente)
            )
            conn.commit()


class BuscarVentasPorCliente(ProductosDB):
    @staticmethod
    def buscar_por_nit(nit: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("""
                SELECT v.id_venta, v.fecha_venta, v.total_venta, v.detalle_productos, c.nombre, c.direccion
                FROM ventas v
                LEFT JOIN clientes c ON v.nit_cliente = c.nit
                WHERE v.nit_cliente = ?
                ORDER BY v.fecha_venta DESC
            """, (nit,))
            return cur.fetchall()

    @staticmethod
    def buscar_por_nombre_cliente(nombre: str):
        patron = '%' + nombre + '%'
        with ProductosDB._conn() as conn:
            cur = conn.execute("""
                SELECT v.id_venta, v.fecha_venta, v.total_venta, v.detalle_productos, v.nit_cliente, c.nombre, c.direccion
                FROM ventas v
                LEFT JOIN clientes c ON v.nit_cliente = c.nit
                WHERE c.nombre LIKE ?
                ORDER BY v.fecha_venta DESC
            """, (patron,))
            return cur.fetchall()

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

class ObtenerTodosProductos(ProductosDB):
    @staticmethod
    def obtener_todos():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos")
            productos_db = cur.fetchall()

            lista_productos_obj = []
            for p in productos_db:
                producto = Productos(
                    codigo=p['codigo'],
                    nombre=p['nombre'],
                    precio_venta=p['precio_venta'],
                    precio_compra=p['precio_compra'],
                    categoria=p['categoria'],
                    cantidad=p['cantidad']
                )
                lista_productos_obj.append(producto)
            return lista_productos_obj


class ObtenerProveedores(ProductosDB):
    @staticmethod
    def obtener_todos():
        with ProductosDB._conn() as conn:
            cur = conn.execute(
                "SELECT nombre, codigo, telefono, ubicacion, informacion FROM proveedores ORDER BY nombre"
            )
            return cur.fetchall()

class GuardarReporte(ProductosDB):
    @staticmethod
    def guardar_reporte(texto: str):
        fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO reportes_novedades (fecha, reporte) VALUES (?, ?)",
                (fecha_actual, texto)
            )
            conn.commit()
        print("Reporte guardado exitosamente.")

class VerReportes(ProductosDB):
    @staticmethod
    def ver_reportes():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT id, fecha, reporte FROM reportes_novedades ORDER BY fecha DESC")
            return cur.fetchall()

class ClientesDB(ProductosDB):
    @staticmethod
    def buscar_por_nit(nit: str):
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT nit, nombre, direccion FROM clientes WHERE nit = ?", (nit,))
            return cur.fetchone()

    @staticmethod
    def guardar_cliente(nit: str, nombre: str, direccion: str):
        with ProductosDB._conn() as conn:
            try:
                conn.execute(
                    "INSERT INTO clientes (nit, nombre, direccion) VALUES (?, ?, ?)",
                    (nit, nombre, direccion)
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                conn.execute(
                    "UPDATE clientes SET nombre = ?, direccion = ? WHERE nit = ?",
                    (nombre, direccion, nit)
                )
                conn.commit()
                return True

    @staticmethod
    def obtener_todos_clientes():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT nit, nombre, direccion FROM clientes ORDER BY nombre")
            return cur.fetchall()

class GeneradorFacturas:
    @staticmethod
    def generar_factura_pdf(carrito, total, nit, nombre, direccion):
        fecha = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nombre_archivo = f"Factura_{fecha}.pdf"

        ruta_facturas = os.path.join(os.getcwd(), "Facturas")
        if not os.path.exists(ruta_facturas):
            os.makedirs(ruta_facturas)

        ruta = os.path.join(ruta_facturas, nombre_archivo)

        c = canvas.Canvas(ruta, pagesize=letter)

        margen_x = 20 * mm
        margen_y = 265 * mm

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margen_x, margen_y, "MINIMARKET")

        c.setFont("Helvetica", 10)
        c.drawString(margen_x, margen_y - 10, "Factura electrónica")
        c.drawString(margen_x, margen_y - 25, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, margen_y - 50, "Datos del cliente:")

        c.setFont("Helvetica", 10)
        c.drawString(margen_x, margen_y - 65, f"NIT: {nit}")
        c.drawString(margen_x, margen_y - 80, f"Nombre: {nombre}")
        c.drawString(margen_x, margen_y - 95, f"Dirección: {direccion}")

        y = margen_y - 130
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margen_x, y, "CANT")
        c.drawString(margen_x + 50, y, "PRODUCTO")
        c.drawString(margen_x + 250, y, "PRECIO")
        c.drawString(margen_x + 320, y, "SUBTOTAL")

        c.line(margen_x, y - 5, margen_x + 380, y - 5)

        c.setFont("Helvetica", 10)
        y -= 25

        for item in carrito:
            producto = item["nombre"]
            precio = float(item["precio"])
            cantidad = int(item["cantidad"])
            subtotal = cantidad * precio

            c.drawString(margen_x, y, str(cantidad))
            c.drawString(margen_x + 50, y, producto[:35])
            c.drawString(margen_x + 250, y, f"Q.{precio:.2f}")
            c.drawString(margen_x + 320, y, f"Q.{subtotal:.2f}")

            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, y - 10, f"TOTAL A PAGAR: Q.{total:.2f}")

        c.save()
        return ruta

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
        self.centrar_ventana(900, 500)

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

        tk.Label(self.panel_rigth, text="USUARIO:", font=("Arial", 9,"bold"), bg=self.COLOR_BLANCO).place(x=150,y=160)
        self.entry_user=tk.Entry(self.panel_rigth, width=30, bg=self.COLOR_INPUT,relief="flat", font=("Arial", 10))
        self.entry_user.place(x=150, y=180 , height=30)

        tk.Label(self.panel_rigth, text="CONTRASEÑA:", font=("Arial", 9,"bold"), bg=self.COLOR_BLANCO).place(x=150, y=220)
        self.entry_password=tk.Entry(self.panel_rigth, show="*", width=30, bg=self.COLOR_INPUT, relief="flat", font=("Arial", 10))
        self.entry_password.place(x=150, y=240, height=30)

        self.boton_login=tk.Button(self.panel_rigth, text="INICIAR SESIÓN", bg=self.COLOR_BOTON, fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25, command=self.login)
        self.boton_login.place(x=150, y=300, height=35)

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def login(self):
        user=self.entry_user.get()
        password=self.entry_password.get()
        if user =="ADMIN" and password=="1234":
            self.root.destroy()
            app2=App()
            app2.mainloop()
        elif user == "CAJERA" and password == "5678":
            self.root.destroy()
            app_cajera = AppCajera()
            app_cajera.mainloop()

        elif user == "SUPERADMIN" and password == "A1B2C3":
            self.root.destroy()
            app_delete_db = AppDeleteDB()
            app_delete_db.mainloop()

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
        configurar_estilo_combobox()
        self.carrito_items = []
        self.auth_eliminar_carrito = False

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

        self.button_acerca_de = tk.Button(self.panel_left, text="ACERCA DE", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_acerca_de)
        self.button_acerca_de.place(x=0, y=660, height=35)

        self.button_close= tk.Button(self.panel_left, text="CERRAR SESIÓN", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25, command=self.cerrar_sesion)
        self.button_close.place(x=0, y=550, height=35)

        self.botones=[self.button_ventas, self.button_buscar_venta, self.button_inventario, self.button_proveedores, self.button_reportes, self.button_acerca_de]
        self.mostrar_menu_principal()

    def mostrar_acerca_de(self):
        self.activar_boton(self.button_acerca_de)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="ACERCA DE - SISTEMA MINIMARKET", font=("Arial", 20, "bold"), bg="#FFFFFF",fg="#007BFF").pack(pady=30)

        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=50, pady=10)

        info_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        info_frame.pack(pady=20, padx=50)

        tk.Label(info_frame, text="Versión: 1.0.0", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=10)

        tk.Label(info_frame, text="Sistema de Gestión para MiniMarket", font=("Arial", 12), bg="#FFFFFF",fg="#666666").pack(pady=5)

        tk.Frame(self.panel_right, bg="gray", height=1).pack(fill="x", padx=50, pady=20)

        tk.Label(self.panel_right, text="DESARROLLADO POR:", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=15)

        dev_frame = tk.Frame(self.panel_right, bg="#E6F3FF", relief="solid", borderwidth=2)
        dev_frame.pack(pady=10, padx=100, fill="x")

        tk.Label(dev_frame, text="MAYNOR EDUARDO MORALES CHANG", font=("Arial", 13, "bold"), bg="#E6F3FF",pady=10).pack()
        tk.Label(dev_frame, text="Email: memoralesch@correo.url.edu.gt ", font=("Arial", 12), bg="#E6F3FF", pady=5).pack()
        tk.Label(dev_frame, text="Teléfono: 3570-6701", font=("Arial", 12), bg="#E6F3FF", pady=5).pack()

        tk.Frame(dev_frame, bg="gray", height=1).pack(fill="x", padx=20, pady=10)

        tk.Label(dev_frame, text="CRISTHIAN ESTUARDO DE LEÓN PÉREZ", font=("Arial", 13, "bold"), bg="#E6F3FF",pady=10).pack()
        tk.Label(dev_frame, text="Email: cedeleonpe@correo.url.edu.gt ", font=("Arial", 12), bg="#E6F3FF",pady=5).pack()
        tk.Label(dev_frame, text="Teléfono: 5080-8254", font=("Arial", 12), bg="#E6F3FF", pady=5).pack(pady=(0, 10))

        tk.Label(self.panel_right, text="© 2025 - Todos los derechos reservados", font=("Arial", 10), bg="#FFFFFF",fg="#999999").pack(pady=30)

    def activar_boton(self, boton):
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)
        boton.config(bg=self.COLOR_SELECCION)

    def limpiar_panel(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self, event=None):
        self.limpiar_panel()
        tk.Label(self.panel_right, text="MENÚ PRINCIPAL - ADMINISTRADOR", font=("Arial", 22, "bold"), bg="#FFFFFF").pack(pady=50)
        tk.Label(self.panel_right, text="¡Bienvenido al MiniMarket!", font=("Arial", 16), bg="#FFFFFF").pack(pady=20)
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)

    def aplicar_ordenamiento(self, metodo_nombre, metodo_funcion, lista_productos):
        try:
            productos_obj = ObtenerTodosProductos.obtener_todos()
            import time
            inicio = time.time()
            lista_ordenada = metodo_funcion(productos_obj)
            fin = time.time()
            tiempo_transcurrido = (fin - inicio) * 1000
            lista_productos.delete(0, tk.END)
            for p in lista_ordenada:
                lista_productos.insert(tk.END,f"{p.codigo:<13} {p.nombre:<29} {p.categoria:<16} Q.{float(p.precio_compra):<9.2f} Q.{float(p.precio_venta):<9.2f} {float(p.cantidad):<8.2f}")
            messagebox.showinfo("Ordenamiento Completado",f"Método: {metodo_nombre}\n\n" f"Productos ordenados: {len(lista_ordenada)}\n" f"Tiempo de ejecución: {tiempo_transcurrido:.2f} ms", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar ordenamiento:\n{str(e)}", parent=self)

    def mostrar_ventas(self):
        self.activar_boton(self.button_ventas)
        self.limpiar_panel()
        self.auth_eliminar_carrito = False

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

        subtotal_var = tk.DoubleVar(value=0.00)
        frame_total = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_total.pack(pady=5)

        tk.Label(frame_total, text="TOTAL Q.", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red").pack(side="left", padx=(10, 5))
        label_total = tk.Label(frame_total, text="0.00", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red")
        label_total.pack(side="left")

        def actualizar_carrito_display():
            carrito.delete(0, tk.END)
            total = 0
            for item in self.carrito_items:
                subtotal = item["cantidad"] * item["precio"]
                total += subtotal
                carrito.insert(tk.END,f"{item['cantidad']:<11} {item['nombre']:<34} Q.{item['precio']:<9.2f} Q.{subtotal:<8.2f}")
            subtotal_var.set(total)
            label_total.config(text=f"{total:.2f}")

        def solicitar_autorizacion():
            if self.auth_eliminar_carrito:
                return True

            codigo = simpledialog.askstring("Autorización requerida","Ingrese el código de autorización para eliminar productos del carrito:",show='*')

            if codigo == "A1B2C3":
                self.auth_eliminar_carrito = True
                messagebox.showinfo("Autorizado", "Autorización concedida. Ahora puede eliminar productos del carrito.")
                return True
            elif codigo is not None:
                messagebox.showerror("Error", "Código incorrecto. Autorización denegada.")

            return False

        def modificar_cantidad_carrito(event=None):
            if not carrito.curselection():
                messagebox.showwarning("Advertencia", "Seleccione un producto del carrito para modificar su cantidad.")
                return
            indice = int(carrito.curselection()[0])
            if indice >= len(self.carrito_items):
                return
            item_seleccionado = self.carrito_items[indice]
            producto = ObtenerCodigo.obtener_por_codigo(item_seleccionado["codigo"])
            if not producto:
                messagebox.showerror("Error", "No se encontró el producto en la base de datos.")
                return
            stock_disponible = producto["cantidad"]
            cantidad_actual = item_seleccionado["cantidad"]
            nueva_cantidad_str = simpledialog.askstring("Modificar Cantidad",f"Producto: {item_seleccionado['nombre']}\n" f"Cantidad actual: {cantidad_actual}\n" f"Stock disponible: {stock_disponible}\n\n" f"Ingrese la nueva cantidad:")
            if nueva_cantidad_str is None:
                return
            try:
                nueva_cantidad = float(nueva_cantidad_str)
                if nueva_cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                    return
                if nueva_cantidad > stock_disponible:
                    messagebox.showerror("Stock Insuficiente",f"No hay suficiente stock disponible.\n\n" f"Stock disponible: {stock_disponible}\n" f"Cantidad solicitada: {nueva_cantidad}")
                    return
                item_seleccionado["cantidad"] = int(nueva_cantidad)
                actualizar_carrito_display()
                messagebox.showinfo("Éxito", f"Cantidad actualizada a {int(nueva_cantidad)} unidades.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido.")

        def eliminar_uno_del_carrito(event=None):
            if not carrito.curselection():
                return

            if not solicitar_autorizacion():
                return

            indice = int(carrito.curselection()[0])

            if indice >= len(self.carrito_items):
                return

            item_seleccionado = self.carrito_items[indice]

            if "cantidad" not in item_seleccionado:
                messagebox.showerror("Error", "Estructura de datos inválida")
                return

            item_seleccionado["cantidad"] -= 1

            if item_seleccionado["cantidad"] <= 0:
                self.carrito_items.pop(indice)

            actualizar_carrito_display()

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
                messagebox.showerror("Stock Agotado",f"No se puede agregar más de {producto['nombre']}.\n\n" f"Límite de stock: {stock_disponible}\n" f"Actualmente en carrito: {cantidad_en_carrito}")
                return
            if item_existente:
                item_existente["cantidad"] += cantidad_a_sumar
            else:
                self.carrito_items.append({"codigo": producto["codigo"],"nombre": producto["nombre"],"precio": float(producto["precio_venta"]),"cantidad": cantidad_a_sumar})
            actualizar_carrito_display()
        def vaciar_carrito():
            if not self.carrito_items:
                messagebox.showwarning("Advertencia", "El carrito ya está vacío.")
                return
            if not solicitar_autorizacion():
                return
            confirmar = messagebox.askyesno("Confirmar acción",f"¿Está seguro de que desea vaciar el carrito?\n\n"f"Se eliminarán {len(self.carrito_items)} producto(s).")
            if confirmar:
                self.carrito_items.clear()
                actualizar_carrito_display()
                messagebox.showinfo("Éxito", "El carrito ha sido vaciado.")

        def finalizar_venta():
            if not self.carrito_items:
                messagebox.showerror("Error", "El carrito está vacío.")
                return

            try:
                ClientesDB.guardar_cliente("C/F", "Consumidor Final", "Ciudad")
            except:
                pass

            total = subtotal_var.get()
            detalle = [f"{i['cantidad']} x {i['nombre']} @Q.{i['precio']}" for i in self.carrito_items]
            RegistrarVenta.registrar_venta(total, detalle, "C/F")

            for item in self.carrito_items:
                ActualizarStock.actualizar_stock(item['codigo'], item['cantidad'])

            messagebox.showinfo("Éxito",f"✓ Venta registrada (Cliente: C/F)\n✓ Stock actualizado\n\nTotal: Q.{total:.2f}")
            self.carrito_items.clear()
            actualizar_carrito_display()
            carrito.delete(0, tk.END)
            subtotal_var.set(0.0)

            self.auth_eliminar_carrito = False

        def generar_factura():
            if not self.carrito_items:
                messagebox.showerror("Error", "El carrito está vacío. Agregue productos antes de generar la factura.")
                return

            ventana_factura = tk.Toplevel(self)
            ventana_factura.title("Generar Factura")
            ventana_factura.geometry("500x400")
            ventana_factura.configure(bg="#FFFFFF")
            ventana_factura.resizable(False, False)
            ventana_factura.transient(self)
            ventana_factura.grab_set()

            ventana_factura.update_idletasks()
            x = (ventana_factura.winfo_screenwidth() // 2) - (500 // 2)
            y = (ventana_factura.winfo_screenheight() // 2) - (400 // 2)
            ventana_factura.geometry(f"500x400+{x}+{y}")

            tk.Label(ventana_factura, text="DATOS DEL CLIENTE", font=("Arial", 18, "bold"), bg="#FFFFFF",fg="#007BFF").pack(pady=20)

            tk.Frame(ventana_factura, bg="gray", height=2).pack(fill="x", padx=20, pady=10)

            campos_frame = tk.Frame(ventana_factura, bg="#FFFFFF")
            campos_frame.pack(pady=20, padx=40)

            tk.Label(campos_frame, text="NIT:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,sticky="e", padx=10,pady=15)
            entry_nit = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_nit.grid(row=0, column=1, pady=15)
            entry_nit.focus()

            tk.Label(campos_frame, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=1, column=0,sticky="e", padx=10,pady=15)
            entry_nombre = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_nombre.grid(row=1, column=1, pady=15)

            tk.Label(campos_frame, text="DIRECCIÓN:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=2, column=0,sticky="e",padx=10, pady=15)
            entry_direccion = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_direccion.grid(row=2, column=1, pady=15)

            def autocompletar_cliente(event=None):
                nit = entry_nit.get().strip()
                if len(nit) >= 3:
                    cliente = ClientesDB.buscar_por_nit(nit)
                    if cliente:
                        entry_nombre.delete(0, tk.END)
                        entry_nombre.insert(0, cliente['nombre'])
                        entry_direccion.delete(0, tk.END)
                        entry_direccion.insert(0, cliente['direccion'])
                        entry_nombre.config(bg="#E6F3FF")
                        entry_direccion.config(bg="#E6F3FF")
                    else:
                        entry_nombre.delete(0, tk.END)
                        entry_direccion.delete(0, tk.END)
                        entry_nombre.config(bg="#E6F3FF")
                        entry_direccion.config(bg="#E6F3FF")
                else:
                    entry_nombre.delete(0, tk.END)
                    entry_direccion.delete(0, tk.END)
                    entry_nombre.config(bg="#E6F3FF")
                    entry_direccion.config(bg="#E6F3FF")

            entry_nit.bind("<KeyRelease>", autocompletar_cliente)

            botones_frame = tk.Frame(ventana_factura, bg="#FFFFFF")
            botones_frame.pack(pady=20)

            def procesar_factura():
                nit = entry_nit.get().strip()
                nombre = entry_nombre.get().strip()
                direccion = entry_direccion.get().strip()

                if not nit or not nombre or not direccion:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=ventana_factura)
                    return

                try:
                    ClientesDB.guardar_cliente(nit, nombre, direccion)

                    total = subtotal_var.get()
                    archivo_pdf = GeneradorFacturas.generar_factura_pdf(self.carrito_items, total, nit, nombre,direccion)

                    detalle = [f"{i['cantidad']} x {i['nombre']} @Q.{i['precio']}" for i in self.carrito_items]
                    RegistrarVenta.registrar_venta(total, detalle, nit)

                    for item in self.carrito_items:
                        ActualizarStock.actualizar_stock(item['codigo'], item['cantidad'])

                    ventana_factura.destroy()

                    self.carrito_items.clear()
                    actualizar_carrito_display()
                    self.auth_eliminar_carrito = False

                    respuesta = messagebox.askyesno(
                        "Venta Completada",
                        f"✓ Venta registrada correctamente\n"
                        f"✓ Factura generada: {archivo_pdf}\n"
                        f"✓ Cliente guardado: {nombre}\n"
                        f"✓ Stock actualizado\n\n"
                        f"Total: Q.{total:.2f}\n\n"
                        f"¿Desea abrir la factura ahora?"
                    )

                    if respuesta:
                        import subprocess
                        import platform

                        if platform.system() == 'Windows':
                            os.startfile(archivo_pdf)
                        elif platform.system() == 'Darwin':
                            subprocess.call(['open', archivo_pdf])
                        else:
                            subprocess.call(['xdg-open', archivo_pdf])

                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar la venta:\n{str(e)}", parent=ventana_factura)

            tk.Button(botones_frame, text="GENERAR FACTURA", bg="#007BFF", fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=procesar_factura, width=20).grid(row=0, column=0, padx=10)

            tk.Button(botones_frame, text="CANCELAR", bg="#6c757d", fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=ventana_factura.destroy, width=15).grid(row=0, column=1,padx=10)

        def agregar_enter(event):
            actualizar_lista()
            if lista_productos.size() > 0:
                lista_productos.selection_clear(0, tk.END)
                lista_productos.select_set(0)
                lista_productos.activate(0)
                agregar_al_carrito()
                entry_buscar.delete(0, tk.END)
                actualizar_lista()

        entry_buscar.bind("<Return>", agregar_enter)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_productos.bind("<Double-Button-1>", agregar_al_carrito)
        carrito.bind("<Double-Button-1>", eliminar_uno_del_carrito)
        carrito.bind("<Button-3>", modificar_cantidad_carrito)
        carrito.bind("<m>", modificar_cantidad_carrito)
        carrito.bind("<M>", modificar_cantidad_carrito)

        frame_botones_accion = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones_accion.pack(pady=10)

        tk.Button(frame_botones_accion, text="Finalizar Venta", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=finalizar_venta, width=20).grid(row=0, column=1, padx=10)

        tk.Button(frame_botones_accion, text="Generar Factura", bg="#28a745", fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=generar_factura, width=20).grid(row=0, column=0, padx=10)

        tk.Button(frame_botones_accion, text="Vaciar Carrito", bg="#ffc107", fg="black", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=vaciar_carrito, width=20).grid(row=0, column=2, padx=10)
        tk.Button(frame_botones_accion, text="Modificar Cantidad", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=modificar_cantidad_carrito, width=20).grid(row=0, column=3, padx=10)
        actualizar_lista()
        actualizar_carrito_display()

    def mostrar_buscar_venta(self):
        self.activar_boton(self.button_buscar_venta)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="BUSCAR VENTA", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=20)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

        panel_filtros = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_filtros.pack(pady=10)

        tk.Label(panel_filtros, text="Buscar (Fecha o NIT):", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0,column=0,padx=5)
        entry_fecha = tk.Entry(panel_filtros, width=20, bg="#E6F3FF", font=("Arial", 12))
        entry_fecha.grid(row=0, column=1, padx=5)

        def buscar_por_teclado(event):
            actualizar_lista(entry_fecha.get(), self.combo_mes_filtro.get())
        entry_fecha.bind("<KeyRelease>", buscar_por_teclado)

        tk.Label(panel_filtros, text="Filtrar por Mes:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=2,padx=(20, 5))
        meses = ["Todos", "01-Enero", "02-Febrero", "03-Marzo", "04-Abril","05-Mayo", "06-Junio", "07-Julio", "08-Agosto", "09-Septiembre","10-Octubre", "11-Noviembre", "12-Diciembre"]
        self.combo_mes_filtro = ttk.Combobox(panel_filtros, values=meses, width=15, style='Custom.TCombobox',state="readonly", font=("Arial", 12))
        self.combo_mes_filtro.current(0)
        self.combo_mes_filtro.grid(row=0, column=3, padx=5)

        def seleccionar_mes(event):
            actualizar_lista(entry_fecha.get(), self.combo_mes_filtro.get())
        self.combo_mes_filtro.bind("<<ComboboxSelected>>", seleccionar_mes)

        resumen_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        resumen_frame.pack(pady=5)
        COLOR_ENCABEZADO = "#E6F3FF"
        encabezado = tk.Frame(resumen_frame, bg=COLOR_ENCABEZADO)
        encabezado.pack(side="top", fill="x")

        tk.Label(encabezado, text="ID", font=("Arial", 11, "bold"), width=9, anchor="w", bg=COLOR_ENCABEZADO).pack(side="left")
        tk.Label(encabezado, text="FECHA Y HORA", font=("Arial", 11, "bold"), width=25, anchor="w",bg=COLOR_ENCABEZADO).pack(side="left")
        tk.Label(encabezado, text="NIT CLIENTE", font=("Arial", 11, "bold"), width=15, anchor="w",bg=COLOR_ENCABEZADO).pack(side="left")
        tk.Label(encabezado, text="TOTAL", font=("Arial", 11, "bold"), width=15, anchor="w", bg=COLOR_ENCABEZADO).pack(side="left")
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

        frame_total = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_total.pack(pady=5)

        tk.Label(frame_total, text="TOTAL Q.", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red").pack(side="left", padx=(10, 5))
        label_total = tk.Label(frame_total, text="0.00", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red")
        label_total.pack(side="left")

        def actualizar_lista(busqueda="", mes_filtro="Todos"):
            lista_resumen.delete(0, tk.END)
            with ProductosDB._conn() as conn:
                query = "SELECT id_venta, fecha_venta, total_venta, nit_cliente FROM ventas"
                conditions = []
                params = []

                if busqueda:
                    conditions.append("(fecha_venta LIKE ? OR nit_cliente LIKE ?)")
                    params.append('%' + busqueda + '%')
                    params.append('%' + busqueda + '%')

                if mes_filtro and mes_filtro != "Todos":
                    mes_num = mes_filtro.split('-')[0]
                    conditions.append("SUBSTR(fecha_venta, 4, 2) = ?")
                    params.append(mes_num)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += " ORDER BY fecha_venta DESC LIMIT 50"

                cur = conn.execute(query, tuple(params))

                for v in cur.fetchall():
                    nit_display = v['nit_cliente'] if v['nit_cliente'] else 'C/F'
                    lista_resumen.insert(tk.END,f"{v['id_venta']:<10} {v['fecha_venta']:<28} {nit_display:<16} Q.{v['total_venta']:<10.2f}")

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
                            lista_detalle.insert(tk.END, f"{cantidad:<35} {nombre:<35} Q.{precio_unidad:<10.2f}")
                        except ValueError:
                            lista_detalle.insert(tk.END, f"ERROR DE FORMATO: {item}")

                    label_total.config(text=f"{total_venta:.2f}")

        lista_resumen.bind("<<ListboxSelect>>", mostrar_detalle)
        actualizar_lista("", self.combo_mes_filtro.get())

    def mostrar_inventario(self):
        self.activar_boton(self.button_inventario)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="INVENTARIO DE PRODUCTOS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        panel_buttons = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buttons.pack(pady=0)

        button_agregar = tk.Button(panel_buttons, text="AGREGAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_agregar_producto)
        button_agregar.grid(row=0, column=0, padx=10)

        button_editar = tk.Button(panel_buttons, text="EDITAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_editar_producto)
        button_editar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(panel_buttons, text="ELIMINAR PRODUCTO", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_eliminar_producto)
        btn_eliminar.grid(row=0, column=2, padx=10, pady=5)

        btn_categorias = tk.Button(panel_buttons, text="CATEGORÍAS", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_categorias)
        btn_categorias.grid(row=0, column=3, padx=10, pady=5)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=20)

        panel_buscar = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buscar.pack(pady=10)

        frame_superior_busqueda = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_superior_busqueda.pack(pady=(0, 10), fill="x")

        frame_botones_superior = tk.Frame(frame_superior_busqueda, bg="#FFFFFF")
        frame_botones_superior.pack(side="left", padx=(100, 10), anchor="w")

        btn_busqueda_avanzada = tk.Button(frame_botones_superior, text="Búsqueda avanzada", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=18, height=1)
        btn_busqueda_avanzada.pack(pady=(0, 5))

        btn_ordenar = tk.Menubutton(frame_botones_superior, text="Métodos ordenamiento", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=20, height=1)
        btn_ordenar.pack()

        menu_ordenar = tk.Menu(btn_ordenar, tearoff=0)
        btn_ordenar.config(menu=menu_ordenar)

        menu_ordenar.add_command(label="1. Bubble Sort", command=lambda: self.aplicar_ordenamiento("Bubble Sort", ordenamiento_burbuja, lista_productos))
        menu_ordenar.add_command(label="2. Quick Sort", command=lambda: self.aplicar_ordenamiento("Quick Sort", ordenamiento_rapido, lista_productos))
        menu_ordenar.add_command(label="3. Selection Sort", command=lambda: self.aplicar_ordenamiento("Selection Sort", ordenamiento_seleccion, lista_productos))

        panel_buscar = tk.Frame(frame_superior_busqueda, bg="#FFFFFF")
        panel_buscar.pack(side="left", padx=10, anchor="w")

        tk.Label(panel_buscar,text="Buscar producto:",font=("Arial", 12, "bold"),bg="#FFFFFF").grid(row=0, column=0, padx=5)

        entry_buscar = tk.Entry(panel_buscar,width=50,bg="#E6F3FF",font=("Arial", 12))
        entry_buscar.grid(row=0, column=1, padx=5)

        contenedor_principal = tk.Frame(self.panel_right, bg="#FFFFFF")
        contenedor_principal.pack(pady=5, padx=100, fill="both")

        contenedor_lista = tk.Frame(contenedor_principal, bg="#FFFFFF")
        contenedor_lista.pack(fill="both", expand=True)

        lista_frame = tk.Frame(contenedor_lista, bg="#FFFFFF")
        lista_frame.pack(side="left", fill="both", expand=True)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack(fill="x")

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=12, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=25, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="CATEGORÍA", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="COMPRA", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="VENTA", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="STOCK", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(fill="both", expand=True, pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista_productos = tk.Listbox(frame_lista_scroll, width=90, height=10, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_productos.pack(side="left", fill="both", expand=True)
        scroll.config(command=lista_productos.yview)

        detalle_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        detalle_frame.pack(pady=10, padx=100)

        tk.Label(detalle_frame, text="INFORMACIÓN DETALLADA", font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)

        campos_detalle = tk.Frame(detalle_frame, bg="#FFFFFF")
        campos_detalle.pack(pady=10)

        tk.Label(campos_detalle, text="CÓDIGO:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0,sticky="w",padx=(0, 10), pady=5)
        codigo_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        codigo_label.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="NOMBRE:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0,sticky="w",padx=(0, 10), pady=5)
        nombre_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        nombre_label.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="CATEGORÍA:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0,sticky="w",padx=(0, 10), pady=5)
        categoria_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        categoria_label.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="COMPRA:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0,sticky="w",padx=(0, 10), pady=5)
        precio_compra_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        precio_compra_label.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="VENTA:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,sticky="w", padx=(0, 10),pady=5)
        precio_venta_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        precio_venta_label.grid(row=4, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="STOCK:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=5, column=0,sticky="w", padx=(0, 10),pady=5)
        stock_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        stock_label.grid(row=5, column=1, sticky="ew", pady=5)

        def buscar_producto_evento(event=None):
            valor = entry_buscar.get().strip()
            if not valor:
                messagebox.showwarning("Búsqueda", "Ingrese un código, nombre o categoría para buscar.")
                return
            with ProductosDB._conn() as conn:
                cur = conn.execute("""
                    SELECT codigo, nombre, categoria, precio_compra, precio_venta, cantidad
                    FROM productos
                    WHERE codigo LIKE ? OR nombre LIKE ? OR categoria LIKE ?
                    ORDER BY nombre
                """, (f"%{valor}%", f"%{valor}%", f"%{valor}%"))
                resultados = cur.fetchall()
            lista_productos.delete(0, tk.END)
            if resultados:
                for r in resultados:
                    if not isinstance(r, dict):
                        r = dict(r)
                    lista_productos.insert(tk.END,f"{r['codigo']:<13} {r['nombre']:<25} {r['categoria']:<16} "f"Q.{float(r['precio_compra']):<8.2f} Q.{float(r['precio_venta']):<8.2f} {float(r['cantidad']):<8.2f}")
                if len(resultados) == 1:
                    unico = resultados[0]
                    codigo_label.config(text=unico["codigo"])
                    nombre_label.config(text=unico["nombre"])
                    categoria_label.config(text=unico["categoria"])
                    precio_compra_label.config(text=f"Q.{float(unico['precio_compra']):.2f}")
                    precio_venta_label.config(text=f"Q.{float(unico['precio_venta']):.2f}")
                    stock_label.config(text=f"{float(unico['cantidad']):.2f}")

            else:
                messagebox.showwarning("Sin resultados", "No se encontraron productos que coincidan.")
                codigo_label.config(text="")
                nombre_label.config(text="")
                categoria_label.config(text="")
                precio_compra_label.config(text="")
                precio_venta_label.config(text="")
                stock_label.config(text="")

        def cargar_inventario_completo():
            try:
                productos_obj = ObtenerTodosProductos.obtener_todos()
                lista_productos.delete(0, tk.END)
                for p in productos_obj:
                    lista_productos.insert(tk.END,f"{p.codigo:<13} {p.nombre:<29} {p.categoria:<16} Q.{float(p.precio_compra):<9.2f} Q.{float(p.precio_venta):<9.2f} {float(p.cantidad):<8.2f}")
            except Exception as e:
                messagebox.showerror("Error de Carga", f"No se pudieron cargar los productos: {str(e)}")
        cargar_inventario_completo()

        def abrir_ventana_ordenamiento():
            ventana = tk.Toplevel(self)
            ventana.title("Métodos de Ordenamiento")
            ventana.geometry("600x500")
            ventana.configure(bg="#FFFFFF")
            ventana.transient(self)
            ventana.grab_set()

            ventana.update_idletasks()
            x = (ventana.winfo_screenwidth() // 2) - (600 // 2)
            y = (ventana.winfo_screenheight() // 2) - (500 // 2)
            ventana.geometry(f"600x500+{x}+{y}")

            tk.Label(ventana, text="MÉTODOS DE ORDENAMIENTO", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#007BFF").pack(pady=20)
            tk.Frame(ventana, bg="gray", height=2).pack(fill="x", padx=20, pady=10)

            info_label = tk.Label(ventana, text="Seleccione un método para ordenar el inventario alfabéticamente por nombre:",font=("Arial", 11), bg="#FFFFFF", wraplength=500, justify="center")
            info_label.pack(pady=10)

            botones_frame = tk.Frame(ventana, bg="#FFFFFF")
            botones_frame.pack(pady=20, padx=40, fill="both", expand=True)

            def aplicar_ordenamiento(metodo_nombre, metodo_funcion):
                try:
                    with ProductosDB._conn() as conn:
                        cur = conn.execute("SELECT * FROM productos")
                        productos_db = cur.fetchall()
                        if not productos_db:
                            messagebox.showinfo("Información","No hay productos en el inventario para ordenar.", parent=ventana)
                            return
                        lista_productos_obj = []
                        for p in productos_db:
                            producto = Productos(codigo=p['codigo'], nombre=p['nombre'], precio_venta=p['precio_venta'], precio_compra=p['precio_compra'], categoria=p['categoria'], cantidad=p['cantidad'])
                            lista_productos_obj.append(producto)
                        import time
                        inicio = time.time()
                        lista_ordenada = metodo_funcion(lista_productos_obj)
                        fin = time.time()
                        tiempo_transcurrido = (fin - inicio) * 1000
                        lista_productos.delete(0, tk.END)
                        for p in lista_ordenada:
                            lista_productos.insert(tk.END,f"{p.codigo:<13} {p.nombre:<29} {p.categoria:<16} Q.{float(p.precio_compra):<9.2f} Q.{float(p.precio_venta):<9.2f} {float(p.cantidad):<8.2f}")
                        ventana.destroy()
                        messagebox.showinfo("Ordenamiento Completado",f"Método: {metodo_nombre}\n\n" f"Productos ordenados: {len(lista_ordenada)}\n" f"Tiempo de ejecución: {tiempo_transcurrido:.2f} ms")
                except Exception as e:
                    messagebox.showerror("Error",f"Error al aplicar ordenamiento:\n{str(e)}", parent=ventana)
            frame_bubble = tk.LabelFrame(botones_frame, text="Bubble Sort (Burbuja)", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=15, pady=10)
            frame_bubble.pack(fill="x", pady=5)

            tk.Label(frame_bubble, text="Compara elementos adyacentes repetidamente.\nComplejidad: O(n²)", font=("Arial", 9), bg="#FFFFFF", fg="#666666").pack(pady=5)
            tk.Button(frame_bubble, text="APLICAR BUBBLE SORT", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=lambda: aplicar_ordenamiento("Bubble Sort", ordenamiento_burbuja), width=25).pack(pady=5)

            frame_selection = tk.LabelFrame(botones_frame, text="Selection Sort (Selección)", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=15, pady=10)
            frame_selection.pack(fill="x", pady=5)

            tk.Label(frame_selection, text="Busca el elemento mínimo y lo coloca al inicio.\nComplejidad: O(n²)", font=("Arial", 9), bg="#FFFFFF", fg="#666666").pack(pady=5)
            tk.Button(frame_selection, text="APLICAR SELECTION SORT", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=lambda: aplicar_ordenamiento("Selection Sort", ordenamiento_seleccion), width=25).pack(pady=5)

            frame_shell = tk.LabelFrame(botones_frame, text="Shell Sort", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=15, pady=10)
            frame_shell.pack(fill="x", pady=5)

            tk.Label(frame_shell, text="Mejora del insertion sort usando intervalos.\nComplejidad: O(n log n)", font=("Arial", 9), bg="#FFFFFF", fg="#666666").pack(pady=5)

            tk.Button(frame_shell, text="APLICAR SHELL SORT", bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=lambda: aplicar_ordenamiento("Shell Sort", ordenamiento_shell), width=25).pack(pady=5)
            frame_quick = tk.LabelFrame(botones_frame, text="Quick Sort (Rápido)", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=15, pady=10)
            frame_quick.pack(fill="x", pady=5)

            tk.Label(frame_quick, text="Divide y conquista usando pivote.\nComplejidad: O(n log n)", font=("Arial", 9), bg="#FFFFFF", fg="#666666").pack(pady=5)
            tk.Button(frame_quick, text="APLICAR QUICK SORT", bg="#28a745", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=lambda: aplicar_ordenamiento("Quick Sort", ordenamiento_rapido), width=25).pack(pady=5)

            frame_bogo = tk.LabelFrame(botones_frame, text="Bogo Sort (Aleatorio)", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=15, pady=10)
            frame_bogo.pack(fill="x", pady=5)

            tk.Button(ventana, text="CERRAR", bg="#6c757d", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", command=ventana.destroy, width=15).pack(pady=15)

        def actualizar_lista(event=None):
            cadena = entry_buscar.get()
            lista_productos.delete(0, tk.END)
            with ProductosDB._conn() as conn:
                if cadena:
                    patron = '%' + cadena + '%'
                    cur = conn.execute("SELECT codigo, nombre, categoria, precio_compra, precio_venta, cantidad FROM productos WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ? ORDER BY nombre",(patron, patron, patron))
                else:
                    cur = conn.execute("SELECT codigo, nombre, categoria, precio_compra, precio_venta, cantidad FROM productos ORDER BY nombre")
                for r in cur.fetchall():
                    lista_productos.insert(tk.END,f"{r['codigo']:<13} {r['nombre']:<29} {r['categoria']:<16} Q.{float(r['precio_compra']):<9.2f} Q.{float(r['precio_venta']):<9.2f} {float(r['cantidad']):<8.2f}")

        def mostrar_detalle(event):
            if not lista_productos.curselection():
                return

            indice = lista_productos.curselection()[0]
            seleccion = lista_productos.get(indice)
            codigo = seleccion[:14].strip()

            with ProductosDB._conn() as conn:
                cur = conn.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
                producto = cur.fetchone()

                if producto:
                    codigo_label.config(text=producto['codigo'])
                    nombre_label.config(text=producto['nombre'])
                    categoria_label.config(text=producto['categoria'])
                    precio_compra_label.config(text=f"Q. {producto['precio_compra']:.2f}")
                    precio_venta_label.config(text=f"Q. {producto['precio_venta']:.2f}")
                    stock_label.config(text=f"{producto['cantidad']:.2f} unidades")

        def mostrar_resultados_busqueda(resultados, tipo_busqueda):
            lista_productos.delete(0, tk.END)

            if resultados:
                for r in resultados:
                    precio_compra = float(r.get('precio_compra', r.get('precio', 0)))
                    lista_productos.insert(tk.END,f"{r['codigo']:<13} {r['nombre']:<29} {r['categoria']:<16} Q.{precio_compra:<9.2f} Q.{float(r['precio']):<9.2f} {float(r['cantidad']):<8.2f}")

                messagebox.showinfo("Búsqueda Completa",f"Búsqueda {tipo_busqueda} completada.\n"f"Se encontraron {len(resultados)} resultado(s).")
            else:
                messagebox.showwarning("Sin Resultados",f"La búsqueda {tipo_busqueda} no encontró resultados.")

        def abrir_ventana_busqueda():
            ventana = tk.Toplevel(self)
            ventana.title("Búsqueda Avanzada")
            ventana.geometry("500x400")
            ventana.configure(bg="#FFFFFF")
            ventana.transient(self)
            ventana.grab_set()

            ventana.update_idletasks()
            x = (ventana.winfo_screenwidth() // 2) - (500 // 2)
            y = (ventana.winfo_screenheight() // 2) - (500 // 2)
            ventana.geometry(f"500x500+{x}+{y}")

            tk.Label(ventana, text="BÚSQUEDA AVANZADA",font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#007BFF").pack(pady=20)

            tk.Frame(ventana, bg="gray", height=2).pack(fill="x", padx=20, pady=10)

            frame_secuencial = tk.LabelFrame(ventana, text="Búsqueda Secuencial",font=("Arial", 12, "bold"),bg="#FFFFFF", padx=20, pady=15)
            frame_secuencial.pack(pady=10, padx=20, fill="x")

            tk.Label(frame_secuencial, text="Buscar por:",font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            combo_criterio = ttk.Combobox(frame_secuencial,values=["nombre", "codigo", "categoria"],state="readonly", width=15, style='Custom.TCombobox')
            combo_criterio.current(0)
            combo_criterio.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            tk.Label(frame_secuencial, text="Valor:",font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            entry_valor_sec = tk.Entry(frame_secuencial, width=30, bg="#E6F3FF", font=("Arial", 10))
            entry_valor_sec.grid(row=1, column=1, padx=5, pady=5)
            entry_valor_sec.focus()

            def ejecutar_secuencial():
                criterio = combo_criterio.get()
                valor = entry_valor_sec.get().strip()

                if not valor:
                    messagebox.showerror("Error", "Ingrese un valor a buscar", parent=ventana)
                    return

                resultados = BusquedaAvanzada.busqueda_secuencial_db(criterio, valor)
                ventana.destroy()
                mostrar_resultados_busqueda(resultados, "Secuencial")

            tk.Button(frame_secuencial, text="BUSCAR SECUENCIAL", bg=self.COLOR_BOTON,fg="white", font=("Arial", 10, "bold"), relief="flat",cursor="hand2", command=ejecutar_secuencial, width=20).grid(row=2, column=0,columnspan=2, pady=15)

            frame_binaria = tk.LabelFrame(ventana, text="Búsqueda Binaria (Nombre Exacto)",font=("Arial", 12, "bold"),bg="#FFFFFF", padx=20, pady=15)
            frame_binaria.pack(pady=10, padx=20, fill="x")

            tk.Label(frame_binaria, text="Nombre exacto:",font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            entry_nombre_bin = tk.Entry(frame_binaria, width=30, bg="#E6F3FF", font=("Arial", 10))
            entry_nombre_bin.grid(row=0, column=1, padx=5, pady=5)

            def ejecutar_binaria():
                nombre = entry_nombre_bin.get().strip()

                if not nombre:
                    messagebox.showerror("Error", "Ingrese un nombre a buscar", parent=ventana)
                    return

                resultado = BusquedaAvanzada.busqueda_binaria_db(nombre)
                ventana.destroy()

                if resultado:
                    resultados = [resultado]
                else:
                    resultados = []

                mostrar_resultados_busqueda(resultados, "Binaria")

            tk.Button(frame_binaria, text="BUSCAR BINARIA", bg=self.COLOR_BOTON,fg="white", font=("Arial", 10, "bold"), relief="flat",cursor="hand2", command=ejecutar_binaria, width=20).grid(row=1, column=0,columnspan=2, pady=15)

            tk.Button(ventana, text="CANCELAR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2",command=ventana.destroy, width=15).pack(pady=10)

        btn_busqueda_avanzada.config(command=abrir_ventana_busqueda)

        entry_buscar.bind("<Return>", buscar_producto_evento)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_productos.bind("<<ListboxSelect>>", mostrar_detalle)
        actualizar_lista()

    def mostrar_proveedores(self):
        self.activar_boton(self.button_proveedores)
        self.limpiar_panel()

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

        panel_buscar = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buscar.pack(pady=10)

        tk.Label(panel_buscar, text="Buscar proveedor:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=5)
        entry_buscar = tk.Entry(panel_buscar, width=50, bg="#E6F3FF", font=("Arial", 12))
        entry_buscar.grid(row=0, column=1, padx=5)

        lista_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        lista_frame.pack(pady=5, padx=100)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack(fill="x")

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=25, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="TELÉFONO", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="UBICACIÓN", font=("Arial", 11, "bold"), width=20, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista_proveedores = tk.Listbox(frame_lista_scroll, width=80, height=10, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_proveedores.pack(side="left")
        scroll.config(command=lista_proveedores.yview)

        detalle_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        detalle_frame.pack(pady=10, padx=100)

        tk.Label(detalle_frame, text="INFORMACIÓN DETALLADA", font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)

        campos_detalle = tk.Frame(detalle_frame, bg="#FFFFFF")
        campos_detalle.pack(pady=10)

        tk.Label(campos_detalle, text="CÓDIGO:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0,sticky="w",padx=(0, 10), pady=5)
        codigo_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        codigo_label.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="NOMBRE:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0,sticky="w",padx=(0, 10), pady=5)
        nombre_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        nombre_label.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="TELÉFONO:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0,sticky="w",padx=(0, 10), pady=5)
        telefono_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        telefono_label.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="UBICACIÓN:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0,sticky="w",padx=(0, 10), pady=5)
        ubicacion_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        ubicacion_label.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="INFORMACIÓN:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,sticky="w",padx=(0, 10),pady=5)
        info_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        info_label.grid(row=4, column=1, sticky="ew", pady=5)

        def actualizar_lista(event=None):
            cadena = entry_buscar.get().strip()
            lista_proveedores.delete(0, tk.END)

            with ProductosDB._conn() as conn:
                if cadena:
                    patron = '%' + cadena + '%'
                    cur = conn.execute("SELECT codigo, nombre, telefono, ubicacion, informacion FROM proveedores WHERE nombre LIKE ? OR codigo LIKE ? OR telefono LIKE ? ORDER BY nombre",(patron, patron, patron))
                else:
                    cur = conn.execute("SELECT codigo, nombre, telefono, ubicacion, informacion FROM proveedores ORDER BY nombre")

                for r in cur.fetchall():
                    lista_proveedores.insert(tk.END,f"{r['codigo']:<17} {r['nombre']:<28} {r['telefono']:<17} {r['ubicacion']:<20}")

        def mostrar_detalle(event):
            if not lista_proveedores.curselection():
                return

            indice = lista_proveedores.curselection()[0]
            seleccion = lista_proveedores.get(indice)
            codigo = seleccion[:17].strip()

            with ProductosDB._conn() as conn:
                cur = conn.execute("SELECT * FROM proveedores WHERE codigo = ?", (codigo,))
                proveedor = cur.fetchone()

                if proveedor:
                    codigo_label.config(text=proveedor['codigo'])
                    nombre_label.config(text=proveedor['nombre'])
                    telefono_label.config(text=proveedor['telefono'])
                    ubicacion_label.config(text=proveedor['ubicacion'])
                    info_label.config(text=proveedor['informacion'])

        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_proveedores.bind("<<ListboxSelect>>", mostrar_detalle)

        actualizar_lista()

    def mostrar_reportes(self):
        self.activar_boton(self.button_reportes)
        self.limpiar_panel()
        tk.Label(self.panel_right, text="REPORTES DEL SISTEMA", font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=10)

        button_ver_reporte_cajera = tk.Button(frame_botones, text="VER REPORTES", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_ver_reportes)
        button_ver_reporte_cajera.grid(row=0, column=0, padx=10)

        button_ganancias = tk.Button(frame_botones, text="ECONOMIA", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_economia)
        button_ganancias.grid(row=0, column=1, padx=10)

        linea = tk.Frame(self.panel_right, bg="gray", height=2)
        linea.pack(fill="x", padx=0, pady=10)

    def mostrar_ver_reportes(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                widget.destroy()
            elif isinstance(widget, tk.Label) and widget.winfo_y() > 150:
                widget.destroy()

        contenido_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        contenido_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(contenido_frame, text="VER REPORTES DE CAJERAS", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        panel_filtros = tk.Frame(contenido_frame, bg="#FFFFFF")
        panel_filtros.pack(pady=10)

        tk.Label(panel_filtros, text="Buscar por fecha (dd-mm-yyyy):", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0, padx=5)
        entry_fecha = tk.Entry(panel_filtros, width=20, bg="#E6F3FF", font=("Arial", 12))
        entry_fecha.grid(row=0, column=1, padx=5)

        tk.Label(panel_filtros, text="Filtrar por Mes:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=2,padx=(20, 5))
        meses = ["Todos", "01-Enero", "02-Febrero", "03-Marzo", "04-Abril", "05-Mayo", "06-Junio","07-Julio", "08-Agosto", "09-Septiembre", "10-Octubre", "11-Noviembre", "12-Diciembre"]
        combo_mes_filtro = ttk.Combobox(panel_filtros, values=meses, width=15, style='Custom.TCombobox',state="readonly", font=("Arial", 12))
        combo_mes_filtro.current(0)
        combo_mes_filtro.grid(row=0, column=3, padx=5)

        lista_frame = tk.Frame(contenido_frame, bg="#FFFFFF")
        lista_frame.pack(pady=10, padx=50, fill="both")

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack(fill="x")

        tk.Label(encabezado, text="ID", font=("Arial", 11, "bold"), width=8, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="FECHA Y HORA", font=("Arial", 11, "bold"), width=25, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="REPORTE (Vista previa)", font=("Arial", 11, "bold"), width=70, anchor="w",bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame)
        frame_lista_scroll.pack(fill="both", pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista_reportes = tk.Listbox(frame_lista_scroll, width=120, height=8, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_reportes.pack(side="left", fill="both", expand=True)
        scroll.config(command=lista_reportes.yview)

        detalle_frame = tk.Frame(contenido_frame, bg="#FFFFFF")
        detalle_frame.pack(pady=10, padx=50, fill="both", expand=True)

        tk.Label(detalle_frame, text="DETALLE DEL REPORTE", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=5)

        text_frame = tk.Frame(detalle_frame, bg="#FFFFFF")
        text_frame.pack(pady=10, fill="both", expand=True)

        scroll_text = tk.Scrollbar(text_frame)
        scroll_text.pack(side="right", fill="y")

        text_reporte = tk.Text(text_frame, width=100, height=10, font=("Arial", 12), bg="#E6F3FF",relief="solid", borderwidth=2, yscrollcommand=scroll_text.set, wrap="word",state="disabled", padx=10, pady=10)
        text_reporte.pack(side="left", fill="both", expand=True)
        scroll_text.config(command=text_reporte.yview)

        def actualizar_lista(fecha_buscar="", mes_filtro="Todos"):
            lista_reportes.delete(0, tk.END)

            with ProductosDB._conn() as conn:
                query = "SELECT id, fecha, reporte FROM reportes_novedades"
                conditions = []
                params = []

                if fecha_buscar:
                    conditions.append("fecha LIKE ?")
                    params.append('%' + fecha_buscar + '%')

                if mes_filtro and mes_filtro != "Todos":
                    mes_num = mes_filtro.split('-')[0]
                    conditions.append("SUBSTR(fecha, 4, 2) = ?")
                    params.append(mes_num)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                query += " ORDER BY fecha DESC LIMIT 100"

                cur = conn.execute(query, tuple(params))

                for r in cur.fetchall():
                    reporte_truncado = r['reporte'][:80] + "..." if len(r['reporte']) > 80 else r['reporte']
                    lista_reportes.insert(tk.END, f"{r['id']:<9} {r['fecha']:<28} {reporte_truncado}")

        def mostrar_detalle_reporte(event):
            if not lista_reportes.curselection():
                return

            indice = lista_reportes.curselection()[0]
            seleccion = lista_reportes.get(indice)
            id_reporte = int(seleccion[:9].strip())

            with ProductosDB._conn() as conn:
                cur = conn.execute("SELECT reporte FROM reportes_novedades WHERE id = ?", (id_reporte,))
                reporte = cur.fetchone()

                if reporte:
                    # Actualizar solo el texto completo del reporte
                    text_reporte.config(state="normal")
                    text_reporte.delete("1.0", tk.END)
                    text_reporte.insert("1.0", reporte['reporte'])
                    text_reporte.config(state="disabled")

        def buscar_por_teclado(event):
            actualizar_lista(entry_fecha.get(), combo_mes_filtro.get())

        def seleccionar_mes(event):
            actualizar_lista(entry_fecha.get(), combo_mes_filtro.get())

        entry_fecha.bind("<KeyRelease>", buscar_por_teclado)
        combo_mes_filtro.bind("<<ComboboxSelected>>", seleccionar_mes)
        lista_reportes.bind("<<ListboxSelect>>", mostrar_detalle_reporte)

        frame_botones = tk.Frame(contenido_frame, bg="#FFFFFF")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="VOLVER", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=self.mostrar_reportes, width=20).pack()

        actualizar_lista()

        actualizar_lista()

    def mostrar_economia(self):
        for widget in self.panel_right.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 150:
                widget.destroy()
            elif isinstance(widget, tk.Label) and widget.winfo_y() > 150:
                widget.destroy()

        contenido_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        contenido_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(contenido_frame, text="ANÁLISIS ECONÓMICO", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        panel_filtro = tk.Frame(contenido_frame, bg="#FFFFFF")
        panel_filtro.pack(pady=20)

        tk.Label(panel_filtro, text="Seleccionar Mes:", font=("Arial", 14, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=10)

        meses = ["01-Enero", "02-Febrero", "03-Marzo", "04-Abril", "05-Mayo", "06-Junio","07-Julio", "08-Agosto", "09-Septiembre", "10-Octubre", "11-Noviembre", "12-Diciembre"]

        combo_mes = ttk.Combobox(panel_filtro, values=meses, width=20, style='Custom.TCombobox',state="readonly", font=("Arial", 12))
        fecha_actual = datetime.now()
        mes_actual = f"{fecha_actual.month:02d}"
        for i, mes in enumerate(meses):
            if mes.startswith(mes_actual):
                combo_mes.current(i)
                break
        combo_mes.grid(row=0, column=1, padx=10)

        tk.Label(panel_filtro, text="Año:", font=("Arial", 14, "bold"), bg="#FFFFFF").grid(row=0, column=2, padx=10)

        anio_actual = fecha_actual.year
        anios = [str(anio_actual - 1), str(anio_actual), str(anio_actual + 1)]
        combo_anio = ttk.Combobox(panel_filtro, values=anios, width=10, style='Custom.TCombobox',state="readonly", font=("Arial", 12))
        combo_anio.set(str(anio_actual))
        combo_anio.grid(row=0, column=3, padx=10)

        btn_calcular = tk.Button(panel_filtro, text="CALCULAR", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", width=15)
        btn_calcular.grid(row=0, column=4, padx=20)

        resultados_frame = tk.Frame(contenido_frame, bg="#FFFFFF")
        resultados_frame.pack(pady=30, padx=100, fill="both", expand=True)

        tk.Label(resultados_frame, text="RESUMEN ECONÓMICO", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        datos_frame = tk.Frame(resultados_frame, bg="#E6F3FF", relief="solid", borderwidth=2)
        datos_frame.pack(pady=20, padx=50, fill="x")

        tk.Label(datos_frame, text="INVERSIÓN TOTAL:", font=("Arial", 14, "bold"), bg="#E6F3FF").grid(row=0, column=0,sticky="w",padx=20, pady=15)
        label_inversion = tk.Label(datos_frame, text="Q. 0.00", font=("Arial", 14), bg="#E6F3FF", fg="#DC3545")
        label_inversion.grid(row=0, column=1, sticky="e", padx=20, pady=15)

        tk.Label(datos_frame, text="VENTAS TOTALES:", font=("Arial", 14, "bold"), bg="#E6F3FF").grid(row=1, column=0,sticky="w",padx=20, pady=15)
        label_ventas = tk.Label(datos_frame, text="Q. 0.00", font=("Arial", 14), bg="#E6F3FF", fg="#007BFF")
        label_ventas.grid(row=1, column=1, sticky="e", padx=20, pady=15)

        tk.Frame(datos_frame, bg="gray", height=2).grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        tk.Label(datos_frame, text="GANANCIA:", font=("Arial", 16, "bold"), bg="#E6F3FF").grid(row=3, column=0,sticky="w", padx=20,pady=15)
        label_ganancia = tk.Label(datos_frame, text="Q. 0.00", font=("Arial", 16, "bold"), bg="#E6F3FF", fg="#28a745")
        label_ganancia.grid(row=3, column=1, sticky="e", padx=20, pady=15)

        tk.Label(datos_frame, text="MARGEN DE GANANCIA:", font=("Arial", 14, "bold"), bg="#E6F3FF").grid(row=4,column=0,sticky="w",padx=20,pady=15)
        label_margen = tk.Label(datos_frame, text="0.00%", font=("Arial", 14), bg="#E6F3FF", fg="#6c757d")
        label_margen.grid(row=4, column=1, sticky="e", padx=20, pady=15)

        datos_frame.grid_columnconfigure(1, weight=1)

        def calcular_economia():
            mes_seleccionado = combo_mes.get().split('-')[0]
            anio_seleccionado = combo_anio.get()

            try:
                with ProductosDB._conn() as conn:
                    cur_ventas = conn.execute("""
                        SELECT v.detalle_productos, v.total_venta 
                        FROM ventas v
                        WHERE SUBSTR(v.fecha_venta, 4, 2) = ? 
                        AND SUBSTR(v.fecha_venta, 7, 4) = ?
                    """, (mes_seleccionado, anio_seleccionado))

                    ventas = cur_ventas.fetchall()

                    inversion_total = 0
                    ventas_total = 0

                    for venta in ventas:
                        ventas_total += venta['total_venta']

                        detalle_productos = venta['detalle_productos'].split(" | ")

                        for item in detalle_productos:
                            try:
                                cantidad_str, resto = item.split(" x ", 1)
                                cantidad = int(cantidad_str.strip())

                                nombre_producto = resto.split(" @Q.")[0].strip()

                                cur_producto = conn.execute("""
                                    SELECT precio_compra 
                                    FROM productos 
                                    WHERE nombre = ?
                                """, (nombre_producto,))

                                producto = cur_producto.fetchone()

                                if producto:
                                    inversion_total += cantidad * producto['precio_compra']

                            except (ValueError, IndexError):
                                continue

                    ganancia = ventas_total - inversion_total
                    margen = (ganancia / ventas_total * 100) if ventas_total > 0 else 0

                    label_inversion.config(text=f"Q. {inversion_total:,.2f}")
                    label_ventas.config(text=f"Q. {ventas_total:,.2f}")
                    label_ganancia.config(text=f"Q. {ganancia:,.2f}")
                    label_margen.config(text=f"{margen:.2f}%")

                    if ganancia < 0:
                        label_ganancia.config(fg="#DC3545")
                    else:
                        label_ganancia.config(fg="#28a745")

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular economía:\n{str(e)}")

        btn_calcular.config(command=calcular_economia)

        frame_botones = tk.Frame(contenido_frame, bg="#FFFFFF")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="VOLVER", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=self.mostrar_reportes, width=20).pack()

        calcular_economia()

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
        combo_categoria = ttk.Combobox(panel_form, width=38, font=("Arial", 12), state="readonly",style="Custom.TCombobox")
        combo_categoria.place(x=200, y=200, height=30)

        categorias = ObtenerCategorias.obtener_categorias()
        combo_categoria['values'] = categorias
        if categorias:
            combo_categoria.current(0)

        tk.Label(panel_form, text="CANTIDAD:", font=("Arial", 12, "bold"), bg="#FFFFFF").place(x=50, y=240)
        entry_cantidad = tk.Entry(panel_form, width=40, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_cantidad.place(x=200, y=240, height=25)

        def guardar_producto():
            nombre = entry_nombre.get().strip()
            codigo = entry_codigo.get().strip()
            precio_compra = entry_precio.get().strip()
            precio_venta = entry_precio_venta.get().strip()
            categoria = combo_categoria.get().strip()
            cantidad = entry_cantidad.get().strip()

            if not all([nombre, codigo, precio_compra, precio_venta, categoria, cantidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                precio_compra_float = float(precio_compra)
                precio_venta_float = float(precio_venta)
                cantidad_float = float(cantidad)
            except ValueError:
                messagebox.showerror("Error de Formato", "Los precios y la cantidad deben ser números válidos.")
                return
            if precio_compra_float <= 0 or precio_venta_float <= 0 or cantidad_float <= 0:
                messagebox.showerror("Error de Valor", "Los precios y la cantidad deben ser números **mayores a 0**.")
                return

            try:
                producto = Productos(codigo=codigo, nombre=nombre, precio_venta=precio_venta_float, precio_compra=precio_compra_float, categoria=categoria, cantidad=cantidad_float)
                GuardarProducto.guardar(producto)
                messagebox.showinfo("Éxito", f"Producto '{producto.nombre}' agregado correctamente.")
                entry_nombre.delete(0, tk.END)
                entry_codigo.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
                entry_precio_venta.delete(0, tk.END)
                combo_categoria.set('')
                entry_cantidad.delete(0, tk.END)
                entry_nombre.focus()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error de Código", "¡Error! El código ya está registrado. Ingrese uno nuevo.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el producto:\n{str(e)}")



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

        tk.Label(campos_frame, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0, padx=5,pady=5, sticky="e")
        entry_nombre = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="PRECIO COMPRA:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=1, column=0,padx=5, pady=5,sticky="e")
        entry_precio_compra = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_precio_compra.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="PRECIO VENTA:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=2, column=0,padx=5, pady=5,sticky="e")
        entry_precio_venta = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_precio_venta.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(campos_frame, text="CATEGORÍA:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=3, column=0,padx=5, pady=5,sticky="e")
        combo_categoria = ttk.Combobox(campos_frame, width=33, font=("Arial", 12), state="readonly")
        combo_categoria.grid(row=3, column=1, padx=5, pady=5)

        categorias = ObtenerCategorias.obtener_categorias()
        combo_categoria['values'] = categorias

        tk.Label(campos_frame, text="CANTIDAD:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=4, column=0, padx=5,pady=5, sticky="e")
        entry_cantidad = tk.Entry(campos_frame, width=35, bg="#E6F3FF", relief="flat", font=("Arial", 12))
        entry_cantidad.grid(row=4, column=1, padx=5, pady=5)

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
            categoria_actual = producto["categoria"]
            if categoria_actual in combo_categoria['values']:
                combo_categoria.set(categoria_actual)
            else:
                combo_categoria.set('')
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
            nueva_categoria = combo_categoria.get().strip()
            nueva_cantidad = entry_cantidad.get().strip()

            if not all([nuevo_nombre, nuevo_precio_compra, nuevo_precio_venta, nueva_categoria, nueva_cantidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                precio_compra_float = float(nuevo_precio_compra)
                precio_venta_float = float(nuevo_precio_venta)
                cantidad_float = float(nueva_cantidad)
                if precio_compra_float <= 0 or precio_venta_float <= 0 or cantidad_float <= 0:
                    messagebox.showerror("Error","El precio de compra, precio de venta y la cantidad deben ser números mayores a 0.")
                    return

                ModificarProducto.modificar_producto(codigo=self.codigo_actual_edicion, nombre=nuevo_nombre,precio_compra=precio_compra_float, precio_venta=precio_venta_float,categoria=nueva_categoria, cantidad=cantidad_float)

                messagebox.showinfo("Éxito", f"Producto '{nuevo_nombre}' actualizado correctamente.")
                entry_nombre.delete(0, tk.END)
                entry_precio_compra.delete(0, tk.END)
                entry_precio_venta.delete(0, tk.END)
                combo_categoria.set('')
                entry_cantidad.delete(0, tk.END)
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

            if not telefono.isdigit():
                messagebox.showerror("Error de Formato", "El campo Teléfono solo debe contener números (dígitos).")
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

            except sqlite3.IntegrityError as e:
                error_msg = str(e).lower()

                if 'proveedores.codigo' in error_msg or 'unique constraint' in error_msg and 'codigo' in error_msg:
                    messagebox.showerror("Error de Código","¡Error! El código del proveedor ya está registrado en la base de datos. Debe ser único.")
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

            if not nuevo_telefono.isdigit():
                messagebox.showerror("Error de Formato", "El campo Teléfono solo debe contener números (dígitos).")
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

    def mostrar_busqueda_avanzada(self):
        ventana = tk.Toplevel(self)
        ventana.title("Búsqueda Avanzada")
        ventana.geometry("600x500")
        ventana.configure(bg="#FFFFFF")
        ventana.transient(self)
        ventana.grab_set()

        tk.Label(ventana, text="BÚSQUEDA AVANZADA", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=20)

        frame_secuencial = tk.LabelFrame(ventana, text="Búsqueda Secuencial", font=("Arial", 12, "bold"), bg="#FFFFFF",padx=20, pady=20)
        frame_secuencial.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_secuencial, text="Criterio:", font=("Arial", 10), bg="#FFFFFF").grid(row=0, column=0, padx=5,pady=5)
        combo_criterio = ttk.Combobox(frame_secuencial, values=["nombre", "codigo", "categoria"], state="readonly",width=15)
        combo_criterio.current(0)
        combo_criterio.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_secuencial, text="Valor:", font=("Arial", 10), bg="#FFFFFF").grid(row=1, column=0, padx=5,pady=5)
        entry_valor_sec = tk.Entry(frame_secuencial, width=30, bg="#E6F3FF")
        entry_valor_sec.grid(row=1, column=1, padx=5, pady=5)

        resultado_sec = tk.Label(frame_secuencial, text="", font=("Arial", 9), bg="#FFFFFF", wraplength=400,justify="left")
        resultado_sec.grid(row=3, column=0, columnspan=2, pady=10)

        def ejecutar_secuencial():
            criterio = combo_criterio.get()
            valor = entry_valor_sec.get().strip()

            if not valor:
                messagebox.showerror("Error", "Ingrese un valor a buscar")
                return

            resultados = BusquedaAvanzada.busqueda_secuencial_db(criterio, valor)

            if resultados:
                texto = f"Se encontraron {len(resultados)} resultado(s):\n\n"
                for r in resultados[:5]:  # Mostrar máximo 5
                    texto += f"• {r['nombre']} ({r['codigo']})\n"
                if len(resultados) > 5:
                    texto += f"\n... y {len(resultados) - 5} más"
            else:
                texto = "No se encontraron resultados"

            resultado_sec.config(text=texto, fg="#28a745" if resultados else "#DC3545")

        tk.Button(frame_secuencial, text="BUSCAR", bg=self.COLOR_BOTON, fg="white", font=("Arial", 10, "bold"),command=ejecutar_secuencial).grid(row=2, column=0, columnspan=2, pady=10)

        frame_binaria = tk.LabelFrame(ventana, text="Búsqueda Binaria (Nombre Exacto)", font=("Arial", 12, "bold"),bg="#FFFFFF", padx=20, pady=20)
        frame_binaria.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_binaria, text="Nombre exacto:", font=("Arial", 10), bg="#FFFFFF").grid(row=0, column=0, padx=5,pady=5)
        entry_nombre_bin = tk.Entry(frame_binaria, width=30, bg="#E6F3FF")
        entry_nombre_bin.grid(row=0, column=1, padx=5, pady=5)

        resultado_bin = tk.Label(frame_binaria, text="", font=("Arial", 9), bg="#FFFFFF", wraplength=400,justify="left")
        resultado_bin.grid(row=2, column=0, columnspan=2, pady=10)

        def ejecutar_binaria():
            nombre = entry_nombre_bin.get().strip()

            if not nombre:
                messagebox.showerror("Error", "Ingrese un nombre a buscar")
                return

            resultado = BusquedaAvanzada.busqueda_binaria_db(nombre)

            if resultado:
                texto = (f"✓ Producto encontrado:\n\n"
                         f"Nombre: {resultado['nombre']}\n"
                         f"Código: {resultado['codigo']}\n"
                         f"Categoría: {resultado['categoria']}\n"
                         f"Precio: Q.{resultado['precio']:.2f}\n"
                         f"Stock: {resultado['cantidad']:.2f}")
                color = "#28a745"
            else:
                texto = "✗ Producto no encontrado"
                color = "#DC3545"

            resultado_bin.config(text=texto, fg=color)

        tk.Button(frame_binaria, text="BUSCAR", bg=self.COLOR_BOTON, fg="white", font=("Arial", 10, "bold"),command=ejecutar_binaria).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(ventana, text="CERRAR", bg="#6c757d", fg="white", font=("Arial", 10, "bold"),command=ventana.destroy).pack(pady=20)

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


class AppCajera(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniMarket - CAJERA")
        self.geometry("1200x600")
        self.resizable(True, True)
        self.configure(bg="#FFFFFF")
        self.COLOR_FONDO = "#1E90FF"
        self.COLOR_BOTON = "#007BFF"
        self.COLOR_SELECCION = "#0056b3"
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)
        self.state('zoomed')
        self.carrito_items = []
        self.auth_eliminar_carrito = False

        self.panel_left = tk.Frame(self, bg="#1E90FF", width=200, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.panel_right = tk.Frame(self, bg="#FFFFFF")
        self.panel_right.pack(side="right", fill="both", expand=True)

        self.imagen = tk.PhotoImage(file="2.png")
        self.label_logo = tk.Label(self.panel_left, image=self.imagen, bg="#1E90FF")
        self.label_logo.place(x=10, y=20)
        self.label_logo.bind("<Button-1>", self.mostrar_menu_principal)

        self.button_ventas = tk.Button(self.panel_left, text="VENTAS", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_ventas)
        self.button_ventas.place(x=0, y=220, height=35)

        self.button_inventario = tk.Button(self.panel_left, text="INVENTARIO", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_inventario)
        self.button_inventario.place(x=0, y=290, height=35)

        self.button_reportes = tk.Button(self.panel_left, text="REPORTES", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_crear_reporte)
        self.button_reportes.place(x=0, y=360, height=35)

        self.button_acerca_de = tk.Button(self.panel_left, text="ACERCA DE", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.mostrar_acerca_de)
        self.button_acerca_de.place(x=0, y=660, height=35)

        self.button_close = tk.Button(self.panel_left, text="CERRAR SESIÓN", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.cerrar_sesion)
        self.button_close.place(x=0, y=550, height=35)

        self.botones = [self.button_ventas, self.button_inventario, self.button_reportes, self.button_acerca_de]

        self.mostrar_menu_principal()

    def aplicar_ordenamiento(self, metodo, funcion_ordenamiento, lista_productos):
        try:
            productos_obj = ObtenerTodosProductos.obtener_todos()
            if not productos_obj:
                messagebox.showwarning("Aviso", "No hay productos para ordenar.")
                return
            lista_ordenada = funcion_ordenamiento(productos_obj)
            lista_productos.delete(0, tk.END)
            for p in lista_ordenada:
                lista_productos.insert(tk.END, f"{p.codigo:<17} {p.nombre:<33} {p.categoria:<17} Q.{float(p.precio_venta):<9.2f} {float(p.cantidad):<10.2f}")
            messagebox.showinfo("Ordenamiento", f"Productos ordenados usando {metodo}.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al ordenar:\n{e}")

    def mostrar_acerca_de(self):
        self.activar_boton(self.button_acerca_de)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="ACERCA DE - SISTEMA MINIMARKET", font=("Arial", 20, "bold"), bg="#FFFFFF",fg="#007BFF").pack(pady=30)

        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=50, pady=10)

        info_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        info_frame.pack(pady=20, padx=50)

        tk.Label(info_frame, text="Versión: 1.0.0", font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=10)

        tk.Label(info_frame, text="Sistema de Gestión para MiniMarket", font=("Arial", 12), bg="#FFFFFF",fg="#666666").pack(pady=5)

        tk.Frame(self.panel_right, bg="gray", height=1).pack(fill="x", padx=50, pady=20)

        tk.Label(self.panel_right, text="DESARROLLADO POR:", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=15)

        dev_frame = tk.Frame(self.panel_right, bg="#E6F3FF", relief="solid", borderwidth=2)
        dev_frame.pack(pady=10, padx=100, fill="x")

        tk.Label(dev_frame, text="MAYNOR EDUARDO MORALES CHANG", font=("Arial", 13, "bold"), bg="#E6F3FF",pady=10).pack()
        tk.Label(dev_frame, text="Teléfono: 3570-6701", font=("Arial", 12), bg="#E6F3FF", pady=5).pack()

        tk.Frame(dev_frame, bg="gray", height=1).pack(fill="x", padx=20, pady=10)

        tk.Label(dev_frame, text="CRISTHIAN ESTUARDO DE LEÓN PEREZ", font=("Arial", 13, "bold"), bg="#E6F3FF",pady=10).pack()
        tk.Label(dev_frame, text="Teléfono: 5080-8254", font=("Arial", 12), bg="#E6F3FF", pady=5).pack(pady=(0, 10))

        tk.Label(self.panel_right, text="© 2025 - Todos los derechos reservados", font=("Arial", 10), bg="#FFFFFF",fg="#999999").pack(pady=30)


    def activar_boton(self, boton):
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)
        boton.config(bg=self.COLOR_SELECCION)

    def limpiar_panel(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self, event=None):
        self.limpiar_panel()
        tk.Label(self.panel_right, text="MENÚ PRINCIPAL - CAJERA", font=("Arial", 22, "bold"), bg="#FFFFFF").pack(pady=50)
        tk.Label(self.panel_right, text="¡Bienvenido al MiniMarket!", font=("Arial", 16), bg="#FFFFFF").pack(pady=20)

        frame_ofertas = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_ofertas.pack(pady=20)

        try:
            imagen_ofertas = tk.PhotoImage(file="ofertas.png")
            self.imagen_ofertas = imagen_ofertas

            imagen_ofertas2 = tk.PhotoImage(file="oferta2.png")
            self.imagen_ofertas2 = imagen_ofertas2

            label_ofertas = tk.Label(frame_ofertas, image=imagen_ofertas, bg="#FFFFFF", cursor="hand2", relief="raised",borderwidth=2)
            label_ofertas.pack(side="left", padx=10)

            label_ofertas = tk.Label(frame_ofertas, image=imagen_ofertas2, bg="#FFFFFF", cursor="hand2",relief="raised", borderwidth=2)
            label_ofertas.pack(side="left", padx=10)

        except Exception as e:
            tk.Label(frame_ofertas, text="Imagen de ofertas no disponible", font=("Arial", 12), bg="#FFE6E6",fg="#DC3545", padx=20, pady=10).pack()
        for b in self.botones:
            b.config(bg=self.COLOR_BOTON)

    def mostrar_ventas(self):
        self.activar_boton(self.button_ventas)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="SECCIÓN DE VENTAS", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=20)
        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=0, pady=20)

        panel_buscar = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buscar.pack(pady=10)
        tk.Label(panel_buscar, text="Buscar producto:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,
                                                                                                       padx=5)
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

        tk.Label(frame_total, text="TOTAL Q.", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red").pack(side="left", padx=(10, 5))
        label_total = tk.Label(frame_total, text="0.00", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="Red")
        label_total.pack(side="left")


        def actualizar_carrito_display():
            carrito.delete(0, tk.END)
            total = 0
            for item in self.carrito_items:
                subtotal = item["cantidad"] * item["precio"]
                total += subtotal
                carrito.insert(tk.END,
                               f"{item['cantidad']:<11} {item['nombre']:<34} Q.{item['precio']:<9.2f} Q.{subtotal:<8.2f}")
            subtotal_var.set(total)
            label_total.config(text=f"{total:.2f}")

        def solicitar_autorizacion():
            if self.auth_eliminar_carrito:
                return True

            codigo = simpledialog.askstring("Autorización requerida","Ingrese el código de autorización para eliminar productos del carrito:",show='*')

            if codigo == "A1B2C3":
                self.auth_eliminar_carrito = True
                messagebox.showinfo("Autorizado", "Autorización concedida. Ahora puede eliminar productos del carrito.")
                return True
            elif codigo is not None:
                messagebox.showerror("Error", "Código incorrecto. Autorización denegada.")

            return False

        def modificar_cantidad_carrito(event=None):
            if not carrito.curselection():
                messagebox.showwarning("Advertencia", "Seleccione un producto del carrito para modificar su cantidad.")
                return
            indice = int(carrito.curselection()[0])
            if indice >= len(self.carrito_items):
                return
            item_seleccionado = self.carrito_items[indice]
            producto = ObtenerCodigo.obtener_por_codigo(item_seleccionado["codigo"])
            if not producto:
                messagebox.showerror("Error", "No se encontró el producto en la base de datos.")
                return
            stock_disponible = producto["cantidad"]
            cantidad_actual = item_seleccionado["cantidad"]
            nueva_cantidad_str = simpledialog.askstring("Modificar Cantidad",f"Producto: {item_seleccionado['nombre']}\n" f"Cantidad actual: {cantidad_actual}\n" f"Stock disponible: {stock_disponible}\n\n" f"Ingrese la nueva cantidad:")
            if nueva_cantidad_str is None:
                return
            try:
                nueva_cantidad = float(nueva_cantidad_str)
                if nueva_cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                    return
                if nueva_cantidad > stock_disponible:
                    messagebox.showerror("Stock Insuficiente",f"No hay suficiente stock disponible.\n\n" f"Stock disponible: {stock_disponible}\n" f"Cantidad solicitada: {nueva_cantidad}")
                    return
                item_seleccionado["cantidad"] = int(nueva_cantidad)
                actualizar_carrito_display()
                messagebox.showinfo("Éxito", f"Cantidad actualizada a {int(nueva_cantidad)} unidades.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido.")

        def eliminar_uno_del_carrito(event=None):
            if not carrito.curselection():
                return

            if not solicitar_autorizacion():
                return

            indice = int(carrito.curselection()[0])

            if indice >= len(self.carrito_items):
                return

            item_seleccionado = self.carrito_items[indice]

            if "cantidad" not in item_seleccionado:
                messagebox.showerror("Error", "Estructura de datos inválida")
                return

            item_seleccionado["cantidad"] -= 1

            if item_seleccionado["cantidad"] <= 0:
                self.carrito_items.pop(indice)

            actualizar_carrito_display()

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
            cantidad_en_carrito = sum(item["cantidad"] for item in self.carrito_items if item["codigo"] == codigo)

            if cantidad_en_carrito >= stock_disponible:
                messagebox.showerror("Stock Agotado", f"No hay más stock de {producto['nombre']}.")
                return

            for item in self.carrito_items:
                if item["codigo"] == producto["codigo"]:
                    item["cantidad"] += 1
                    break
            else:
                self.carrito_items.append({
                    "codigo": producto["codigo"],
                    "nombre": producto["nombre"],
                    "precio": float(producto["precio_venta"]),
                    "cantidad": 1
                })

            actualizar_carrito_display()

        def vaciar_carrito():
            if not self.carrito_items:
                messagebox.showwarning("Advertencia", "El carrito ya está vacío.")
                return

            if not solicitar_autorizacion():
                return

            confirmar = messagebox.askyesno(
                "Confirmar acción",
                f"¿Está seguro de que desea vaciar el carrito?\n\n"
                f"Se eliminarán {len(self.carrito_items)} producto(s)."
            )

            if confirmar:
                self.carrito_items.clear()
                actualizar_carrito_display()
                messagebox.showinfo("Éxito", "El carrito ha sido vaciado.")

        def finalizar_venta():
            if not self.carrito_items:
                messagebox.showerror("Error", "El carrito está vacío.")
                return

            try:
                ClientesDB.guardar_cliente("C/F", "Consumidor Final", "Ciudad")
            except:
                pass

            total = subtotal_var.get()
            detalle = [f"{i['cantidad']} x {i['nombre']} @Q.{i['precio']}" for i in self.carrito_items]
            RegistrarVenta.registrar_venta(total, detalle, "C/F")

            for item in self.carrito_items:
                ActualizarStock.actualizar_stock(item['codigo'], item['cantidad'])

            messagebox.showinfo("Éxito",f"✓ Venta registrada (Cliente: C/F)\n✓ Stock actualizado\n\nTotal: Q.{total:.2f}")
            self.carrito_items.clear()
            actualizar_carrito_display()
            carrito.delete(0, tk.END)
            subtotal_var.set(0.0)

            self.auth_eliminar_carrito = False

        def generar_factura():
            if not self.carrito_items:
                messagebox.showerror("Error", "El carrito está vacío. Agregue productos antes de generar la factura.")
                return

            ventana_factura = tk.Toplevel(self)
            ventana_factura.title("Generar Factura")
            ventana_factura.geometry("500x400")
            ventana_factura.configure(bg="#FFFFFF")
            ventana_factura.resizable(False, False)
            ventana_factura.transient(self)
            ventana_factura.grab_set()

            ventana_factura.update_idletasks()
            x = (ventana_factura.winfo_screenwidth() // 2) - (500 // 2)
            y = (ventana_factura.winfo_screenheight() // 2) - (400 // 2)
            ventana_factura.geometry(f"500x400+{x}+{y}")

            tk.Label(ventana_factura, text="DATOS DEL CLIENTE", font=("Arial", 18, "bold"), bg="#FFFFFF",fg="#007BFF").pack(pady=20)

            tk.Frame(ventana_factura, bg="gray", height=2).pack(fill="x", padx=20, pady=10)

            campos_frame = tk.Frame(ventana_factura, bg="#FFFFFF")
            campos_frame.pack(pady=20, padx=40)

            tk.Label(campos_frame, text="NIT:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,sticky="e", padx=10,pady=15)
            entry_nit = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_nit.grid(row=0, column=1, pady=15)
            entry_nit.focus()

            tk.Label(campos_frame, text="NOMBRE:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=1, column=0,sticky="e", padx=10,pady=15)
            entry_nombre = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_nombre.grid(row=1, column=1, pady=15)

            tk.Label(campos_frame, text="DIRECCIÓN:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=2, column=0,sticky="e",padx=10, pady=15)
            entry_direccion = tk.Entry(campos_frame, width=30, bg="#E6F3FF", relief="flat", font=("Arial", 11))
            entry_direccion.grid(row=2, column=1, pady=15)

            def autocompletar_cliente(event=None):
                nit = entry_nit.get().strip()
                if len(nit) >= 3:
                    cliente = ClientesDB.buscar_por_nit(nit)
                    if cliente:
                        entry_nombre.delete(0, tk.END)
                        entry_nombre.insert(0, cliente['nombre'])
                        entry_direccion.delete(0, tk.END)
                        entry_direccion.insert(0, cliente['direccion'])
                        entry_nombre.config(bg="#E6F3FF")
                        entry_direccion.config(bg="#E6F3FF")
                    else:
                        entry_nombre.delete(0, tk.END)
                        entry_direccion.delete(0, tk.END)
                        entry_nombre.config(bg="#E6F3FF")
                        entry_direccion.config(bg="#E6F3FF")
                else:
                    entry_nombre.delete(0, tk.END)
                    entry_direccion.delete(0, tk.END)
                    entry_nombre.config(bg="#E6F3FF")
                    entry_direccion.config(bg="#E6F3FF")

            entry_nit.bind("<KeyRelease>", autocompletar_cliente)

            botones_frame = tk.Frame(ventana_factura, bg="#FFFFFF")
            botones_frame.pack(pady=20)

            def procesar_factura():
                nit = entry_nit.get().strip()
                nombre = entry_nombre.get().strip()
                direccion = entry_direccion.get().strip()

                if not nit or not nombre or not direccion:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.",parent=ventana_factura)
                    return

                try:
                    ClientesDB.guardar_cliente(nit, nombre, direccion)

                    total = subtotal_var.get()
                    archivo_pdf = GeneradorFacturas.generar_factura_pdf(self.carrito_items, total, nit, nombre, direccion)

                    detalle = [f"{i['cantidad']} x {i['nombre']} @Q.{i['precio']}" for i in self.carrito_items]
                    RegistrarVenta.registrar_venta(total, detalle, nit)

                    for item in self.carrito_items:
                        ActualizarStock.actualizar_stock(item['codigo'], item['cantidad'])

                    ventana_factura.destroy()

                    self.carrito_items.clear()
                    actualizar_carrito_display()
                    self.auth_eliminar_carrito = False

                    respuesta = messagebox.askyesno(
                        "Venta Completada",
                        f"✓ Venta registrada correctamente\n"
                        f"✓ Factura generada: {archivo_pdf}\n"
                        f"✓ Cliente guardado: {nombre}\n"
                        f"✓ Stock actualizado\n\n"
                        f"Total: Q.{total:.2f}\n\n"
                        f"¿Desea abrir la factura ahora?"
                    )

                    if respuesta:
                        import subprocess
                        import platform

                        if platform.system() == 'Windows':
                            os.startfile(archivo_pdf)
                        elif platform.system() == 'Darwin':
                            subprocess.call(['open', archivo_pdf])
                        else:
                            subprocess.call(['xdg-open', archivo_pdf])

                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar la venta:\n{str(e)}",parent=ventana_factura)

            tk.Button(botones_frame, text="GENERAR FACTURA", bg="#007BFF", fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=procesar_factura, width=20).grid(row=0, column=0, padx=10)

            tk.Button(botones_frame, text="CANCELAR", bg="#6c757d", fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=ventana_factura.destroy, width=15).grid(row=0, column=1,padx=10)

        def agregar_enter(event):
            actualizar_lista()
            if lista_productos.size() > 0:
                lista_productos.selection_clear(0, tk.END)
                lista_productos.select_set(0)
                lista_productos.activate(0)
                agregar_al_carrito()
                entry_buscar.delete(0, tk.END)
                actualizar_lista()

        entry_buscar.bind("<Return>", agregar_enter)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_productos.bind("<Double-Button-1>", agregar_al_carrito)
        carrito.bind("<Double-Button-1>", eliminar_uno_del_carrito)
        carrito.bind("<Button-3>", modificar_cantidad_carrito)
        carrito.bind("<m>", modificar_cantidad_carrito)
        carrito.bind("<M>", modificar_cantidad_carrito)

        frame_botones_accion = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones_accion.pack(pady=10)
        tk.Button(frame_botones_accion, text="Finalizar Venta", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2", command=finalizar_venta, width=20).grid(row=0, column=1, padx=10)
        tk.Button(frame_botones_accion, text="Generar Factura", bg="#28a745", fg="white", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=generar_factura, width=20).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones_accion, text="Vaciar Carrito", bg="#ffc107", fg="black", font=("Arial", 12, "bold"),relief="flat", cursor="hand2", command=vaciar_carrito, width=20).grid(row=0, column=2, padx=10)
        tk.Button(frame_botones_accion, text="Modificar Cantidad", bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat", cursor="hand2",command=modificar_cantidad_carrito, width=20).grid(row=0, column=3, padx=10)
        actualizar_lista()
        actualizar_carrito_display()

    def mostrar_inventario(self):
        self.activar_boton(self.button_inventario)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="CONSULTA DE INVENTARIO", font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)
        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=0, pady=20)

        panel_buscar = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_buscar.pack(pady=10)

        frame_superior_busqueda = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_superior_busqueda.pack(pady=(0, 10), fill="x")

        frame_boton_busqueda = tk.Frame(frame_superior_busqueda, bg="#FFFFFF")
        frame_boton_busqueda.pack(side="left", padx=(100, 10), anchor="w")

        btn_busqueda_avanzada = tk.Button(frame_boton_busqueda, text="Búsqueda avanzada", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=18, height=1)
        btn_busqueda_avanzada.pack()
        btn_busqueda_avanzada.config(command=self.abrir_busqueda_avanzada_cajera)

        panel_buscar = tk.Frame(frame_superior_busqueda, bg="#FFFFFF")
        panel_buscar.pack(side="left", padx=10, anchor="w")

        tk.Label(panel_buscar, text="Buscar producto:", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=5)

        entry_buscar = tk.Entry(panel_buscar, width=50, bg="#E6F3FF", font=("Arial", 12))
        entry_buscar.grid(row=0, column=1, padx=5)

        contenedor_principal = tk.Frame(self.panel_right, bg="#FFFFFF")
        contenedor_principal.pack(pady=5, padx=100, fill="both")

        contenedor_lista = tk.Frame(contenedor_principal, bg="#FFFFFF")
        contenedor_lista.pack(fill="both", expand=True)

        lista_frame = tk.Frame(contenedor_lista, bg="#FFFFFF")
        lista_frame.pack(side="left", fill="both", expand=True)

        lista_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        lista_frame.pack(pady=5, padx=100)

        encabezado = tk.Frame(lista_frame, bg="#E6F3FF")
        encabezado.pack(fill="x")

        tk.Label(encabezado, text="CÓDIGO", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="NOMBRE", font=("Arial", 11, "bold"), width=30, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="CATEGORÍA", font=("Arial", 11, "bold"), width=15, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="PRECIO", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")
        tk.Label(encabezado, text="STOCK", font=("Arial", 11, "bold"), width=10, anchor="w", bg="#E6F3FF").pack(side="left")

        frame_lista_scroll = tk.Frame(lista_frame, bg="#FFFFFF")
        frame_lista_scroll.pack(pady=5)

        scroll = tk.Scrollbar(frame_lista_scroll)
        scroll.pack(side="right", fill="y")

        lista_productos = tk.Listbox(frame_lista_scroll, width=100, height=10, font=("Courier New", 10),yscrollcommand=scroll.set)
        lista_productos.pack(side="left")
        scroll.config(command=lista_productos.yview)

        detalle_frame = tk.Frame(self.panel_right, bg="#FFFFFF")
        detalle_frame.pack(pady=10, padx=100)

        tk.Label(detalle_frame, text="INFORMACIÓN DETALLADA", font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)

        campos_detalle = tk.Frame(detalle_frame, bg="#FFFFFF")
        campos_detalle.pack(pady=10)

        tk.Label(campos_detalle, text="CÓDIGO:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=0, column=0,sticky="w",padx=(0, 10), pady=5)
        codigo_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        codigo_label.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="NOMBRE:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=1, column=0,sticky="w",padx=(0, 10), pady=5)
        nombre_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        nombre_label.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="CATEGORÍA:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=2, column=0,sticky="w",padx=(0, 10), pady=5)
        categoria_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        categoria_label.grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="PRECIO VENTA:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=3, column=0,sticky="w",padx=(0, 10),pady=5)
        precio_venta_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        precio_venta_label.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(campos_detalle, text="STOCK:", font=("Arial", 11, "bold"), bg="#FFFFFF").grid(row=4, column=0,sticky="w", padx=(0, 10),pady=5)
        stock_label = tk.Label(campos_detalle, text="", font=("Arial", 11), bg="#E6F3FF", anchor="w", width=50,relief="flat")
        stock_label.grid(row=4, column=1, sticky="ew", pady=5)

        frame_botones_superior = tk.Frame(frame_superior_busqueda, bg="#FFFFFF")
        frame_botones_superior.pack(side="left", padx=(100, 10), anchor="w")

        btn_ordenar = tk.Menubutton(frame_botones_superior, text="Métodos ordenamiento", bg="#007BFF", fg="white", font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=20, height=1)
        btn_ordenar.pack()

        menu_ordenar = tk.Menu(btn_ordenar, tearoff=0)
        btn_ordenar.config(menu=menu_ordenar)

        menu_ordenar.add_command(label="1. Bubble Sort", command=lambda: self.aplicar_ordenamiento("Bubble Sort", ordenamiento_burbuja, lista_productos))
        menu_ordenar.add_command(label="2. Quick Sort", command=lambda: self.aplicar_ordenamiento("Quick Sort", ordenamiento_rapido, lista_productos))
        menu_ordenar.add_command(label="3. Selection Sort", command=lambda: self.aplicar_ordenamiento("Selection Sort", ordenamiento_seleccion, lista_productos))

        def buscar_producto_evento(event=None):
            valor = entry_buscar.get().strip()
            if not valor:
                messagebox.showwarning("Búsqueda", "Ingrese un código, nombre o categoría para buscar.")
                return

            with ProductosDB._conn() as conn:
                cur = conn.execute("""
                    SELECT codigo, nombre, categoria, precio_venta, cantidad
                    FROM productos
                    WHERE codigo LIKE ? OR nombre LIKE ? OR categoria LIKE ?
                    ORDER BY nombre
                """, (f"%{valor}%", f"%{valor}%", f"%{valor}%"))
                resultados = cur.fetchall()

            lista_productos.delete(0, tk.END)
            if resultados:
                for r in resultados:
                    if not isinstance(r, dict):
                        r = dict(r)
                    precio_venta = float(r.get("precio_venta", 0))
                    lista_productos.insert(tk.END,f"{r['codigo']:<17} {r['nombre']:<33} {r['categoria']:<17} Q.{precio_venta:<9.2f} {float(r['cantidad']):<10.2f}")

                if len(resultados) == 1:
                    unico = resultados[0]
                    codigo_label.config(text=unico["codigo"])
                    nombre_label.config(text=unico["nombre"])
                    categoria_label.config(text=unico["categoria"])
                    precio_venta_label.config(text=f"Q.{float(unico['precio_venta']):.2f}")
                    stock_label.config(text=f"{float(unico['cantidad']):.2f}")

            else:
                messagebox.showwarning("Sin resultados", "No se encontraron productos que coincidan.")
                codigo_label.config(text="")
                nombre_label.config(text="")
                categoria_label.config(text="")
                precio_venta_label.config(text="")
                stock_label.config(text="")

        def on_select(event):
            seleccion = lista_productos.curselection()
            if not seleccion:
                return
            index = seleccion[0]
            texto = lista_productos.get(index)
            codigo = texto[0:17].strip()
            nombre = texto[18:51].strip()
            categoria = texto[52:69].strip()
            try:
                partes = texto.split("Q.")
                precio = partes[1].split()[0] if len(partes) > 1 else "0.00"
                stock = texto.split()[-1]
            except Exception:
                precio = "0.00"
                stock = "0"
            codigo_label.config(text=codigo)
            nombre_label.config(text=nombre)
            categoria_label.config(text=categoria)
            precio_venta_label.config(text=f"Q.{precio}")
            stock_label.config(text=stock)
        lista_productos.bind("<<ListboxSelect>>", on_select)

        def actualizar_lista(event=None):
            cadena = entry_buscar.get()
            lista_productos.delete(0, tk.END)

            with ProductosDB._conn() as conn:
                if cadena:
                    patron = '%' + cadena + '%'
                    cur = conn.execute("SELECT codigo, nombre, categoria, precio_venta, cantidad FROM productos WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ? ORDER BY nombre",(patron, patron, patron))
                else:
                    cur = conn.execute("SELECT codigo, nombre, categoria, precio_venta, cantidad FROM productos ORDER BY nombre")

                for r in cur.fetchall():
                    lista_productos.insert(tk.END,f"{r['codigo']:<17} {r['nombre']:<33} {r['categoria']:<17} Q.{r['precio_venta']:<9.2f} {r['cantidad']:<10.2f}")

        def mostrar_detalle(event):
            if not lista_productos.curselection():
                return

            indice = lista_productos.curselection()[0]
            seleccion = lista_productos.get(indice)
            codigo = seleccion[:17].strip()

            with ProductosDB._conn() as conn:
                cur = conn.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
                producto = cur.fetchone()

                if producto:
                    codigo_label.config(text=producto['codigo'])
                    nombre_label.config(text=producto['nombre'])
                    categoria_label.config(text=producto['categoria'])
                    precio_venta_label.config(text=f"Q. {producto['precio_venta']:.2f}")
                    stock_label.config(text=f"{producto['cantidad']:.2f} unidades")

        entry_buscar.bind("<Return>", buscar_producto_evento)
        entry_buscar.bind("<KeyRelease>", actualizar_lista)
        lista_productos.bind("<<ListboxSelect>>", mostrar_detalle)
        actualizar_lista()

    def mostrar_crear_reporte(self):
        self.activar_boton(self.button_reportes)
        self.limpiar_panel()

        tk.Label(self.panel_right, text="CREAR REPORTE DE NOVEDADES",font=("Arial", 20, "bold"), bg="#FFFFFF").pack(pady=15)

        tk.Frame(self.panel_right, bg="gray", height=2).pack(fill="x", padx=0, pady=5)

        panel_form = tk.Frame(self.panel_right, bg="#FFFFFF")
        panel_form.pack(fill="both", expand=True, padx=50, pady=10)

        tk.Label(panel_form, text="Escriba el reporte o novedad:",font=("Arial", 14, "bold"), bg="#FFFFFF").pack(pady=5)

        texto_frame = tk.Frame(panel_form, bg="#FFFFFF")
        texto_frame.pack(pady=5)

        scroll_texto = tk.Scrollbar(texto_frame)
        scroll_texto.pack(side="right", fill="y")

        text_reporte = tk.Text(texto_frame, width=80, height=15,font=("Arial", 12), bg="#E6F3FF",relief="solid", borderwidth=2,yscrollcommand=scroll_texto.set, wrap="word")
        text_reporte.pack(side="left")
        scroll_texto.config(command=text_reporte.yview)

        def guardar_reporte():
            texto = text_reporte.get("1.0", tk.END).strip()

            if not texto:
                messagebox.showerror("Error", "El reporte no puede estar vacío.")
                return

            if len(texto) < 10:
                messagebox.showerror("Error", "El reporte debe tener al menos 10 caracteres.")
                return

            try:
                GuardarReporte.guardar_reporte(texto)
                messagebox.showinfo("Éxito", "Reporte guardado correctamente.")
                text_reporte.delete("1.0", tk.END)
                text_reporte.focus()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el reporte:\n{str(e)}")

        frame_botones = tk.Frame(panel_form, bg="#FFFFFF")
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="GUARDAR REPORTE",bg=self.COLOR_BOTON, fg="white",font=("Arial", 12, "bold"), relief="flat",cursor="hand2", command=guardar_reporte, width=20).grid(row=0, column=0, padx=10)

        tk.Button(frame_botones, text="LIMPIAR",bg="#6c757d", fg="white",font=("Arial", 12, "bold"), relief="flat",cursor="hand2", command=lambda: text_reporte.delete("1.0", tk.END),width=15).grid(row=0, column=1, padx=10)

        text_reporte.focus()

    def mostrar_resultados_busqueda_cajera(self, resultados):
        def buscar_listbox(widget):
            if isinstance(widget, tk.Listbox):
                return widget
            for hijo in widget.winfo_children():
                encontrado = buscar_listbox(hijo)
                if encontrado:
                    return encontrado
            return None
        lista_productos = buscar_listbox(self.panel_right)
        if not lista_productos:
            messagebox.showerror("Error", "No se encontró la lista del inventario para actualizar.")
            return
        lista_productos.delete(0, tk.END)
        if resultados:
            for r in resultados:
                if not isinstance(r, dict):
                    r = dict(r)
                precio_venta = float(r.get('precio_venta', r.get('precio', 0)))
                lista_productos.insert(tk.END,f"{r['codigo']:<17} {r['nombre']:<33} {r['categoria']:<17} " f"Q.{precio_venta:<9.2f} {float(r['cantidad']):<10.2f}")
            messagebox.showinfo("Búsqueda completada",f"Se encontraron {len(resultados)} resultado(s).")
        else:
            messagebox.showwarning("Sin resultados","No se encontraron productos que coincidan.")

    def abrir_busqueda_avanzada_cajera(self):
        ventana = tk.Toplevel(self)
        ventana.title("Búsqueda Avanzada")
        ancho, alto = 500, 500
        ventana.configure(bg="#FFFFFF")
        ventana.transient(self)
        ventana.grab_set()

        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(ventana,text="BÚSQUEDA AVANZADA",font=("Arial", 16, "bold"),bg="#FFFFFF",fg="#007BFF").pack(pady=20)

        tk.Frame(ventana, bg="gray", height=2).pack(fill="x", padx=20, pady=10)

        frame_secuencial = tk.LabelFrame(ventana,text="Búsqueda Secuencial",font=("Arial", 12, "bold"),bg="#FFFFFF",padx=20,pady=15)
        frame_secuencial.pack(pady=6, padx=20, fill="x")

        tk.Label(frame_secuencial, text="Buscar por:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=5, pady=5,sticky="w")
        combo_criterio = ttk.Combobox(frame_secuencial, values=["nombre", "codigo", "categoria"], state="readonly",width=15)
        combo_criterio.current(0)
        combo_criterio.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_secuencial, text="Valor:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=1, column=0,padx=5, pady=5,sticky="w")
        entry_valor = tk.Entry(frame_secuencial, width=30, bg="#E6F3FF", font=("Arial", 10))
        entry_valor.grid(row=1, column=1, padx=5, pady=5)

        def ejecutar_busqueda_secuencial():
            criterio = combo_criterio.get()
            valor = entry_valor.get().strip()
            if not valor:
                messagebox.showerror("Error", "Ingrese un valor para buscar", parent=ventana)
                return

            with ProductosDB._conn() as conn:
                cur = conn.execute(f"""
                    SELECT codigo, nombre, categoria, precio_venta, cantidad
                    FROM productos
                    WHERE {criterio} LIKE ?
                    ORDER BY nombre
                """, ('%' + valor + '%',))
                resultados = cur.fetchall()

            ventana.destroy()
            self.mostrar_resultados_busqueda_cajera(resultados)

        tk.Button(frame_secuencial,text="BUSCAR SECUENCIAL",bg="#007BFF",fg="white",font=("Arial", 10, "bold"),relief="flat",cursor="hand2",width=20,command=ejecutar_busqueda_secuencial).grid(row=2, column=0, columnspan=2, pady=10)

        frame_binaria = tk.LabelFrame(ventana,text="Búsqueda Binaria (Nombre Exacto)",font=("Arial", 12, "bold"),bg="#FFFFFF",padx=20,pady=15)
        frame_binaria.pack(pady=6, padx=20, fill="x")

        tk.Label(frame_binaria, text="Nombre exacto:", font=("Arial", 10, "bold"), bg="#FFFFFF").grid(row=0, column=0,padx=5, pady=5,sticky="w")
        entry_nombre = tk.Entry(frame_binaria, width=30, bg="#E6F3FF", font=("Arial", 10))
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        def ejecutar_busqueda_binaria():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Ingrese un nombre para buscar", parent=ventana)
                return

            resultado = BusquedaAvanzada.busqueda_binaria_db(nombre)
            ventana.destroy()
            if resultado:
                self.mostrar_resultados_busqueda_cajera([resultado])
            else:
                self.mostrar_resultados_busqueda_cajera([])

        tk.Button(frame_binaria,text="BUSCAR BINARIA",bg="#007BFF",fg="white",font=("Arial", 10, "bold"),relief="flat",cursor="hand2",width=20,command=ejecutar_busqueda_binaria).grid(row=1, column=0, columnspan=2, pady=10)

        frame_botones = tk.Frame(ventana, bg="#FFFFFF")
        frame_botones.pack(pady=12)

        btn_cancelar = tk.Button(frame_botones,text="CANCELAR",bg="#6c757d",fg="white",font=("Arial", 10, "bold"),relief="flat",cursor="hand2",width=15,command=ventana.destroy)
        btn_cancelar.pack(side="left", padx=8)


    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Confirmación", "¿Está seguro que desea salir?")
        if respuesta:
            self.destroy()
            root = tk.Tk()
            Login(root)
            root.mainloop()

class AppDeleteDB(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniMarket - SUPERADMIN")
        self.geometry("1200x600")
        self.resizable(True, True)
        self.configure(bg="#FFFFFF")
        self.COLOR_FONDO = "#1E90FF"
        self.COLOR_BOTON = "#007BFF"
        self.COLOR_PELIGRO = "#DC3545"
        self.COLOR_SELECCION = "#0056b3"
        self.protocol("WM_DELETE_WINDOW", self.cerrar_sesion)
        self.state('zoomed')

        self.panel_left = tk.Frame(self, bg="#1E90FF", width=200, height=500)
        self.panel_left.pack(side="left", fill="y")

        self.panel_right = tk.Frame(self, bg="#FFFFFF")
        self.panel_right.pack(side="right", fill="both", expand=True)

        self.imagen = tk.PhotoImage(file="2.png")
        self.label_logo = tk.Label(self.panel_left, image=self.imagen, bg="#1E90FF")
        self.label_logo.place(x=10, y=20)
        self.label_logo.bind("<Button-1>", self.mostrar_menu_principal)

        self.button_close = tk.Button(self.panel_left, text="CERRAR SESIÓN", bg="#007BFF", fg="white",font=("Arial", 10, "bold"), relief="flat", cursor="hand2", width=25,command=self.cerrar_sesion)
        self.button_close.place(x=0, y=550, height=35)

        self.mostrar_menu_principal()

    def limpiar_panel(self):
        for widget in self.panel_right.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self, event=None):
        self.limpiar_panel()

        tk.Label(self.panel_right, text="MENÚ PRINCIPAL - SUPERADMIN",font=("Arial", 22, "bold"), bg="#FFFFFF", fg="#DC3545").pack(pady=50)

        tk.Label(self.panel_right, text="PERFIL PARA GESTIÓN DE DATOS",font=("Arial", 16), bg="#FFFFFF").pack(pady=20)

        frame_botones = tk.Frame(self.panel_right, bg="#FFFFFF")
        frame_botones.pack(pady=50)

        tk.Label(frame_botones,text="ZONA PELIGROSA",font=("Arial", 16, "bold"),bg="#FFFFFF",fg="#DC3545").pack(pady=20)

        tk.Label(frame_botones,text="Las siguientes acciones son irreversibles y eliminarán todos los datos del sistema.",font=("Arial", 11),bg="#FFFFFF",fg="#666666",wraplength=600,justify="center").pack(pady=10)

        tk.Button(frame_botones,text="RESETEAR TODAS LAS BASES DE DATOS",bg=self.COLOR_PELIGRO,fg="white",font=("Arial", 14, "bold"),relief="flat",cursor="hand2",command=self.resetear_base_datos,width=40,height=2).pack(pady=20)


    def resetear_base_datos(self):
        primera_confirmacion = messagebox.askokcancel(
            "Advertencia crítica - Confirmación 1 de 2",
            "Está a punto de eliminar todos los datos del sistema.\n\n"
            "Esta acción incluye:\n"
            "• Todos los productos\n"
            "• Todas las ventas\n"
            "• Todas las categorías\n"
            "• Todos los proveedores\n\n"
            "• Todos los reportes\n\n"  
            "Esta acción no se puede deshacer.\n\n"
            "¿Está seguro de que desea continuar?"
        )

        if not primera_confirmacion:
            messagebox.showinfo("Cancelado", "Operación cancelada. No se eliminó ningún dato.")
            return

        from tkinter import simpledialog

        codigo_verificacion = simpledialog.askstring(
            "Confirmación final - 2 de 2",
            "Para confirmar que comprende las consecuencias,\n"
            "ingrese el siguiente código de verificación:\n\n"
            "ELIMINAR TODO\n\n"
            "(Debe escribirlo exactamente como está)"
        )

        if codigo_verificacion != "ELIMINAR TODO":
            if codigo_verificacion is not None:
                messagebox.showerror(
                    "Código incorrecto",
                    "Código de verificación incorrecto.\nOperación cancelada."
                )
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada. No se eliminó ningún dato.")
            return

        try:
            with ProductosDB._conn() as conn:
                cur_productos = conn.execute("SELECT COUNT(*) as total FROM productos")
                total_productos = cur_productos.fetchone()['total']

                cur_ventas = conn.execute("SELECT COUNT(*) as total FROM ventas")
                total_ventas = cur_ventas.fetchone()['total']

                cur_categorias = conn.execute("SELECT COUNT(*) as total FROM categorias")
                total_categorias = cur_categorias.fetchone()['total']

                cur_proveedores = conn.execute("SELECT COUNT(*) as total FROM proveedores")
                total_proveedores = cur_proveedores.fetchone()['total']

                cur_reportes = conn.execute("SELECT COUNT(*) as total FROM reportes_novedades")
                total_reportes = cur_reportes.fetchone()['total']

                conn.execute("DELETE FROM productos")
                conn.execute("DELETE FROM ventas")
                conn.execute("DELETE FROM categorias")
                conn.execute("DELETE FROM proveedores")
                conn.execute("DELETE FROM reportes_novedades")

                conn.execute("DELETE FROM sqlite_sequence WHERE name='productos'")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='ventas'")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='categorias'")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='proveedores'")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='reportes_novedades'")

                conn.commit()

            messagebox.showinfo(
                "Base de datos reseteada",
                f"Todas las bases de datos han sido eliminadas.\n\n"
                f"Resumen:\n"
                f"• Productos eliminados: {total_productos}\n"
                f"• Ventas eliminadas: {total_ventas}\n"
                f"• Categorías eliminadas: {total_categorias}\n"
                f"• Proveedores eliminados: {total_proveedores}\n"
                f"• Reportes eliminados: {total_reportes}\n"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al resetear la base de datos:\n\n{str(e)}"
            )

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
