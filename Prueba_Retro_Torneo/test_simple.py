# test_simple.py
# Script de pruebas automatizadas simples para verificar la lógica del torneo (Versión autocontenida)

import main

def probar_validaciones():
    print("Corriendo pruebas de validación...")
    
    # Pruebas de Nombre
    assert main.validar_nombre("Lucas") == "Lucas"
    assert main.validar_nombre("  Lucas Gomez  ") == "Lucas Gomez"
    try:
        main.validar_nombre("")
        assert False, "Debería lanzar error por nombre vacío"
    except ValueError:
        pass
        
    try:
        main.validar_nombre("   ")
        assert False, "Debería lanzar error por espacios"
    except ValueError:
        pass

    # Pruebas de Edad
    assert main.validar_edad("12") == 12
    assert main.validar_edad("70") == 70
    assert main.validar_edad("35") == 35
    try:
        main.validar_edad("11")
        assert False, "Debería lanzar error por edad menor a 12"
    except ValueError:
        pass
        
    try:
        main.validar_edad("71")
        assert False, "Debería lanzar error por edad mayor a 70"
    except ValueError:
        pass
        
    try:
        main.validar_edad("abc")
        assert False, "Debería lanzar error por edad no numérica"
    except ValueError:
        pass

    # Pruebas de Nivel
    assert main.validar_nivel("1") == 1
    assert main.validar_nivel("5") == 5
    assert main.validar_nivel("3") == 3
    try:
        main.validar_nivel("0")
        assert False, "Debería lanzar error por nivel menor a 1"
    except ValueError:
        pass
        
    try:
        main.validar_nivel("6")
        assert False, "Debería lanzar error por nivel mayor a 5"
    except ValueError:
        pass
        
    try:
        main.validar_nivel("xyz")
        assert False, "Debería lanzar error por nivel no numérico"
    except ValueError:
        pass

    print("-> Pruebas de validación aprobadas con éxito!\n")

def probar_torneo():
    print("Corriendo pruebas de lógica de torneo...")
    
    # Inicializar datos vacíos
    participantes = []
    equipos = {}
    partidas = []
    
    # 1. Registrar participantes
    main.registrar_participante(participantes, "Mario", 30, 5)
    main.registrar_participante(participantes, "Luigi", 28, 4)
    main.registrar_participante(participantes, "Bowser", 45, 3)
    main.registrar_participante(participantes, "Peach", 25, 5)
    
    assert len(participantes) == 4
    
    # Intentar registrar duplicado (insensible a mayúsculas)
    try:
        main.registrar_participante(participantes, "mario", 20, 2)
        assert False, "Debería fallar por nombre duplicado"
    except ValueError:
        pass
        
    # 2. Crear equipos
    # Equipo A
    main.crear_equipo(equipos, participantes, "Los Plomeros", "Mario", "Luigi")
    assert "Los Plomeros" in equipos
    assert equipos["Los Plomeros"]["puntos"] == 0
    assert equipos["Los Plomeros"]["integrantes"] == ["Mario", "Luigi"]
    
    # Verificar que el estado del participante se actualizó
    for p in participantes:
        if p["nombre"] in ["Mario", "Luigi"]:
            assert p["equipo"] == "Los Plomeros"
            
    # Intentar registrar equipo con el mismo nombre
    try:
        main.crear_equipo(equipos, participantes, "los plomeros", "Bowser", "Peach")
        assert False, "Debería fallar por nombre de equipo duplicado"
    except ValueError:
        pass
        
    # Intentar registrar equipo con jugador ya ocupado
    try:
        main.crear_equipo(equipos, participantes, "Los Malos", "Mario", "Bowser")
        assert False, "Debería fallar porque Mario ya está en un equipo"
    except ValueError:
        pass
        
    # Equipo B (exitoso)
    main.crear_equipo(equipos, participantes, "El Reino Champiñon", "Bowser", "Peach")
    assert "El Reino Champiñon" in equipos
    
    # 3. Registrar partidas y validar puntos
    # Partida 1: Plomeros vs Reino Champiñon. Ganador: Plomeros
    main.registrar_partida(partidas, equipos, "Los Plomeros", "El Reino Champiñon", "Los Plomeros")
    assert equipos["Los Plomeros"]["puntos"] == 3
    assert equipos["El Reino Champiñon"]["puntos"] == 0
    assert len(partidas) == 1
    
    # Partida 2: Plomeros vs Reino Champiñon. Ganador: Reino Champiñon
    main.registrar_partida(partidas, equipos, "Los Plomeros", "El Reino Champiñon", "El Reino Champiñon")
    assert equipos["Los Plomeros"]["puntos"] == 3
    assert equipos["El Reino Champiñon"]["puntos"] == 3
    assert len(partidas) == 2
    
    # 4. Probar estadísticas
    promedio = main.obtener_promedio_puntos(equipos)
    assert promedio == 3.0
    
    mediana = main.obtener_mediana_puntos(equipos)
    assert mediana == 3.0
    
    # Añadir una partida más para romper el empate
    # Partida 3: Plomeros gana
    main.registrar_partida(partidas, equipos, "Los Plomeros", "El Reino Champiñon", "Los Plomeros")
    assert equipos["Los Plomeros"]["puntos"] == 6
    assert equipos["El Reino Champiñon"]["puntos"] == 3
    
    promedio_nuevo = main.obtener_promedio_puntos(equipos)
    assert promedio_nuevo == 4.5
    
    desviacion = main.obtener_desviacion_puntos(equipos)
    # stdev([6, 3]) = 2.1213...
    assert abs(desviacion - 2.1213) < 0.001
    
    # Rendimiento
    rendimiento_plomeros = main.calcular_rendimiento_equipo(equipos["Los Plomeros"]["puntos"], promedio_nuevo)
    assert rendimiento_plomeros == 1.5
    
    print("-> Pruebas de lógica de torneo aprobadas con éxito!\n")

def main_test():
    print("=== INICIANDO PRUEBAS UNITARIAS SIMPLES ===")
    probar_validaciones()
    probar_torneo()
    print("=== TODAS LAS PRUEBAS SE PASARON CORRECTAMENTE ===")

if __name__ == "__main__":
    main_test()
