from generar_puntos import generar_malla

prueba = [
    (20.432822, -99.599167), 
    (20.432822, -99.599031), 
    (20.432735, -99.599167), 
    (20.432735, -99.599031)
]

puntos_generados = generar_malla(prueba)

print(puntos_generados)

normal = 1

for puntos in puntos_generados:
    puntos_totales = len(puntos)
    for i in range(puntos_totales):
        #Se hace el recorrido al reves
        if normal % 2 == 0:
            print(f"{puntos[-i-1][0]}, {puntos[-i-1][1]}")

        #Se hace el recorrido normal
        else:
            print(f"{puntos[i][0]}, {puntos[i][1]}")
    normal += 1