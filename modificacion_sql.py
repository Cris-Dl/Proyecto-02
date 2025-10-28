import sqlite3
from datetime import datetime

DB_NAME = "productos.db"

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
        return self.__precio_compra

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
                    codigo TEXT UNIQUE NOT NULL,
                    precio_venta REAL,
                    precio_compra REAL,
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

        # Tabla de Categorias
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS categorias (
                            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT UNIQUE NOT NULL
                        );
                    """)
        conn.commit()
        return conn

    @staticmethod
    def guardar(producto: Productos):
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO productos (nombre, codigo, precio_compra, precio_venta, categoria, cantidad) VALUES (?, ?, ?, ?, ?, ?)",
                (producto.nombre, producto.codigo, producto.precio_compra,producto.precio_venta, producto.categoria, producto.cantidad)
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
                "SELECT nombre, codigo, precio_venta FROM productos WHERE nombre LIKE ? OR codigo LIKE ? LIMIT 10",
                (patron, patron)
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
        print(f"Venta registrada: Total ${total:.2f}")

    @staticmethod
    def actualizar_stock(codigo: str, cantidad_vendida: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?",
                (cantidad_vendida, codigo)
            )
            conn.commit()

    @staticmethod
    def modificar_producto(codigo: str, nombre: str, precio_compra: float, precio_venta: float, categoria: str,cantidad: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET nombre=?, precio_compra=?, precio_venta=?, categoria=?, cantidad=? WHERE codigo=?",
                (nombre, precio_compra, precio_venta, categoria, cantidad, codigo)
            )
            conn.commit()

    @staticmethod
    def agregar_stock(codigo: str, cantidad_adicional: float):
        with ProductosDB._conn() as conn:
            conn.execute(
                "UPDATE productos SET cantidad = cantidad + ? WHERE codigo = ?",
                (cantidad_adicional, codigo)
            )
            conn.commit()

    @staticmethod
    def obtener_categorias():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT nombre FROM categorias ORDER BY nombre")
            return [row['nombre'] for row in cur.fetchall()]

    @staticmethod
    def agregar_categoria(nombre: str):
        with ProductosDB._conn() as conn:
            conn.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
            conn.commit()

