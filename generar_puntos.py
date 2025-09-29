
from geopy import distance
def generar_malla(esquinas, step=0.000020):
    """
    Genera una malla de puntos GPS dentro de un rectángulo definido por 4 esquinas.
    
    Parámetros:
        esquinas (list): Lista de 4 tuplas con coordenadas (lat, lon).
        step (float): Paso en grados (default=0.000020 ≈ ~2 m en latitud).
    
    Retorna:
        list: Lista de puntos (lat, lon) dentro de la malla.
    """
    # Determinar los límites
    latitudes = [p[0] for p in esquinas]
    longitudes = [p[1] for p in esquinas]

    lat_min, lat_max = min(latitudes), max(latitudes)
    lon_min, lon_max = min(longitudes), max(longitudes)

    # Generar la malla
    grid_points = []
    lat = lat_min
    while lat <= lat_max:
        lon = lon_min
        while lon <= lon_max:
            grid_points.append((lat, lon))
            lon += step
        lat += step

    return grid_points
