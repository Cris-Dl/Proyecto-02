import sqlite3

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
        conn.commit()
        return conn

    @staticmethod
    def guardar(producto: Productos):
        with ProductosDB._conn() as conn:
            conn.execute(
                "INSERT INTO productos (nombre, codigo, precio, categoria, cantidad) VALUES (?, ?, ?, ?, ?)",
                (producto.nombre, producto.codigo, producto.precio, producto.categoria, producto.cantidad)
            )
        print(f"Productos '{producto.nombre}' guardado con éxito.")

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
                "SELECT nombre, codigo FROM productos WHERE nombre LIKE ? OR codigo LIKE ? LIMIT 10",
                (patron, patron)
            )
            return cur.fetchall()





while True:
    print("---Menú----")
    print("1.- Registrar producto")
    print("2.- Ver productos")
    print("3.- Eliminar producto")
    menu_option = input("Ingrese el número de la opción que quiera realizar: ")
    print()
    match menu_option:
        case "1":
            print("Registrar producto")
            ProductosDB.registrar_producto()
            print()
        case "2":
            print("Ver productos")
            ProductosDB.ver_productos()
            print()
        case "3":
            print("Eliminar producto")
            ProductosDB.elim