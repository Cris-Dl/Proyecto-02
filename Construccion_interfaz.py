import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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

        buton=tk.Button(frame_left, text="Guardar", bg="#2779F5", command=lambda:self.tab_productos.destroy())  #ERROR
        buton.place(x=10, y=130,)

    def ventas(self):
        frame=ttk.Frame(self.tab_ventas, padding=10)
        frame.pack(side="right", fill="y")

        ttk.Label(frame, text="Reporte").pack(anchor='w')

ventana=tk.Tk()
ventana.title("PRUEBA")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    ventana.mainloop()
