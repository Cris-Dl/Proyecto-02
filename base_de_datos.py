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
    def ver_productos():
        with ProductosDB._conn() as conn:
            cur = conn.execute("SELECT * FROM productos")
            filas = cur.fetchall()
            if not filas:
                print("No hay productos registrados.")
                return
            print("\n--- LISTADO DE PRODUCTOS ---")
            for f in filas:
                print(
                    f"ID: {f['id_num']} | Nombre: {f['nombre']} | Codigo: {f['codigo']} | Precio: {f['precio']} | Categoría: {f['categoria']} | Cantidad:{f['cantidad']}")

    @staticmethod
    def registrar_producto():
        nombre = input("Ingrese el nombre del producto: ")
        codigo = input("Ingrese el codigo del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        categoria = input("Ingrese la categoria del producto: ")
        cantidad = int(input("Ingrese la cantidad que tiene del producto: "))
        nuevo_producto = Productos(codigo, nombre, precio, categoria, cantidad)
        ProductosDB.guardar(nuevo_producto)

    @staticmethod
    def eliminar_producto():
        codigo = input("Ingrese el codigo del producto a eliminar eliminar: ")
        with ProductosDB._conn() as conn:
            cur = conn.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
            if cur.rowcount == 0:
                print("No se encontró el producto.")
            else:
                print("Producto eliminado con éxito.")

    @staticmethod
    def consultar_producto():
        consulta = input("Ingrese la categoria a buscar: ")


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
            ProductosDB.eliminar_producto()
            print()