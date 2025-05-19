# nach_to_python.py

# Este script convierte un archivo NachLang (.nach) a un script Python ejecutable.

import re

REGLAS = [
    (r"^mostrar (.*)", r"print(\1)"),
    (r"^si (.*):", r"if \1:"),
    (r"^sino:", r"else:"),
    (r"^repetir (\d+) veces:", r"for _ in range(\1):"),
    (r"^definir funcion (.*)", r"def \1"),
    (r"^terminar", r"exit()"),
    (r"^#(.*)", r"#\1"),
]

ESPACIO = "    "


def convertir_linea(linea):
    for patron, reemplazo in REGLAS:
        if re.match(patron, linea):
            return re.sub(patron, reemplazo, linea)
    return linea


def convertir_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    resultado = []
    indentacion = 0

    for linea in lineas:
        linea = linea.rstrip()

        if linea.endswith(":"):
            resultado.append(ESPACIO * indentacion + convertir_linea(linea))
            indentacion += 1
        elif linea.strip() == "":
            resultado.append("")
        elif linea.startswith("sino"):
            indentacion -= 1
            resultado.append(ESPACIO * indentacion + convertir_linea(linea))
            indentacion += 1
        else:
            if linea.startswith(" " * 4):
                resultado.append(ESPACIO * indentacion + convertir_linea(linea.strip()))
            else:
                resultado.append(ESPACIO * indentacion + convertir_linea(linea))

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

    print(f"✅ Archivo convertido guardado como: {archivo_salida}")


if __name__ == "__main__":
    convertir_archivo("ejemplo.nach", "ejemplo_convertido.py")
