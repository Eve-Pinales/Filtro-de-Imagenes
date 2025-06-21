from abc import ABC, abstractmethod
from PIL import Image, ImageOps, ImageTk, ImageFilter
import tkinter as tk
from tkinter import filedialog
import os

# Clase base Imagen
class Imagen:
    def __init__(self, ruta=None):
        self.imagen = None
        self.original = None
        self.ruta = ruta

    def cargar(self, ruta):
        self.imagen = Image.open(ruta)
        self.original = self.imagen.copy()
        self.ruta = ruta
        return self.imagen

    def guardar(self, ruta):
        if self.imagen:
            self.imagen.save(ruta)
            return True
        return False

    def set_imagen(self, nueva_imagen):
        self.imagen = nueva_imagen

    def restaurar_original(self):
        if self.original:
            self.imagen = self.original.copy()

# Clase abstracta Filtro
class Filtro(ABC):
    @abstractmethod
    def aplicar(self, imagen: Image.Image) -> Image.Image:
        pass

# Filtros básicos
class FiltroGrises(Filtro):
    def aplicar(self, imagen):
        return ImageOps.grayscale(imagen)

class FiltroInversion(Filtro):
    def aplicar(self, imagen):
        return ImageOps.invert(imagen.convert("RGB"))

class FiltroDesenfoque(Filtro):
    def aplicar(self, imagen):
        return imagen.filter(ImageFilter.BLUR)

class FiltroBinarizacion(Filtro):
    def aplicar(self, imagen):
        return imagen.convert("L").point(lambda x: 0 if x < 128 else 255, '1')

class FiltroRotacion(Filtro):
    def aplicar(self, imagen):
        return imagen.rotate(90, expand=True)

class FiltroRedimension(Filtro):
    def aplicar(self, imagen):
        return imagen.resize((int(imagen.width / 2), int(imagen.height / 2)))

class FiltroAumento(Filtro):
    def aplicar(self, imagen):
        return imagen.resize((int(imagen.width * 2), int(imagen.height * 2)))

# Interfaz gráfica
class InterfazEditor:
    def __init__(self):
        self.editor = Imagen()
        self.ventana = tk.Tk()
        self.ventana.title("Editor Profesional de Imágenes")
        self.ventana.configure(bg="#FFC0CB")  # Fondo rosa
        self.imagen_tk = None

        self.frame_botones = tk.Frame(self.ventana, bg="#FFC0CB")
        self.frame_botones.grid(row=0, column=0, sticky="ns", padx=20, pady=20)

        self.label_imagen = tk.Label(self.ventana, bg="#FFC0CB")
        self.label_imagen.grid(row=0, column=1, padx=40, pady=20)

        self.crear_widgets()

    def crear_widgets(self):
        estilo_boton = {
            'bg': '#D3D3D3',
            'fg': 'black',
            'font': ('Helvetica', 10, 'bold'),
            'width': 25,
            'relief': 'raised',
            'bd': 2,
            'padx': 5,
            'pady': 5
        }

        botones = [
            ("Cargar Imagen", self.cargar_imagen),
            ("Restaurar Original", self.restaurar_original),
            ("Escala de Grises", self.aplicar_grises),
            ("Inversión", self.aplicar_inversion),
            ("Desenfoque", self.aplicar_desenfoque),
            ("Binarización", self.aplicar_binarizacion),
            ("Rotación 90°", self.aplicar_rotacion),
            ("Guardar Imagen", self.guardar_imagen)
        ]

        for texto, comando in botones:
            btn = tk.Button(self.frame_botones, text=texto, command=comando, **estilo_boton)
            btn.pack(pady=4)

    def actualizar_vista_imagen(self):
        if self.editor.imagen:
            img_mostrar = self.editor.imagen.copy()
            img_mostrar.thumbnail((500, 500))
            self.imagen_tk = ImageTk.PhotoImage(img_mostrar)
            self.label_imagen.config(image=self.imagen_tk)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.bmp")])
        if ruta:
            self.editor.cargar(ruta)
            self.actualizar_vista_imagen()

    def restaurar_original(self):
        self.editor.restaurar_original()
        self.actualizar_vista_imagen()

    def aplicar_grises(self):
        self.aplicar_filtro(FiltroGrises())

    def aplicar_inversion(self):
        self.aplicar_filtro(FiltroInversion())

    def aplicar_desenfoque(self):
        self.aplicar_filtro(FiltroDesenfoque())

    def aplicar_binarizacion(self):
        self.aplicar_filtro(FiltroBinarizacion())

    def aplicar_rotacion(self):
        self.aplicar_filtro(FiltroRotacion())

    def aplicar_filtro(self, filtro):
        if self.editor.imagen:
            nueva_img = filtro.aplicar(self.editor.imagen)
            self.editor.set_imagen(nueva_img)
            self.actualizar_vista_imagen()

    def guardar_imagen(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if ruta:
            self.editor.guardar(ruta)

    def ejecutar(self):
        self.ventana.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = InterfazEditor()
    app.ejecutar()
