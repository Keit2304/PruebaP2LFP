import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

def nuevo_archivo(code_area, master):
    
    contenido_actual = code_area.get("1.0", "end-1c")
    if contenido_actual.strip():
        
        respuesta = messagebox.askyesnocancel("Nuevo archivo", "¿Desea guardar los cambios en el archivo actual antes de crear uno nuevo?")
        if respuesta is None:
            
            return
        elif respuesta:
            
            guardar_como_archivo(code_area)
    
    
    code_area.delete("1.0", "end")

def abrir_archivo(code_area):
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if ruta_archivo:
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            contenido = file.read()
            code_area.delete("1.0", "end")
            code_area.insert("1.0", contenido)

def guardar_archivo():
    print("Guardar archivo")

def guardar_como_archivo(code_area):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        contenido = code_area.get("1.0", "end-1c")
        with open(ruta_archivo, "w") as file:
            file.write(contenido)

def salir(master):
    confirmar_salir = messagebox.askyesno("Salir", "¿Está seguro que desea salir del programa?")
    if confirmar_salir:
        print("Saliendo del programa")
        master.destroy()

def generar_mongodb():
    print("Generar sentencias MongoDB")

def ver_tokens():
    print("Ver Tokens")

def ventana():
    root = tk.Tk()
    root.title("Proyecto #2 - LFP - Keitlyn Tunchez - 202201139")

    window_width = 800  # Ancho 
    window_height = 600  # Alto 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Barra de menú
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Crear los menús
    file_menu = tk.Menu(menubar)
    edit_menu = tk.Menu(menubar)
    view_menu = tk.Menu(menubar)
    help_menu = tk.Menu(menubar)

    menubar.add_cascade(label="Archivo", menu=file_menu)
    menubar.add_cascade(label="Análisis", menu=edit_menu)
    menubar.add_cascade(label="Tokens", menu=view_menu)
    menubar.add_cascade(label="Errores", menu=help_menu)

    # Opciones del menú Archivo
    file_menu.add_command(label="Nuevo", command=lambda: nuevo_archivo(code_area, root))
    file_menu.add_command(label="Abrir", command=lambda: abrir_archivo(code_area))
    file_menu.add_command(label="Guardar", command=guardar_archivo)
    file_menu.add_command(label="Guardar Como", command=lambda: guardar_como_archivo(code_area))
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=lambda: salir(root))

    # Opción del menú Análisis
    edit_menu.add_command(label="Generar sentencias MongoDB", command=generar_mongodb)

    # Opción del menú Tokens
    view_menu.add_command(label="Ver Tokens", command=ver_tokens)

    # Crear el área de edición de código
    code_label = tk.Label(root, text="Archivo de entrada:")
    code_label.pack(anchor="w", padx=10, pady=5)

    code_area = tk.Text(root, font=("Consolas", 12), height=20, width=100)
    code_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    ventana()