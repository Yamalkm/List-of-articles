from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana_editar = None
        self.ventana = root
        self.ventana.title('App Gestor de Productos')
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/M6_P2_icon.ico')

        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto', font=('Calibri', 10, 'bold'))
        frame.grid(row=0, column=0, columnspan=5, pady=20)

        # Nombre
        self.etiqueta_nombre = Label(frame, text='Nombre: ')
        self.etiqueta_nombre.grid(row=1, column=0)

        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Precio
        self.etiqueta_precio = Label(frame, text='Precio: ')
        self.etiqueta_precio.grid(row=2, column=0)

        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # Stock
        self.etiqueta_stock = Label(frame, text='Stock: ')
        self.etiqueta_stock.grid(row=3, column=0)

        self.stock = Entry(frame)
        self.stock.grid(row=3, column=1)

        #Categoria

        self.etiqueta_categoria = Label(frame, text='Categoria: ')
        self.etiqueta_categoria.grid(row=4, column=0)

        self.categoria = Entry(frame)
        self.categoria.grid(row=4, column=1)

        # Botón Añadir Producto
        self.boton_aniadir = ttk.Button(frame, text='Guardar Producto', command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure('my.TButton', font=('Calibri', 11, 'bold'))

        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview",
                     [('mystystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=("#1", "#2","#3"), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='Stock', anchor=CENTER)  # Encabezado 2
        self.tabla.heading('#3', text='Categoria', anchor=CENTER)  # Encabezado 3

        self.get_productos()

        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        boton_eliminar.grid(row=6, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        boton_editar.grid(row=6, column=1, sticky=W + E)

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        resgistros_tabla = self.tabla.get_children()
        for fila in resgistros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            self.tabla.insert('', 0, text=fila[1], values=(fila[2],fila[3],fila[4]))

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def validacion_stock(self):
        return len(self.stock.get()) != 0

    def validacion_categoria(self):
        return len(self.categoria.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() and self.validacion_categoria():
            query = 'INSERT INTO producto VALUES(NULL,?,?,?,?)'
            parametros = (self.nombre.get(), self.precio.get(), self.stock.get(),self.categoria.get())
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadir con éxito'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.stock.delete(0, END)
            self.categoria.delete(0, END)
            # print(self.nombre.get())
            # print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_stock() == False and self.validacion_categoria() == False:
            print('El precio, stock y categoria son obligatorios')
            self.mensaje['text'] = 'El precio, stock y categoria son obligatorios'

        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_stock() == False and self.validacion_categoria() == False:
            print('El nombre, stock y categoria son obligatorios')
            self.mensaje['text'] = 'El nombre, stock y categoria son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() == False and self.validacion_precio()== False and self.validacion_stock() and self.validacion_categoria() == False:
            print('El nombre, precio y categoria son obligatorios')
            self.mensaje['text'] = 'El nombre, precio y categoria son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() == False and self.validacion_precio()== False and self.validacion_stock()== False and self.validacion_categoria():
            print('El nombre, precio y stock son obligatorios')
            self.mensaje['text'] = 'El nombre, precio y stock son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_stock()== False and self.validacion_categoria()== False:
            print('El stock y categoria son obligatorios')
            self.mensaje['text'] = 'El stock y categoria son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_stock() and self.validacion_categoria()== False:
            print('La categoria es obligatoria')
            self.mensaje['text'] = 'La categoria es obligatoria'.format(self.nombre.get())

        elif self.validacion_nombre() == False and self.validacion_precio()  and self.validacion_stock() and self.validacion_categoria()== False:
            print('El precio y stock son obligatorios')
            self.mensaje['text'] = 'El nombre y categoria son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() == False and self.validacion_precio() == False  and self.validacion_stock() and self.validacion_categoria():
            print('El nombre y precio son obligatorios')
            self.mensaje['text'] = 'El nombre y precio son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio() == False  and self.validacion_stock() and self.validacion_categoria()== False:
            print('El precio y categoria son obligatorios')
            self.mensaje['text'] = 'El precio y categoria son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio() == False  and self.validacion_stock() and self.validacion_categoria():
            print('El precio es obligatorio')
            self.mensaje['text'] = 'El precio es obligatorio'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio()  and self.validacion_stock()== False  and self.validacion_categoria():
            print('El stock es obligatorio')
            self.mensaje['text'] = 'El stock es obligatorio'.format(self.nombre.get())

        elif self.validacion_nombre() == False and self.validacion_precio()  and self.validacion_stock()  and self.validacion_categoria():
            print('El nombre es obligatorio')
            self.mensaje['text'] = 'El nombre es obligatorio'.format(self.nombre.get())

        elif self.validacion_nombre() and self.validacion_precio()== False  and self.validacion_stock()== False  and self.validacion_categoria():
            print('El precio y stock son obligatorios')
            self.mensaje['text'] = 'El precio y stock son obligatorios'.format(self.nombre.get())

        elif self.validacion_nombre()== False and self.validacion_precio()  and self.validacion_stock()== False  and self.validacion_categoria():
            print('El nombre y stock son obligatorios')
            self.mensaje['text'] = 'El nombre y stock son obligatorios'.format(self.nombre.get())


        else:
            print('El nombre y el precio son obligatorios')
            self.mensaje['text'] = 'El nombre, el precio, el stock y la categoria son obligatorios'

        self.get_productos()

    def del_producto(self):
        # print('Eliminar producto')
        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()

    def edit_producto(self):
        print('Editar producto')
        self.mensaje['text'] = ''

        old_nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]
        old_stock = self.tabla.item(self.tabla.selection())['values'][1]
        old_categoria = self.tabla.item(self.tabla.selection())['values'][2]

        self.ventana_editar = Toplevel()  # Crear una ventana nueva
        self.ventana_editar.title('Editar Producto')
        self.ventana_editar.resizable(1, 1)
        self.ventana_editar.wm_iconbitmap("recursos/M6_P2_icon.ico")

        titulo = Label(self.ventana_editar, text='Edición de Producto', font=('Calibri', 20, 'bold'))
        titulo.grid(row=0, column=0)

        frame_ep = LabelFrame(self.ventana_editar, text='Editar el siguiente Producto', font=('Calibri', 13, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text='Nombre antiguo: ', font=('Calibri', 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Entry Nombre antiguo

        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre),
                                          state='readonly', font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text='Nombre nuevo: ', font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)

        ##################################

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text='Precio antiguo: ', font=('Calibri', 13))
        self.etiqueta_precio_antiguo.grid(row=4, column=0)
        # Entry Precio antiguo
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text='Precio nuevo: ', font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        ##################################

        # Label Stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text='Stock antiguo: ', font=('Calibri', 13))
        self.etiqueta_stock_antiguo.grid(row=6, column=0)
        # Entry Stock antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                          state='readonly', font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=6, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text='Stock nuevo: ', font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=7, column=0)
        # Entry Stock nuevo
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=7, column=1)

        ##################################

        # Label Categoria antiguo
        self.etiqueta_categoria_antiguo = Label(frame_ep, text='Categoria antiguo: ', font=('Calibri', 13))
        self.etiqueta_categoria_antiguo.grid(row=8, column=0)
        # Entry Categoria antiguo
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                         state='readonly', font=('Calibri', 13))
        self.input_categoria_antiguo.grid(row=8, column=1)

        # Label Categoria nuevo
        self.etiqueta_categoria_nuevo = Label(frame_ep, text='Categoria nuevo: ', font=('Calibri', 13))
        self.etiqueta_categoria_nuevo.grid(row=9, column=0)
        # Entry Categoria nuevo
        self.input_categoria_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nuevo.grid(row=9, column=1)



        self.boton_actualizar = ttk.Button(frame_ep, text='Actualizar Producto',
                                           command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                     self.input_nombre_antiguo.get(),
                                                                                     self.input_precio_nuevo.get(),
                                                                                     self.input_precio_antiguo.get(),
                                                                                     self.input_stock_nuevo.get(),
                                                                                     self.input_stock_antiguo.get(),
                                                                                     self.input_categoria_nuevo.get(),
                                                                                     self.input_categoria_antiguo.get()),
                                           style='my.TButton')

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)
    def input_nombre(self):
        return len(self.input_nombre_nuevo.get()) != 0

    def input_precio(self):
        return len(self.input_precio_nuevo.get()) != 0

    def input_stock(self):
        return len(self.input_stock_nuevo.get()) != 0

    def input_categoria(self):
        return len(self.input_categoria_nuevo.get()) != 0
    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio,
                             nuevo_stock, antiguo_stock, nuevo_categoria, antiguo_categoria):
        if self.input_nombre() and self.input_precio() and self.input_stock() and self.input_categoria():
            query = 'UPDATE producto SET nombre = ?, precio = ?, stock = ?, categoria = ? WHERE nombre = ? AND precio = ? AND stock = ? AND categoria = ?'
            parametros = (nuevo_nombre, nuevo_precio, nuevo_stock, nuevo_categoria, antiguo_nombre, antiguo_precio, antiguo_stock, antiguo_categoria)
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            self.get_productos()


if __name__ == "__main__":
    root = Tk()
    app = Producto(root)
    root.mainloop()
