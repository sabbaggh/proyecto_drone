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

# Conexión al SITL (ajusta el puerto si es necesario)
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



# ----------------------------
#Ciclo for para recorrer todos los puntos
for i in range(len(puntos_generados)):
    # 2) Definimos un punto GPS al que ir
    target_location = LocationGlobalRelative(puntos_generados[i][0],puntos_generados[i][1], 3)  #Ejemplo en el rancho de Aron

    print(f"Flying to target location {puntos_generados[i]}")
    vehicle.simple_goto(target_location)

    # Esperar a que llegue al punto (tolerancia de 50 cm)
    while True:
        current_location = vehicle.location.global_relative_frame
        distance_curr_target = distance.distance(
                (current_location.lat, current_location.lon), 
                (target_location.lat, target_location.lon)
            ).meters
        print(f"Distancia al punto {i}: {distance_curr_target:.2f} m")

        if distance_curr_target <= 0.5:  # tolerancia de llegada
            print(f"Llegó al punto {i}")
            time.sleep(3)
            ## Aqui podriamos poner que tome las fotos

            break
        

# Mantener el script vivo un rato para que pueda volar
time.sleep(4)

# ----------------------------
# 3) Regresar y aterrizar
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Cerrar conexión
vehicle.close()
