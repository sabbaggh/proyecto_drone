from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from geopy import distance
from generar_puntos import generar_malla

#esquina_sup_izq, esquina_sup_der, esquina_inf_izq, esquina_inf_der = (20.432822, -99.599167), (20.432822, -99.599031), (20.432735, -99.599167), (20.432735, -99.599031)

prueba = [
    (20.432822, -99.599167), 
    (20.432822, -99.599031), 
    (20.432735, -99.599167), 
    (20.432735, -99.599031)
]

puntos_generados = generar_malla(prueba)

# Conexión al SITL (despues se cambiaria por la pixhawk)
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# ----------------------------
# 1) Despegar a 3 m
arm_and_takeoff(3)


normal = 1
# ----------------------------
#Ciclo for para recorrer todos los puntos
for puntos in puntos_generados:
    puntos_totales = len(puntos)
    for i in range(puntos_totales):
        # 2) Definimos un punto GPS al que ir
        #Definir si el recorrido actual es de inicio a fin o de fin a inicio
        ##Se hace un objeto de ubicacion de dronekit con las coordenadas y la altitud
        if normal % 2 == 0:
            target_location = LocationGlobalRelative(puntos[-i-1][0],puntos[-i-1][1], 3)  #Ejemplo en el rancho de Aron
            print(f"Flying to target location {(puntos[-i-1][0],puntos[-i-1][1])}")
        else:
            target_location = LocationGlobalRelative(puntos[i][0],puntos[i][1], 3)
            print(f"Flying to target location {(puntos[i][0],puntos[i][1])}")
        
        #Hacer que el dron vuele al punto objetivo
        vehicle.simple_goto(target_location)

        #Ciclo while para esperar a que llegue al punto (tolerancia de 50 cm)
        while True:

            #Obtener locacion actual del UAV
            current_location = vehicle.location.global_relative_frame

            #Calcular distancia entre la locacion actual y la objetivo 
            distance_curr_target = distance.distance(
                    (current_location.lat, current_location.lon), 
                    (target_location.lat, target_location.lon)
                ).meters
            print(f"Distancia al punto {i}: {distance_curr_target:.2f} m")

            #Verificar si la distancia entre los puntos es menor o igual a 0.5m
            if distance_curr_target <= 0.5:  
                print(f"Llegó al punto {i}")
                #Dejar al dron volando durante 3 segundos en ese punto
                time.sleep(3)
                ## Aqui podriamos poner que tome las fotos

                break
    #Se le aumenta 1 a normal para que en la siguiente iteracion se determine el tipo de recorrido (inicio a fin o fin a inicio)
    normal += 1
        

# Mantener el script vivo un rato para que pueda volar
time.sleep(4)

# ----------------------------
# 3) Regresar y aterrizar
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Cerrar conexión
vehicle.close()
