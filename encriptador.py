
import random  # Para usar 'seed' (semilla) y 'shuffle' (barajar)
import string  # Para obtener la lista completa de caracteres (ej: 'abc...', '123...', '!@#...')
from abc import ABC, abstractmethod


# --- 2. PLANTILLA DEL CODIFICADOR ---
class Codificador(ABC):
    """
    Esta es una Clase Base Abstracta (ABC).
    Sirve como una "plantilla" que obliga a cualquier
    clase que herede de ella (como CifradoCompleto) a tener
    los métodos que aquí se definen (@abstractmethod).

    Si creamos un nuevo cifrado y olvidamos definir .codificar(), Python dará un error.
    """
    @abstractmethod
    def codificar(self, texto: str) -> str:
        pass

    @abstractmethod
    def decodificar(self, texto: str) -> str:
        pass


class CifradoCompleto(Codificador):
    """
    Cifrado por sustitución usando una clave secreta como "semilla" para el generador aleatorio (pero replicable).
    """
    def __init__(self, clave_secreta: str):
        caracteres_normales = list(string.printable)    # 'string.printable' es una cadena que contiene todos los caractere ASCII imprimibles: letras, números, puntuación y espacios.
        caracteres_clave = list(caracteres_normales)    # Creamos una copia exacta pero desordenada.

        random.seed(clave_secreta)                      # Inicializa el generador 'aleatorio'. Esto está basado en la clave que le proporcionemos.
        random.shuffle(caracteres_clave)                # Desordena la lista de caracteres 'clave_secreta'

        # --- MAPAS DE TRADUCCIÓN ---
        self.mapa_codificar = dict(zip(caracteres_normales, caracteres_clave))    # 'zip()' une las dos listas -> (normal[0], clave[0]), (normal[1], clave[1]), ...
        self.mapa_decodificar = dict(zip(caracteres_clave, caracteres_normales))  # igual pero a la inversa

    def codificar(self, texto_original: str) -> str:
        """
        Toma el texto de entrada (original) y lo traduce 
        carácter por carácter usando el 'mapa_codificar'.
        """
        texto_resultado = ""
        for char in texto_original:
            # 'self.mapa_codificar.get(char, char)' es la operación principal:
            # 1. Intenta buscar 'char' (ej: 'H') como clave en el mapa.
            # 2. Si lo encuentra, devuelve su valor (ej: 'p').
            # 3. Si NO lo encuentra (ej: un emoji), devuelve 'char' (el valor original, 'H').
            # 4. Añade el carácter (traducido o no) al resultado.
            texto_resultado += self.mapa_codificar.get(char, char)
        return texto_resultado

    def decodificar(self, texto_codificado: str) -> str:
        """
        Toma el texto cifrado y lo revierte 
        carácter por carácter usando el 'mapa_decodificar'.
        """
        texto_resultado = ""
        for char in texto_codificado:
            texto_resultado += self.mapa_decodificar.get(char, char)
        return texto_resultado  # Devuelve el texto original