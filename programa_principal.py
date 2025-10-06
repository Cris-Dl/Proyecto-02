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



