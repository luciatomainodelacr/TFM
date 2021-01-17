######PRUEBA CON LAS FUNCIONES AUXILIARES PARA MODELO AVANZADO######

#Import libraries
import sys
import pandas as pd
import numpy as np

import funcion_aux as fa

#Main function
if __name__ == "__main__":
    
#    if len(sys.argv) != 2:
#        print("ERROR: This program needs at least 2 parameters: program_name program_type")
#        sys.exit(1)
#    else:
        # print("The number of arguments is ", len(sys.argv))
        # program_name = sys.argv[0]
        # program_type = sys.argv[1]
        # print("The program run is: ",program_name, program_type)

    
    d_distancias = {"origen": ["Albacete Tren", "Caceres Tren","Alicante Tren"], "destino": ["Caceres Tren", "Alicante Tren", "Zaragoza Tren"], "distancia": [510.915, 674.844, 490.975]}
    df_distancias = pd.DataFrame(data=d_distancias)
    distancias = df_distancias["distancia"]
    d_punto_recarga = {"punto_recarga": ["Caceres Tren", "Alicante Tren"], "numero_conectores": [3, 5]}
    df_punto_recarga = pd.DataFrame(data=d_punto_recarga)
    numero_conectores_pc = df_punto_recarga["numero_conectores"]
    velocidad = 100 # km/h
    carga = 1 # h
    autonomia_coche = 190 #km
    tiempo_viaje = fa.funcion_objetivo_tiempo(distancias, velocidad, carga, numero_conectores_pc)
    restricciones_autonomia = fa.restriccion_autonomia(distancias,autonomia_coche)
    print ("El tiempo de viaje es: ", tiempo_viaje, "horas")
    print ("Las restricciones de autonomía son: ", restricciones_autonomia)