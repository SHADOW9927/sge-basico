# Sistema de Gestión de Estudiantes (SGE) básico

Aplicación de consola desarrollada en Python para el curso **Algoritmos y Programación**
de la Fundación Universitaria Compensar (Actividad 4, Etapa de Profundización).

**Autor:** Joseth David Moreno Duarte

## Funcionalidades

1. Agregar estudiante (ID, nombre, programa académico y promedio de 0.0 a 5.0)
2. Mostrar la lista completa de estudiantes
3. Buscar un estudiante por ID
4. Mostrar la lista en orden inverso
5. Ver el ranking por promedio (ordenamiento burbuja optimizado con bandera)
6. Ver estadísticas del grupo (promedio general, aprobados y en riesgo, mejor promedio y distribución por desempeño)
7. Eliminar un estudiante (con confirmación)
8. Salir del sistema (con confirmación)

## Requisitos

- Python 3.10 o superior (se usa la estructura `match-case`)

## Cómo ejecutarlo

```bash
python sge.py
```

## Conceptos aplicados

- **Decisiones:** simples, dobles, anidadas y múltiples (`if`, `if-else`, `if-elif-else`, `match-case`)
- **Repeticiones:** `while` condicionado al comienzo, `while True` como repetición condicionada al final
  (equivalente a `do-while`), `for` con iteración ascendente y descendente, y ciclos `for` anidados
- **Variables especiales:** conteo (`total_estudiantes`, `aprobados`, diccionario `distribucion`), sumatoria
  (`suma_promedios`) y banderas (`bandera_salir`, `encontrado`, `hubo_intercambio`)
- **Estructura de datos:** lista de diccionarios con capacidad máxima controlada (`MAX_ESTUDIANTES = 50`)
- **Validación y manejo de errores:** `try-except` para entradas no numéricas, rangos, campos vacíos,
  IDs duplicados e interrupción con Ctrl+C
- **Funciones reutilizables:** cada opción del menú y cada tipo de lectura tiene su propia función
