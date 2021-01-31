# -*- coding: utf-8 -*-
import pandas as pd

class Restricciones(object):
    """
    Atributos:
    ------------
    restriccion_tipo_conector:           Pandas Dataframe
    restricciones_prim_par:              Pandas Dataframe
    restricciones_ult_par:               Pandas Dataframe
    
    Metodos:
    ------------
    constructor:                        __init__(self,...)
    str:                                __str__(self)
    restriccion_tipo_conector:         restriccion_tipo_conector(self)
    restriccion_primera_parada:        restriccion_primera_parada(self)
    restriccion_ultima_parada:         restriccion_ultima_parada(self)
    """
    def __init__(self):
        """
        Definicion del constructor _init_:
        ----------
        Funcion que inicializa los atributos del objeto

        Parametros
        ----------
        self:                  Restricciones
            objeto instanciado de la clase
        
        Returns
        ------
        Al ser el constructor de una clase, no existe return como tal, si no 
        que se asigna el valor a los atributos del objeto de la clase (self)
    
        Ejemplo
        -------
        >>> restriccion = Restricciones()
        """
        
        columnas_tipo_conector = ["Origen","Destino","Restr_con"]
        self.restriccion_tipo_conector = pd.DataFrame(columns = columnas_tipo_conector)

        columnas_primera_parada = ["Origen","Destino","Restr_prim_par"]
        self.restricciones_prim_par = pd.DataFrame(columns = columnas_primera_parada)

        columnas_ultima_parada = ["Origen","Destino","Restr_ult_par"]
        self.restricciones_ult_par = pd.DataFrame(columns = columnas_ultima_parada)

    def __str__(self):
        """
        Definicion de la sobrecarga del str:
        ----------
        Funcion de escritura de los atributos del objeto
    
        Parametros
        ----------
        self:                  Restricciones
            objeto instanciado de la clase
        
        Returns
        ------
        string 
            Informacion sobre los atributos de la base de datos
    
        Ejemplo
        -------
        >>> restriccion = Restricciones()
        >>> print(restriccion)  
        """
        
        return ("Restricciones: "
                + str(self.restriccion_tipo_conector) + ", "
                + str(self.restricciones_prim_par) + ", "
                + str(self.restricciones_ult_par))  

    def restriccion_tipo_conector(self, distancias, puntoscarga_reduced):
         """
        Definicion del metodo restriccion_tipo_conector:
            
            Funcion de aplicar las restriccione tipo conector
    
        Parametros
        ----------
        self:                  Restricciones
            objeto instanciado de la clase

        distancias:            Pandas Dataframe
            Dataframe que contiene los resultados de la query
        
        puntoscarga_reduced:   list[string]
            Lista de string que contiene los id de los puntos de carga
            con el tipo de conector necesario
        
        Returns
        ------
        En este metodo de la clase, no existe return como tal, si no 
        que se asigna un valor al atributo existencias del objeto (self)
        
        Ejemplo
        -------
        >>> restriccion = Restricciones()
        >>> print(restriccion)  
        >>> restriccion.restriccion_tipo_conector()
        """

         restriccion_tipo_conector = []
         for index, distancia in distancias.iterrows():
            if ("punto_recarga" in distancia["Origen"]) & ("punto_recarga" in distancia["Destino"]):
                if (distancia["Origen"] in puntoscarga_reduced) & (distancia["Destino"] in puntoscarga_reduced):
                    restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],True))
                else:
                    restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],False))
            else:
                if (distancia["Origen"] in puntoscarga_reduced) | (distancia["Destino"] in puntoscarga_reduced):
                    restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],True))
                else:
                    restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],False))
        #column_names = ["Origen","Destino","Restr_con"]
        #restriccion_tipo_conector_df = pd.DataFrame(data = restriccion_tipo_conector, columns = column_names)
         self.restriccion_tipo_conector.append(data = restriccion_tipo_conector)

    def restriccion_primera_parada(self, distancias_origen, carga_inicial, autonomia_coche):
         """
        Definicion del metodo restriccion_primera_parada:
            
            Funcion de aplicar la restriccion de primera parada
    
        Parametros
        ----------
        self:                  Restricciones
            objeto instanciado de la clase

        distancias_origen:     Pandas Dataframe
            Dataframe que contiene las distancias desde el origen
        
        carga_inicial:         float
            Porcentaje de carga inicial del coche al iniciar el viaje
        
        autonomia_coche:       float
            Autonomia del coche 
        
        Returns
        ------
        En este metodo de la clase, no existe return como tal, si no 
        que se asigna un valor al atributo existencias del objeto (self)
        
        Ejemplo
        -------
        >>> restriccion = Restricciones()
        >>> print(restriccion)  
        >>> restriccion.restriccion_primera_parada()
        """

         restriccion_primera_parada = []
         for index, distancia in distancias_origen.iterrows():
            if (float(distancia["Distance_km"]) - 0.9 * autonomia_coche * carga_inicial / 100) <= 0:
                restriccion_primera_parada.append((distancia["Origen"],distancia["Destino"],True))
            else:
                restriccion_primera_parada.append((distancia["Origen"],distancia["Destino"],False))
         #column_names = ["Origen","Destino","Restr_prim_par"]
         #restriccion_primera_parada_df = pd.DataFrame(data = restriccion_primera_parada, columns = column_names)
         self.restricciones_prim_par.append(data = restriccion_primera_parada)

    def restriccion_ultima_parada(self, distancias_destino, carga_final, autonomia_coche):
         """
        Definicion del metodo restriccion_ultima_parada:
            
            Funcion de aplicar la restriccion de ultima parada
    
        Parametros
        ----------
        self:                  Restricciones
            objeto instanciado de la clase

        distancias_destino:     Pandas Dataframe
            Dataframe que contiene las distancias desde el destino
        
        carga_final:            float
            Porcentaje de carga final del coche al iniciar el viaje

        autonomia_coche:        float
            Autonomia del coche        
         
        Returns
        ------
        En este metodo de la clase, no existe return como tal, si no 
        que se asigna un valor al atributo existencias del objeto (self)
        
        Ejemplo
        -------
        >>> restriccion = Restricciones()
        >>> print(restriccion)  
        >>> restriccion.restriccion_ultima_parada()
        """

         restriccion_ultima_parada = []
         for index, distancia in distancias_destino.iterrows():
            if (float(distancia["Distance_km"]) - ((100 - carga_final) / 100 * 0.9 * autonomia_coche)) <= 0:
                restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],True))
            else:
                restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],False))
        #column_names = ["Origen","Destino","Restr_ult_par"]
        #restriccion_ultima_parada_df = pd.DataFrame(data = restriccion_ultima_parada, columns = column_names)
         self.restricciones_ult_par.append(data = restriccion_ultima_parada)