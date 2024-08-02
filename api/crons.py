from models import LecturaRaspberry, LecturaEsp32, DiarioLecturaRaspberry, SemanaLecturaRaspberry, MesLecturaRaspberry, DiarioLecturaEsp32, MesLecturaEsp32

from django.db.models import Avg, Sum
from datetime import datetime, timedelta

# Función auxiliar para saber si es el último día del mes
def es_ultimo_dia(fecha):
    ultimo_dia = (fecha.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    return fecha.day == ultimo_dia.day


def registrar_lectura_diaria_raspberry():
    hoy = datetime.now().date()
    
    # Crear objetos datetime para el inicio y el final del día
    inicio_dia = datetime.combine(hoy, datetime.min.time())
    fin_dia = datetime.combine(hoy, datetime.max.time())


    # Modificar la consulta para filtrar por rango de fechas
    ids_raspberry = LecturaRaspberry.objects.filter(fecha=hoy).values_list('idRaspberry', flat=True).distinct()

    for id_raspberry in ids_raspberry:

        # Calcular promedios y suma para cada idRaspberry
        promedios_y_suma = LecturaRaspberry.objects.filter(
            fecha__range=(inicio_dia, fin_dia), 
            idRaspberry=id_raspberry
        ).aggregate(
            promedio_humedad_ambiente=Avg('humedad_ambiente'),
            promedio_temperatura_ambiente=Avg('temperatura_ambiente'),
            promedio_radiacion_solar=Avg('radiacion_solar'),
            promedio_presion_atmosferica=Avg('presion_atmosferica'),
            promedio_velocidad_viento=Avg('velocidad_viento'),
            suma_et0=Sum('et0')
        )
        
        # Crear un registro en DiarioLecturaRaspberry para cada idRaspberry
        DiarioLecturaRaspberry.objects.create(
            fecha=hoy,
            idRaspberry=id_raspberry,
            humedad_ambiente=promedios_y_suma['promedio_humedad_ambiente'],
            temperatura_ambiente=promedios_y_suma['promedio_temperatura_ambiente'],
            radiacion_solar=promedios_y_suma['promedio_radiacion_solar'],
            presion_atmosferica=promedios_y_suma['promedio_presion_atmosferica'],
            velocidad_viento=promedios_y_suma['promedio_velocidad_viento'],
            et0=promedios_y_suma['suma_et0']
        )



def registrar_lectura_diaria_esp32():
    hoy = datetime.now().date()
    nombre_dia = datetime.now().weekday()

    # Crear objetos datetime para el inicio y el final del día
    inicio_dia = datetime.combine(hoy, datetime.min.time())
    fin_dia = datetime.combine(hoy, datetime.max.time())

    # Identificar todos los idEsp32 únicos que tienen registros para hoy
    ids_esp32 = LecturaEsp32.objects.filter(fecha=hoy).values_list('idEsp32', flat=True).distinct()

    for id_esp32 in ids_esp32:
        # Calcular promedios y suma para cada idEsp32
        promedios_y_suma = LecturaEsp32.objects.filter(
            fecha__range=(inicio_dia, fin_dia), 
            idEsp32=id_esp32
        ).aggregate(
            promedio_humedad_suelo=Avg('humedad_suelo'),
        )
        
        # Crear un registro en DiarioLecturaEsp32 para cada idEsp32
        DiarioLecturaEsp32.objects.create(
            fecha=hoy,
            idEsp32=id_esp32,
            dia = nombre_dia,
            humedad_suelo=promedios_y_suma['promedio_humedad_suelo'],
        )



def registrar_lectura_semanal_raspberry():
    hoy = datetime.now()
    hace_siete_dias = hoy - timedelta(days=7)

    # Identificar todos los idRaspberry únicos que tienen registros en el rango de fechas
    ids_raspberry = DiarioLecturaRaspberry.objects.filter(fecha__range=[hace_siete_dias, hoy]).values_list('idRaspberry', flat=True).distinct()
        
    for id_raspberry in ids_raspberry:
        # Calcular promedios para cada idRaspberry
        promedios = DiarioLecturaRaspberry.objects.filter(
            fecha__range=[hace_siete_dias, hoy], 
            idRaspberry=id_raspberry
        ).aggregate(
            promedio_humedad_ambiente=Avg('humedad_ambiente'),
            promedio_temperatura_ambiente=Avg('temperatura_ambiente'),
            promedio_radiacion_solar=Avg('radiacion_solar'),
            promedio_presion_atmosferica=Avg('presion_atmosferica'),
            promedio_velocidad_viento=Avg('velocidad_viento'),
            promedio_et0=Avg('et0')
        )
        
        # Obtener el número de la semana actual
        numero_semana = datetime.now().isocalendar()[1]
        
        # Crear un registro en SemanaLecturaRaspberry para cada idRaspberry
        SemanaLecturaRaspberry.objects.create(
            semana=numero_semana,
            idRaspberry=id_raspberry,
            humedad_ambiente=promedios['promedio_humedad_ambiente'],
            temperatura_ambiente=promedios['promedio_temperatura_ambiente'],
            radiacion_solar=promedios['promedio_radiacion_solar'],
            presion_atmosferica=promedios['promedio_presion_atmosferica'],
            velocidad_viento=promedios['promedio_velocidad_viento'],
            et0=promedios['promedio_et0']
        )

def registrar_lectura_mensual_raspberry():
    hoy = datetime.now()
    inicio_mes = datetime(hoy.year, hoy.month, 1)
    mes = hoy.month

    # Función auxiliar para saber si es el último día del mes
    def es_ultimo_dia(fecha):
        ultimo_dia = (fecha.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        return fecha.day == ultimo_dia.day

    if es_ultimo_dia(hoy):
        # Identificar todos los idRaspberry únicos que tienen registros en el rango de fechas
        ids_raspberry = DiarioLecturaRaspberry.objects.filter(fecha__range=[inicio_mes, hoy]).values_list('idRaspberry', flat=True).distinct()
            
        for id_raspberry in ids_raspberry:

            # Calcular promedios para cada idRaspberry
            promedios = DiarioLecturaRaspberry.objects.filter(
                fecha__range=[inicio_mes, hoy], 
                idRaspberry=id_raspberry
            ).aggregate(
                promedio_humedad_ambiente=Avg('humedad_ambiente'),
                promedio_temperatura_ambiente=Avg('temperatura_ambiente'),
                promedio_radiacion_solar=Avg('radiacion_solar'),
                promedio_presion_atmosferica=Avg('presion_atmosferica'),
                promedio_velocidad_viento=Avg('velocidad_viento'),
                promedio_et0=Avg('et0')
            )
                    
            # Crear un registro en MesLecturaRaspberry para cada idRaspberry
            MesLecturaRaspberry.objects.create(
                mes=mes,
                idRaspberry=id_raspberry,
                humedad_ambiente=promedios['promedio_humedad_ambiente'],
                temperatura_ambiente=promedios['promedio_temperatura_ambiente'],
                radiacion_solar=promedios['promedio_radiacion_solar'],
                presion_atmosferica=promedios['promedio_presion_atmosferica'],
                velocidad_viento=promedios['promedio_velocidad_viento'],
                et0=promedios['promedio_et0']
            )

    

def registrar_lectura_mensual_esp32():
    hoy = datetime.now()
    inicio_mes = datetime(hoy.year, hoy.month, 1)
    mes = hoy.month

    # Función auxiliar para saber si es el último día del mes
    def es_ultimo_dia(fecha):
        ultimo_dia = (fecha.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        return fecha.day == ultimo_dia.day

    if es_ultimo_dia(hoy):

        # Identificar todos los idEsp32 únicos que tienen registros en el rango de fechas
        ids_esp32 = DiarioLecturaEsp32.objects.filter(fecha__range=[inicio_mes, hoy]).values_list('idEsp32', flat=True).distinct()
            
        for id_esp32 in ids_esp32:

            # Calcular promedios para cada idEsp32
            promedios = DiarioLecturaEsp32.objects.filter(
                fecha__range=[inicio_mes, hoy], 
                idEsp32=id_esp32
            ).aggregate(
                promedio_humedad_suelo=Avg('humedad_suelo'),
            )
                    
            # Crear un registro en MesLecturaEsp32 para cada idEsp32
            MesLecturaEsp32.objects.create(
                mes=mes,
                idEsp32=id_esp32,
                humedad_suelo=promedios['promedio_humedad_suelo'],
            )
