# main.py
# =====================================================================
# SISTEMA DE GESTIÓN DE TORNEO DE VIDEOJUEGOS RETRO - "PIXELES RETRO"
# =====================================================================
# Este archivo contiene todo el programa en un único script autocontenido,
# diseñado con conceptos básicos de Python (funciones, listas, diccionarios
# y ciclos) ideales para un nivel de estudiante.

import statistics

# =====================================================================
# 1. ENTRADA Y VALIDACIÓN DE DATOS
# =====================================================================

def validar_nombre(nombre_str):
    """
    Valida que el nombre del participante no esté vacío.
    Retorna el nombre limpio (sin espacios al inicio o final).
    """
    if not nombre_str:
        raise ValueError("Error: El nombre no puede estar vacío.")
    
    nombre_limpio = nombre_str.strip()
    if nombre_limpio == "":
        raise ValueError("Error: El nombre no puede estar compuesto únicamente por espacios.")
    
    return nombre_limpio

def validar_edad(edad_str):
    """
    Valida que la edad sea un número entero y se encuentre entre 12 y 70 años.
    Retorna la edad convertida a entero.
    """
    try:
        edad = int(edad_str)
    except ValueError:
        raise ValueError("Error: La edad ingresada debe ser un número entero válido.")
    
    if edad < 12 or edad > 70:
        raise ValueError("Error: La edad debe estar entre 12 y 70 años (inclusive).")
    
    return edad

def validar_nivel(nivel_str):
    """
    Valida que el nivel de experiencia sea un número entero entre 1 y 5.
    Retorna el nivel convertido a entero.
    """
    try:
        nivel = int(nivel_str)
    except ValueError:
        raise ValueError("Error: El nivel debe ser un número entero válido.")
    
    if nivel < 1 or nivel > 5:
        raise ValueError("Error: El nivel de experiencia debe ser un número entero entre 1 y 5 (inclusive).")
    
    return nivel


# =====================================================================
# 2. GESTIÓN DE PARTICIPANTES Y EQUIPOS (LÓGICA)
# =====================================================================

def registrar_participante(participantes, nombre, edad, nivel):
    """
    Registra un nuevo participante en la lista.
    Valida que el nombre no esté duplicado (insensible a mayúsculas).
    """
    # Buscar si ya existe un participante con el mismo nombre
    for p in participantes:
        if p["nombre"].lower() == nombre.lower():
            raise ValueError(f"Error: Ya existe un participante registrado con el nombre '{nombre}'.")
    
    nuevo = {
        "nombre": nombre,
        "edad": edad,
        "nivel": nivel,
        "equipo": None  # Inicialmente no pertenece a ningún equipo
    }
    participantes.append(nuevo)
    return nuevo

def crear_equipo(equipos, participantes, nombre_equipo, jugador1_nombre, jugador2_nombre):
    """
    Crea un nuevo equipo de 2 jugadores.
    Valida:
    - Que el nombre del equipo sea único.
    - Que ambos jugadores existan.
    - Que ambos jugadores estén disponibles (no tengan equipo asignado).
    - Que el jugador 1 y el jugador 2 no sean la misma persona.
    """
    # 1. Validar que el nombre del equipo no esté duplicado
    for eq_name in equipos:
        if eq_name.lower() == nombre_equipo.lower():
            raise ValueError(f"Error: Ya existe un equipo registrado con el nombre '{nombre_equipo}'.")
    
    # 2. Validar que no sea el mismo jugador
    if jugador1_nombre.lower() == jugador2_nombre.lower():
        raise ValueError("Error: Un equipo debe estar conformado por dos personas distintas.")
    
    # 3. Buscar a los jugadores en la lista de participantes y validar su disponibilidad
    j1 = None
    j2 = None
    
    for p in participantes:
        if p["nombre"].lower() == jugador1_nombre.lower():
            j1 = p
        if p["nombre"].lower() == jugador2_nombre.lower():
            j2 = p

    if j1 is None:
        raise ValueError(f"Error: El participante '{jugador1_nombre}' no está registrado.")
    if j2 is None:
        raise ValueError(f"Error: El participante '{jugador2_nombre}' no está registrado.")
        
    if j1["equipo"] is not None:
        raise ValueError(f"Error: El jugador '{j1['nombre']}' ya forma parte del equipo '{j1['equipo']}'.")
    if j2["equipo"] is not None:
        raise ValueError(f"Error: El jugador '{j2['nombre']}' ya forma parte del equipo '{j2['equipo']}'.")
    
    # 4. Asignar el equipo a los jugadores
    j1["equipo"] = nombre_equipo
    j2["equipo"] = nombre_equipo
    
    # 5. Crear la estructura del equipo
    nuevo_equipo = {
        "nombre": nombre_equipo,
        "integrantes": [j1["nombre"], j2["nombre"]],
        "puntos": 0
    }
    
    equipos[nombre_equipo] = nuevo_equipo
    return nuevo_equipo


# =====================================================================
# 3. REGISTRO Y ANÁLISIS DE PARTIDAS
# =====================================================================

def registrar_partida(partidas, equipos, equipo_a_nombre, equipo_b_nombre, ganador_nombre):
    """
    Registra el resultado de una partida entre dos equipos.
    Asigna 3 puntos al equipo ganador e ingresa la partida al historial.
    """
    # Validar existencia de equipos
    eq_a = None
    eq_b = None
    
    for eq_name in equipos:
        if eq_name.lower() == equipo_a_nombre.lower():
            eq_a = equipos[eq_name]
        if eq_name.lower() == equipo_b_nombre.lower():
            eq_b = equipos[eq_name]
            
    if eq_a is None:
        raise ValueError(f"Error: El equipo '{equipo_a_nombre}' no existe en el torneo.")
    if eq_b is None:
        raise ValueError(f"Error: El equipo '{equipo_b_nombre}' no existe en el torneo.")
        
    if eq_a["nombre"].lower() == eq_b["nombre"].lower():
        raise ValueError("Error: Un equipo no puede jugar contra sí mismo.")
        
    # Validar que el ganador sea uno de los contendientes
    if ganador_nombre.lower() not in (eq_a["nombre"].lower(), eq_b["nombre"].lower()):
        raise ValueError("Error: El ganador de la partida debe ser uno de los dos equipos participantes.")
        
    # Obtener el nombre oficial del ganador para sumar puntos
    nombre_ganador_oficial = eq_a["nombre"] if ganador_nombre.lower() == eq_a["nombre"].lower() else eq_b["nombre"]
    
    # Sumar 3 puntos al equipo ganador
    equipos[nombre_ganador_oficial]["puntos"] += 3
    
    # Guardar partida en el historial
    nueva_partida = {
        "partida_numero": len(partidas) + 1,
        "equipo_a": eq_a["nombre"],
        "equipo_b": eq_b["nombre"],
        "ganador": nombre_ganador_oficial
    }
    partidas.append(nueva_partida)
    return nueva_partida

def obtener_promedio_puntos(equipos):
    """
    Calcula el promedio de puntos por equipo usando el modulo statistics.
    Si no hay equipos registrados, retorna 0.0.
    """
    if not equipos:
        return 0.0
    
    puntos_lista = [eq["puntos"] for eq in equipos.values()]
    return statistics.mean(puntos_lista)

def obtener_mediana_puntos(equipos):
    """
    Calcula la mediana de puntos de los equipos usando statistics.
    """
    if not equipos:
        return 0.0
        
    puntos_lista = [eq["puntos"] for eq in equipos.values()]
    return statistics.median(puntos_lista)

def obtener_desviacion_puntos(equipos):
    """
    Calcula la desviación estándar de los puntos usando statistics.
    Requiere al menos 2 equipos para calcularse, de lo contrario retorna 0.0.
    """
    if len(equipos) < 2:
        return 0.0
        
    puntos_lista = [eq["puntos"] for eq in equipos.values()]
    return statistics.stdev(puntos_lista)

def calcular_rendimiento_equipo(puntos_equipo, promedio):
    """
    Calcula el rendimiento de un equipo en base a la diferencia con el promedio.
    """
    return puntos_equipo - promedio


# =====================================================================
# 4. REPORTES Y CIERRE
# =====================================================================

def mostrar_cabecera(titulo):
    """
    Imprime un título decorado al estilo arcade retro.
    """
    ancho = 60
    print("=" * ancho)
    print(f"| {titulo.upper():^{ancho - 4}} |")
    print("=" * ancho)

def reporte_participantes(participantes):
    """
    Muestra la lista de participantes registrados en un formato de tabla clara.
    """
    mostrar_cabecera("Lista de Participantes Registrados")
    
    if not participantes:
        print("  No hay participantes registrados en el torneo actualmente.")
        print("=" * 60)
        return
        
    print(f"{'Nombre':<22} | {'Edad':<6} | {'Nivel Exp.':<10} | {'Equipo':<15}")
    print("-" * 60)
    
    for p in participantes:
        nombre = p["nombre"]
        edad = p["edad"]
        nivel = p["nivel"]
        equipo = p["equipo"] if p["equipo"] else "Sin equipo"
        print(f"{nombre:<22} | {edad:<6} | {nivel:<10} | {equipo:<15}")
        
    print("=" * 60)
    print(f"Total registrados: {len(participantes)} jugadores.")
    print("=" * 60)
    print()

def reporte_equipos(equipos):
    """
    Muestra la lista de equipos formados con sus integrantes.
    """
    mostrar_cabecera("Equipos Formados en el Torneo")
    
    if not equipos:
        print("  No hay equipos formados en el torneo actualmente.")
        print("=" * 60)
        return
        
    print(f"{'Equipo':<20} | {'Integrante 1':<18} | {'Integrante 2':<18}")
    print("-" * 60)
    
    for eq in equipos.values():
        nombre_eq = eq["nombre"]
        int1 = eq["integrantes"][0]
        int2 = eq["integrantes"][1]
        print(f"{nombre_eq:<20} | {int1:<18} | {int2:<18}")
        
    print("=" * 60)
    print(f"Total de equipos: {len(equipos)}")
    print("=" * 60)
    print()

def obtener_puntos_equipo(equipo):
    """
    Función de ayuda para ordenar los equipos por sus puntos.
    """
    return equipo["puntos"]

def reporte_ranking(equipos):
    """
    Muestra la tabla de clasificación ordenada de mayor a menor puntaje.
    Incluye estadísticas globales al final.
    """
    mostrar_cabecera("Ranking Actual de Equipos")
    
    if not equipos:
        print("  No hay equipos registrados para calcular el ranking.")
        print("=" * 60)
        return
        
    # Convertir dict de equipos a una lista para ordenarla
    lista_equipos = list(equipos.values())
    
    # Ordenar de mayor a menor usando la función auxiliar
    lista_equipos_ordenada = sorted(lista_equipos, key=obtener_puntos_equipo, reverse=True)
    
    # Calcular promedio de puntos global para la comparación de rendimiento
    promedio_global = obtener_promedio_puntos(equipos)
    
    print(f"{'Pos':<4} | {'Equipo':<20} | {'Puntos':<8} | {'Rendimiento vs Promedio':<22}")
    print("-" * 60)
    
    posicion = 1
    for eq in lista_equipos_ordenada:
        nombre = eq["nombre"]
        puntos = eq["puntos"]
        
        # Rendimiento: diferencia con el promedio global
        rendimiento = calcular_rendimiento_equipo(puntos, promedio_global)
        rendimiento_str = f"{rendimiento:+.1f} pts" if rendimiento != 0 else "Promedio exacto"
        
        print(f"{posicion:<4} | {nombre:<20} | {puntos:<8} | {rendimiento_str:<22}")
        posicion += 1
        
    print("=" * 60)
    
    # Estadísticas adicionales con el módulo statistics
    mediana = obtener_mediana_puntos(equipos)
    desviacion = obtener_desviacion_puntos(equipos)
    
    print(f"Estadísticas Generales del Torneo:")
    print(f"  - Promedio de puntos: {promedio_global:.2f} pts")
    print(f"  - Mediana de puntos:  {mediana:.2f} pts")
    if len(equipos) >= 2:
        print(f"  - Desviación estándar: {desviacion:.2f} pts")
    else:
        print(f"  - Desviación estándar: N/A (Se necesitan al menos 2 equipos)")
    print("=" * 60)
    print()


# =====================================================================
# 5. MENÚ INTERACTIVO Y FLUJO PRINCIPAL
# =====================================================================

def mostrar_menu():
    """
    Imprime el menú de opciones del sistema con un diseño estilo retro.
    """
    print("\n" + "=" * 50)
    print("│         PIXELES RETRO - MENÚ DE TORNEO           │")
    print("=" * 50)
    print("  1. Registrar Participante")
    print("  2. Formar Equipo (2 Jugadores)")
    print("  3. Registrar Resultado de Partida")
    print("  4. Consultar Integrantes de un Equipo")
    print("  5. Reporte: Lista de Participantes")
    print("  6. Reporte: Lista de Equipos Formados")
    print("  7. Reporte: Ranking y Estadísticas del Torneo")
    print("  8. Mostrar Historial de Partidas Jugadas")
    print("  9. Salir del Sistema")
    print("=" * 50)

def main():
    # Inicialización de las estructuras de datos (Python Básico)
    participantes = []  # Lista de diccionarios: [{"nombre": str, "edad": int, "nivel": int, "equipo": str/None}]
    equipos = {}        # Diccionario indexado por nombre del equipo: {nombre: {"nombre": str, "integrantes": [str, str], "puntos": int}}
    partidas = []       # Lista de diccionarios con el historial: [{"partida_numero": int, "equipo_a": str, "equipo_b": str, "ganador": str}]

    print("¡Bienvenido al Sistema de Gestión de Torneo de Pixeles Retro!")
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-9): ").strip()
        print() # Espacio en blanco para mejorar legibilidad
        
        if opcion == "1":
            # --- REGISTRAR PARTICIPANTE ---
            print(">>> REGISTRO DE NUEVO PARTICIPANTE <<<")
            
            # Validar nombre
            while True:
                nombre_raw = input("Ingrese nombre del participante: ")
                try:
                    nombre = validar_nombre(nombre_raw)
                    break
                except ValueError as e:
                    print(e)
            
            # Validar edad
            while True:
                edad_raw = input("Ingrese edad (12 a 70 años): ")
                try:
                    edad = validar_edad(edad_raw)
                    break
                except ValueError as e:
                    print(e)
            
            # Validar nivel
            while True:
                nivel_raw = input("Ingrese nivel de experiencia (1 al 5): ")
                try:
                    nivel = validar_nivel(nivel_raw)
                    break
                except ValueError as e:
                    print(e)
            
            # Intentar agregar al torneo
            try:
                registrar_participante(participantes, nombre, edad, nivel)
                print(f"\n¡Éxito! Participante '{nombre}' registrado correctamente.")
            except ValueError as e:
                print(e)

        elif opcion == "2":
            # --- FORMAR EQUIPO ---
            print(">>> FORMACIÓN DE EQUIPOS BALANCEDADOS <<<")
            
            # Mostrar jugadores que no tienen equipo para ayudar al usuario
            jugadores_disponibles = []
            for p in participantes:
                if p["equipo"] is None:
                    jugadores_disponibles.append(p["nombre"])
                    
            if len(jugadores_disponibles) < 2:
                print("Error: No hay suficientes jugadores disponibles sin equipo (se necesitan al menos 2).")
                continue
                
            print(f"Jugadores registrados disponibles para formar equipo: {len(jugadores_disponibles)}")
            for j in jugadores_disponibles:
                # Buscar información de nivel del jugador para mostrar al usuario
                for p in participantes:
                    if p["nombre"] == j:
                        print(f"  - {p['nombre']} (Nivel de Exp: {p['nivel']})")
            
            # Pedir nombre del equipo
            while True:
                nombre_equipo = input("\nIngrese un nombre único para el equipo: ").strip()
                if nombre_equipo == "":
                    print("Error: El nombre del equipo no puede estar vacío.")
                else:
                    break
            
            # Pedir integrantes
            jugador1 = input("Ingrese el nombre del primer integrante: ").strip()
            jugador2 = input("Ingrese el nombre del segundo integrante: ").strip()
            
            try:
                equipo_creado = crear_equipo(equipos, participantes, nombre_equipo, jugador1, jugador2)
                print(f"\n¡Éxito! Equipo '{equipo_creado['nombre']}' formado con éxito.")
                print(f"Integrantes: {equipo_creado['integrantes'][0]} y {equipo_creado['integrantes'][1]}.")
            except ValueError as e:
                print(e)

        elif opcion == "3":
            # --- REGISTRAR PARTIDA ---
            print(">>> REGISTRO DE PARTIDA ARCADE <<<")
            
            if len(equipos) < 2:
                print("Error: Se necesitan al menos 2 equipos formados para jugar una partida.")
                continue
                
            print("Equipos listos para competir:")
            for eq_name in equipos:
                print(f"  - {eq_name}")
                
            equipo_a = input("\nIngrese nombre del primer equipo: ").strip()
            equipo_b = input("Ingrese nombre del segundo equipo: ").strip()
            ganador = input("Ingrese el nombre del equipo ganador: ").strip()
            
            try:
                partida = registrar_partida(partidas, equipos, equipo_a, equipo_b, ganador)
                print(f"\n¡Éxito! Partida registrada.")
                print(f"El equipo '{partida['ganador']}' suma 3 puntos en la clasificación.")
            except ValueError as e:
                print(e)

        elif opcion == "4":
            # --- CONSULTAR EQUIPO ---
            print(">>> CONSULTA DE EQUIPO <<<")
            
            if not equipos:
                print("No hay equipos creados en el torneo aún.")
                continue
                
            busqueda = input("Ingrese el nombre del equipo que desea consultar: ").strip()
            
            # Buscar coincidencia (insensible a mayúsculas)
            equipo_encontrado = None
            for eq_name, eq_data in equipos.items():
                if eq_name.lower() == busqueda.lower():
                    equipo_encontrado = eq_data
                    break
                    
            if equipo_encontrado:
                print("\n" + "-" * 40)
                print(f"Equipo: {equipo_encontrado['nombre']}")
                print(f"Puntos Acumulados: {equipo_encontrado['puntos']} pts")
                print("Integrantes:")
                for integrante in equipo_encontrado["integrantes"]:
                    # Buscar nivel del integrante
                    nivel_int = 0
                    for p in participantes:
                        if p["nombre"] == integrante:
                            nivel_int = p["nivel"]
                    print(f"  - {integrante} (Nivel de Exp: {nivel_int})")
                print("-" * 40)
            else:
                print(f"Error: El equipo '{busqueda}' no existe en el sistema.")

        elif opcion == "5":
            # --- REPORTE PARTICIPANTES ---
            reporte_participantes(participantes)

        elif opcion == "6":
            # --- REPORTE EQUIPOS ---
            reporte_equipos(equipos)

        elif opcion == "7":
            # --- REPORTE RANKING ---
            reporte_ranking(equipos)

        elif opcion == "8":
            # --- HISTORIAL DE PARTIDAS ---
            mostrar_cabecera("Historial de Partidas")
            
            if not partidas:
                print("  Aún no se han jugado partidas en el torneo.")
                print("=" * 60)
                continue
                
            print(f"{'Partida N°':<12} | {'Enfrentamiento':<30} | {'Ganador':<15}")
            print("-" * 60)
            
            for p in partidas:
                n = p["partida_numero"]
                enfrentamiento = f"{p['equipo_a']} vs {p['equipo_b']}"
                ganador = p["ganador"]
                print(f"{n:<12} | {enfrentamiento:<30} | {ganador:<15}")
                
            print("=" * 60)
            print(f"Total de partidas disputadas: {len(partidas)}")
            print("=" * 60)
            print()

        elif opcion == "9":
            # --- SALIDA ---
            print("Guardando datos de sesión y cerrando...")
            print("¡Gracias por utilizar el sistema de Pixeles Retro!")
            break
            
        else:
            print("Opción inválida. Por favor ingrese un número del 1 al 9.")
            
        # Pausa para que el usuario pueda leer antes de refrescar el menú
        input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    main()
