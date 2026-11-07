"""
Sistema de Gestión de Estudiantes (SGE) básico
------------------------------------------------
Autor:   Joseth David Moreno Duarte
Curso:   Algoritmos y Programación, Fundación Universitaria Compensar
Python:  3.10 o superior (se usa la estructura match-case)

Aplicación de consola que permite agregar, mostrar (en orden normal, inverso
y por ranking de promedio), buscar por ID, eliminar y analizar estudiantes.
Los registros se guardan en una lista con capacidad máxima controlada.
"""

# ==========================================================================
# CONSTANTES
# Se declaran en mayúsculas para indicar que su valor no debe cambiar.
# ==========================================================================
MAX_ESTUDIANTES = 50       # Capacidad máxima: evita que la lista crezca sin control
ID_MINIMO = 1
ID_MAXIMO = 999999
NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0          # Escala de calificación colombiana (0.0 a 5.0)
NOTA_APROBATORIA = 3.0
LINEA = "=" * 64
# Palabras que se dejan en minúscula al dar formato a nombres y programas
CONECTORES = ("de", "del", "la", "las", "los", "y", "e")


# ==========================================================================
# FUNCIONES DE ENTRADA Y VALIDACIÓN
# Ninguna de ellas deja avanzar al programa con un dato inválido; así se
# evita que un error de digitación lo detenga (manejo robusto de entradas).
# ==========================================================================
def leer_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de un rango hasta que sea válido."""
    # Repetición condicionada al final (equivalente a un do-while):
    # primero se pide el dato y DESPUÉS se decide si hay que repetir.
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            # Si el usuario escribe letras, int() falla; se captura el
            # error para que el programa no se caiga.
            print("  [!] Entrada inválida: escriba solo números enteros.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  [!] El valor debe estar entre {minimo} y {maximo}.")


def leer_nota(mensaje):
    """Pide una nota decimal entre NOTA_MINIMA y NOTA_MAXIMA."""
    while True:
        # Se acepta la coma decimal (4,5) porque es la costumbre en Colombia.
        texto = input(mensaje).strip().replace(",", ".")
        try:
            nota = float(texto)
        except ValueError:
            print("  [!] Entrada inválida: escriba un número, por ejemplo 4.2")
            continue
        if NOTA_MINIMA <= nota <= NOTA_MAXIMA:
            return round(nota, 1)
        print(f"  [!] La nota debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")


def leer_texto(mensaje):
    """Pide un texto no vacío que contenga solo letras y espacios."""
    while True:
        texto = " ".join(input(mensaje).split())   # quita espacios sobrantes
        if texto == "":
            print("  [!] Este campo no puede quedar vacío.")
        elif not all(caracter.isalpha() or caracter == " " for caracter in texto):
            print("  [!] Use solo letras y espacios.")
        else:
            return formatear_nombre(texto)


def formatear_nombre(texto):
    """Pone mayúscula inicial a cada palabra, salvo a los conectores.

    Ejemplo: "ingeniería de software" -> "Ingeniería de Software".
    """
    palabras = texto.lower().split()
    resultado = []
    for numero, palabra in enumerate(palabras):
        if numero > 0 and palabra in CONECTORES:
            resultado.append(palabra)
        else:
            resultado.append(palabra.capitalize())
    return " ".join(resultado)


def confirmar(pregunta):
    """Hace una pregunta de sí o no (s/n) y devuelve True si la respuesta es 's'."""
    # También condicionada al final: la pregunta se hace al menos una vez.
    # Se reutiliza para confirmar la salida y la eliminación de un estudiante.
    while True:
        respuesta = input(pregunta + " (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("  [!] Responda únicamente con 's' o 'n'.")


# ==========================================================================
# FUNCIONES DE APOYO (unidades de código reutilizables)
# ==========================================================================
def buscar_posicion(estudiantes, id_buscado):
    """Devuelve la posición del estudiante con ese ID, o -1 si no existe.

    Búsqueda lineal con BANDERA: el ciclo se detiene apenas encuentra el
    ID, sin recorrer el resto de la lista. Se reutiliza tanto en la opción
    de búsqueda como al agregar (para impedir IDs duplicados).
    """
    posicion = -1
    encontrado = False          # Bandera: indica si ya se halló el estudiante
    indice = 0
    while indice < len(estudiantes) and not encontrado:
        if estudiantes[indice]["id"] == id_buscado:
            encontrado = True
            posicion = indice
        indice += 1
    return posicion


def clasificar_desempeno(promedio):
    """Clasifica el promedio mediante decisiones ANIDADAS."""
    if promedio >= NOTA_APROBATORIA:
        # Esta segunda decisión solo tiene sentido si el estudiante aprobó.
        if promedio >= 4.5:
            return "Excelente"
        elif promedio >= 4.0:
            return "Sobresaliente"
        else:
            return "Aceptable"
    else:
        return "En riesgo"


def ordenar_por_promedio(estudiantes):
    """Devuelve una COPIA de la lista ordenada de mayor a menor promedio.

    Ordenamiento burbuja optimizado: dos ciclos for ANIDADOS y una BANDERA
    (hubo_intercambio) que detiene el proceso en cuanto la lista ya está
    ordenada. Se trabaja sobre una copia para no alterar el orden de registro.
    """
    ranking = list(estudiantes)                  # Copia superficial de la lista
    n = len(ranking)
    for pasada in range(n - 1):                  # Ciclo externo: n-1 pasadas como máximo
        hubo_intercambio = False                 # Bandera de optimización
        for j in range(n - 1 - pasada):          # Ciclo interno (anidado)
            if ranking[j]["promedio"] < ranking[j + 1]["promedio"]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
                hubo_intercambio = True
        if not hubo_intercambio:                 # Sin intercambios: ya está ordenada
            break
    return ranking


def mostrar_encabezado():
    """Imprime los títulos de las columnas de la tabla de estudiantes."""
    print(f"{'N.º':<4}{'ID':<8}{'Nombre':<22}{'Programa':<26}{'Prom.':<6}{'Desempeño'}")
    print("-" * 80)


def mostrar_estudiante(estudiante, numero):
    """Imprime una fila con los datos de un solo estudiante."""
    print(f"{numero:<4}{estudiante['id']:<8}{estudiante['nombre'][:21]:<22}"
          f"{estudiante['programa'][:25]:<26}{estudiante['promedio']:<6.1f}"
          f"{clasificar_desempeno(estudiante['promedio'])}")


# ==========================================================================
# FUNCIONALIDADES DEL MENÚ
# ==========================================================================
def agregar_estudiante(estudiantes, total_estudiantes):
    """Registra un estudiante nuevo y devuelve el conteo actualizado."""
    print("\n--- AGREGAR ESTUDIANTE ---")
    # Decisión simple: se controla que no se exceda la capacidad máxima.
    if total_estudiantes >= MAX_ESTUDIANTES:
        print(f"  [!] Capacidad máxima alcanzada ({MAX_ESTUDIANTES} estudiantes).")
        return total_estudiantes

    id_nuevo = leer_entero(f"ID del estudiante ({ID_MINIMO} a {ID_MAXIMO}): ",
                           ID_MINIMO, ID_MAXIMO)
    # El ID es la "llave" del sistema: no se permiten dos estudiantes iguales.
    if buscar_posicion(estudiantes, id_nuevo) != -1:
        print(f"  [!] Ya existe un estudiante con el ID {id_nuevo}. No se registró.")
        return total_estudiantes

    nombre = leer_texto("Nombre completo: ")
    programa = leer_texto("Programa académico: ")
    promedio = leer_nota(f"Promedio acumulado ({NOTA_MINIMA} a {NOTA_MAXIMA}): ")

    estudiantes.append({"id": id_nuevo, "nombre": nombre,
                        "programa": programa, "promedio": promedio})
    total_estudiantes += 1      # Variable de CONTEO: total de registrados
    print(f"  [OK] Estudiante registrado. Total actual: {total_estudiantes}")
    return total_estudiantes


def mostrar_estudiantes(estudiantes, total_estudiantes):
    """Muestra la lista completa en el orden de registro (iteración ascendente)."""
    print("\n--- LISTA DE ESTUDIANTES ---")
    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return
    mostrar_encabezado()
    for indice in range(0, total_estudiantes):          # 0, 1, 2, ..., n-1
        mostrar_estudiante(estudiantes[indice], indice + 1)
    print(f"Total de estudiantes: {total_estudiantes}")


def mostrar_inverso(estudiantes, total_estudiantes):
    """Muestra la lista del último registrado al primero (iteración descendente)."""
    print("\n--- ESTUDIANTES EN ORDEN INVERSO (último registrado primero) ---")
    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return
    mostrar_encabezado()
    for indice in range(total_estudiantes - 1, -1, -1):  # n-1, ..., 1, 0
        mostrar_estudiante(estudiantes[indice], indice + 1)


def buscar_estudiante(estudiantes, total_estudiantes):
    """Busca un estudiante por su ID e informa el resultado."""
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")
    if total_estudiantes == 0:
        print("  No hay estudiantes registrados para buscar.")
        return
    id_buscado = leer_entero("Ingrese el ID a buscar: ", ID_MINIMO, ID_MAXIMO)
    posicion = buscar_posicion(estudiantes, id_buscado)
    # Decisión simple: ¿se encontró o no el estudiante?
    if posicion == -1:
        print(f"  [X] No se encontró ningún estudiante con el ID {id_buscado}.")
    else:
        print("  [OK] Estudiante encontrado:")
        mostrar_encabezado()
        mostrar_estudiante(estudiantes[posicion], posicion + 1)


def mostrar_ranking(estudiantes, total_estudiantes):
    """Muestra los estudiantes del mayor al menor promedio."""
    print("\n--- RANKING POR PROMEDIO (de mayor a menor) ---")
    if total_estudiantes == 0:
        print("  No hay estudiantes registrados todavía.")
        return
    ranking = ordenar_por_promedio(estudiantes)
    mostrar_encabezado()
    for puesto in range(1, total_estudiantes + 1):   # El número indica el puesto
        mostrar_estudiante(ranking[puesto - 1], puesto)


def eliminar_estudiante(estudiantes, total_estudiantes):
    """Elimina un estudiante por su ID y devuelve el conteo actualizado."""
    print("\n--- ELIMINAR ESTUDIANTE ---")
    if total_estudiantes == 0:
        print("  No hay estudiantes registrados para eliminar.")
        return total_estudiantes
    id_buscado = leer_entero("Ingrese el ID a eliminar: ", ID_MINIMO, ID_MAXIMO)
    posicion = buscar_posicion(estudiantes, id_buscado)
    if posicion == -1:
        print(f"  [X] No se encontró ningún estudiante con el ID {id_buscado}.")
        return total_estudiantes
    mostrar_encabezado()
    mostrar_estudiante(estudiantes[posicion], posicion + 1)
    # Decisión anidada: solo se pide confirmación si el estudiante existe.
    if confirmar("¿Confirma que desea eliminar este registro?"):
        eliminado = estudiantes.pop(posicion)
        total_estudiantes -= 1      # El CONTEO también disminuye
        print(f"  [OK] Se eliminó a {eliminado['nombre']}. "
              f"Total actual: {total_estudiantes}")
    else:
        print("  Operación cancelada. No se eliminó ningún registro.")
    return total_estudiantes


def mostrar_estadisticas(estudiantes, total_estudiantes):
    """Calcula estadísticas del grupo recorriendo la lista UNA sola vez."""
    print("\n--- ESTADÍSTICAS DEL GRUPO ---")
    if total_estudiantes == 0:
        print("  No hay datos suficientes para calcular estadísticas.")
        return
    suma_promedios = 0.0        # Variable de SUMATORIA (acumulador)
    aprobados = 0               # Variable de CONTEO
    mejor = estudiantes[0]
    # Diccionario de CONTEOS: un contador por cada nivel de desempeño
    distribucion = {"Excelente": 0, "Sobresaliente": 0, "Aceptable": 0, "En riesgo": 0}
    for estudiante in estudiantes:
        suma_promedios += estudiante["promedio"]
        distribucion[clasificar_desempeno(estudiante["promedio"])] += 1
        if estudiante["promedio"] >= NOTA_APROBATORIA:
            aprobados += 1
        if estudiante["promedio"] > mejor["promedio"]:
            mejor = estudiante
    promedio_general = suma_promedios / total_estudiantes
    print(f"{'Estudiantes registrados':<26}: {total_estudiantes}")
    print(f"{'Suma de promedios':<26}: {suma_promedios:.1f}")
    print(f"{'Promedio general':<26}: {promedio_general:.3f}")
    print(f"{f'Aprobados (>= {NOTA_APROBATORIA})':<26}: {aprobados}")
    print(f"{f'En riesgo (< {NOTA_APROBATORIA})':<26}: {total_estudiantes - aprobados}")
    print(f"{'Mejor promedio':<26}: {mejor['nombre']} ({mejor['promedio']:.1f})")
    print("Distribución por desempeño:")
    for nivel, cantidad in distribucion.items():
        print(f"  {nivel:<24}: {cantidad} {'#' * cantidad}")


def mostrar_menu():
    """Imprime las opciones del menú principal."""
    print("\n" + LINEA)
    print("        SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print(LINEA)
    print("  1. Agregar estudiante")
    print("  2. Mostrar lista de estudiantes")
    print("  3. Buscar estudiante por ID")
    print("  4. Mostrar lista en orden inverso")
    print("  5. Ver ranking por promedio")
    print("  6. Ver estadísticas del grupo")
    print("  7. Eliminar estudiante")
    print("  8. Salir del sistema")
    print(LINEA)


# ==========================================================================
# PROGRAMA PRINCIPAL
# ==========================================================================
def main():
    estudiantes = []            # Lista donde se almacenan los registros
    total_estudiantes = 0       # Variable de CONTEO
    bandera_salir = False       # BANDERA que controla el ciclo principal

    print("Bienvenido al SGE. Capacidad máxima:", MAX_ESTUDIANTES, "estudiantes.")

    # Repetición condicionada al comienzo: el menú se repite mientras el
    # usuario no haya confirmado que desea salir.
    while not bandera_salir:
        mostrar_menu()
        opcion = leer_entero("Seleccione una opción (1-8): ", 1, 8)

        # Decisión múltiple: dirige el flujo a la opción elegida.
        match opcion:
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes, total_estudiantes)
            case 4:
                mostrar_inverso(estudiantes, total_estudiantes)
            case 5:
                mostrar_ranking(estudiantes, total_estudiantes)
            case 6:
                mostrar_estadisticas(estudiantes, total_estudiantes)
            case 7:
                total_estudiantes = eliminar_estudiante(estudiantes, total_estudiantes)
            case 8:
                bandera_salir = confirmar("¿Seguro que desea salir?")
            case _:
                # Caso por defecto: no debería ocurrir porque leer_entero ya
                # valida el rango, pero se deja como protección adicional.
                print("  [!] Opción no reconocida.")

    print(f"\nGracias por usar el SGE. Estudiantes registrados al cierre: {total_estudiantes}")
    print("¡Hasta pronto!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Si el usuario cierra con Ctrl+C, se termina con un mensaje amable
        # en lugar de mostrar un error técnico.
        print("\n\nEjecución interrumpida por el usuario. ¡Hasta pronto!")
