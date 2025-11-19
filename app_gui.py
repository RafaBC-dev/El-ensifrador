
import customtkinter as ctk
import pyperclip  # Para copiar en portapapeles
from encriptador import CifradoCompleto

# APARIENCIA
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Ventana principal
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE LA VENTANA ---
        self.title("El ensifrador")
        self.geometry("700x700")

        # Para que sea responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # --- ZONA CLAVE SECRETA ---
        frame_clave = ctk.CTkFrame(self) # Zona Clave_secreta y área texto para escribirla
        frame_clave.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew") # sticky="ew" => que se estire horizontalmente
        frame_clave.grid_columnconfigure(1, weight=1)

        label_clave = ctk.CTkLabel(frame_clave, text="Clave Secreta:")
        label_clave.grid(row=0, column=0, padx=10, pady=10)

        self.entry_clave = ctk.CTkEntry(frame_clave, show="*") # 'show="*"' -> oculta lo que escribes (modo contraseña)
        self.entry_clave.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- ZONA TEXTO NORMAL ---
        self.label_normal = ctk.CTkLabel(self, text="Texto Normal", font=ctk.CTkFont(weight="bold"))
        self.label_normal.grid(row=1, column=0, padx=10, pady=(8, 0), sticky="w")  # "w" => pegado a la izquierda

        self.txt_normal = ctk.CTkTextbox(self, height=200)
        self.txt_normal.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")  # "nsew" => que se estire en todas direcciones

        # --- ZONA DE BOTONES ---
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")  # Marco invisible
        frame_botones.grid(row=3, column=0, pady=8)

        self.btn_codificar = ctk.CTkButton(frame_botones, text="Codificar ⬇️", command=self.accion_codificar)
        self.btn_codificar.grid(row=0, column=0, padx=12)

        self.btn_decodificar = ctk.CTkButton(frame_botones, text="Decodificar ⬆️", command=self.accion_decodificar)
        self.btn_decodificar.grid(row=0, column=1, padx=12)

        self.btn_limpiar = ctk.CTkButton(frame_botones, text="Limpiar Todo", fg_color="#D35400", hover_color="#E67E22", command=self.accion_limpiar)
        self.btn_limpiar.grid(row=0, column=2, padx=12)

        # --- ZONA TEXTO CIFRADO ---
        self.label_cifrado = ctk.CTkLabel(self, text="Texto Cifrado", font=ctk.CTkFont(weight="bold"))
        self.label_cifrado.grid(row=4, column=0, padx=10, pady=(8, 0), sticky="w")

        self.txt_cifrado = ctk.CTkTextbox(self, height=200)
        self.txt_cifrado.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

        self.btn_copiar_normal = ctk.CTkButton(self, text="Copiar", width=80, command=lambda: self.accion_copiar(self.txt_normal)) # para poder pasar un argumento (text area -> txt_normal) a la función
        self.btn_copiar_normal.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="e")  # "e" => pegado a la derecha

        self.btn_copiar_cifrado = ctk.CTkButton(self, text="Copiar", width=80, command=lambda: self.accion_copiar(self.txt_cifrado))
        self.btn_copiar_cifrado.grid(row=4, column=0, padx=10, pady=(5, 0), sticky="e")

        # Para mostrar mensajes
        self.label_estado = ctk.CTkLabel(self, text="", text_color="red")
        self.label_estado.grid(row=6, column=0, padx=10, pady=5, sticky="w")


    # --- 5. MÉTODOS (Las acciones de los botones) ---
    def get_codificador(self):
        """
        1. Coge la clave secreta del campo de entrada (entry_clave).
        2. Si la clave está vacía, muestra un error y devuelve 'None'.
        3. Si hay clave, crea el objeto CifradoCompleto y lo devuelve.
        """
        clave = self.entry_clave.get()
        if not clave:
            self.label_estado.configure(text="¡Error: Se necesita una clave secreta!", text_color="red")
            return None

        self.label_estado.configure(text="")
        return CifradoCompleto(clave_secreta=clave)

    def accion_codificar(self):
        """ Se llama al pulsar el botón 'Codificar' """
        codificador = self.get_codificador()
        if not codificador:
            return  # Si no hay clave, no hace nada

        texto_original = self.txt_normal.get("1.0", "end-1c")  # Para obtener texto normal empezando por el primer caracter de la primera línea y el último, ignorando el salto de línea final (-1 caracter)
        texto_codificado = codificador.codificar(texto_original)

        # Poner el resultado en la caja "Cifrado"
        self.txt_cifrado.delete("1.0", "end")  # Borra lo que hubiera antes
        self.txt_cifrado.insert("1.0", texto_codificado)  # Inserta el nuevo texto

    def accion_decodificar(self):
        """Se llama al pulsar el botón 'Decodificar' """
        codificador = self.get_codificador()
        if not codificador:
            return

        texto_codificado = self.txt_cifrado.get("1.0", "end-1c")
        texto_decodificado = codificador.decodificar(texto_codificado)

        self.txt_normal.delete("1.0", "end")
        self.txt_normal.insert("1.0", texto_decodificado)

    def accion_limpiar(self):
        """Limpia las dos cajas de texto y el mensaje de estado."""
        self.txt_normal.delete("1.0", "end")
        self.txt_cifrado.delete("1.0", "end")
        self.label_estado.configure(text="")

    def accion_copiar(self, caja_de_texto):
        """Copia el texto de una caja (la que pasamos como argumento)"""
        texto = caja_de_texto.get("1.0", "end-1c")
        if texto:
            pyperclip.copy(texto)

            self.label_estado.configure(text="¡Texto copiado!", text_color="green")
            self.after(2000, lambda: self.label_estado.configure(text=""))

        else:
            self.label_estado.configure(text="Nada que copiar.", text_color="orange")
            self.after(2000, lambda: self.label_estado.configure(text=""))


if __name__ == "__main__":
    app = App()
    app.mainloop()