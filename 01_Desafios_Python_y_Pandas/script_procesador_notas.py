import statistics

# 1. Funciones de Entrada
def obtener_datos_estudiante():
    nombre = input("Ingrese el nombre del estudiante: ")
    
    # Validación de la nota 1
    while True:
        try:
            nota1 = float(input("Ingrese la primera nota (1.0 a 7.0): "))
            if 1.0 <= nota1 <= 7.0:
                break
            print("Error: La nota debe estar entre 1.0 y 7.0. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            
    # Validación de la nota 2
    while True:
        try:
            nota2 = float(input("Ingrese la segunda nota (1.0 a 7.0): "))
            if 1.0 <= nota2 <= 7.0:
                break
            print("Error: La nota debe estar entre 1.0 y 7.0. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            
    # Validación de la nota 3
    while True:
        try:
            nota3 = float(input("Ingrese la tercera nota (1.0 a 7.0): "))
            if 1.0 <= nota3 <= 7.0:
                break
            print("Error: La nota debe estar entre 1.0 y 7.0. Intente nuevamente.")
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            
    return nombre, nota1, nota2, nota3

# 2. Funciones de Cálculo
def calcular_promedio(nota1, nota2, nota3):
    return (nota1 + nota2 + nota3) / 3.0

def determinar_estado(promedio):
    if promedio >= 4.0:
        return "Aprobado"
    else:
        return "Reprobado"

# 3. Uso del Módulo statistics
def mostrar_estadisticas(nota1, nota2, nota3):
    notas = [nota1, nota2, nota3]
    mediana = statistics.median(notas)
    try:
        moda = statistics.mode(notas)
    except statistics.StatisticsError:
        # En caso de que no haya una moda única (las 3 notas sean distintas), se asume la primera nota.
        moda = notas[0]
    desviacion = statistics.stdev(notas)
    
    print("\n--- Estadísticas de las Notas ---")
    print(f"Mediana: {mediana:.1f}")
    print(f"Moda: {moda:.1f}")
    print(f"Desviación Estándar: {desviacion:.1f}")
    
    return mediana, moda, desviacion

# 4. Presentación de Resultados
def mostrar_resumen(nombre, nota1, nota2, nota3, promedio, estado, mediana, moda, desviacion):
    print("\n=========================================")
    print("      RESUMEN DE PROCESAMIENTO DE NOTAS   ")
    print("=========================================")
    print(f"Nombre del estudiante: {nombre}")
    print(f"Notas ingresadas: {nota1:.1f}, {nota2:.1f}, {nota3:.1f}")
    print(f"Promedio obtenido: {promedio:.1f}")
    print(f"Estado final: {estado}")
    print("-----------------------------------------")
    print(f"Mediana de las notas: {mediana:.1f}")
    print(f"Nota más frecuente (Moda): {moda:.1f}")
    print(f"Desviación estándar: {desviacion:.1f}")
    print("=========================================")

# Ejecución del programa
if __name__ == "__main__":
    print("Procesador de Notas Académicas")
    print("------------------------------")
    
    # 1. Entrada de datos
    nombre, nota1, nota2, nota3 = obtener_datos_estudiante()
    
    # 2. Cálculos
    promedio = calcular_promedio(nota1, nota2, nota3)
    estado = determinar_estado(promedio)
    
    # 3. Estadísticas
    mediana, moda, desviacion = mostrar_estadisticas(nota1, nota2, nota3)
    
    # 4. Resumen final
    mostrar_resumen(nombre, nota1, nota2, nota3, promedio, estado, mediana, moda, desviacion)
