# -*- coding: utf-8 -*-
import mysql.connector
import pandas as pd

class BaseDatos(object):
    """
    Atributos:
    ------------
    host:           string
    puerto:         int
    usuario:        string
    password:       string
    basedatos:      string
    
    Metodos:
    ------------
    constructor:            __init__(self,...)
    str:                    __str__(self)
    crear_conexion:         crear_conexion(self)
    ejecutar_queries:       ejecutar_queries(self, con, sql_query, columnas, argumentos = ())
    """
    def __init__(self, host, puerto, usuario, password, basedatos):
        """
        Definicion del constructor _init_:
        ----------
        Funcion que inicializa los atributos del objeto

        Parametros
        ----------
        self:                  BaseDatos
            objeto instanciado de la clase
        
        host:                  string
            Nombre del host de la db
        
        puerto:                string
            Puerto de la bd
        
        usuario:               string
            Usuario de la bd
        
        password:              string
            Password de la bd
        
        basedatos:             string
            Nombre de la bd 
        
        Returns
        ------
        Al ser el constructor de una clase, no existe return como tal, si no 
        que se asigna el valor a los atributos del objeto de la clase (self)
    
        Ejemplo
        -------
        >>> bd = BaseDatos(host = "localhost",
                           puerto = 3306,
                           usuario = "root",
                           password = "root",
                           basedatos = "tfm")
        """
        
        self.host = host
        self.puerto = puerto
        self.usuario = usuario
        self.password = password
        self.basedatos = basedatos

    def __str__(self):
        """
        Definicion de la sobrecarga del str:
        ----------
        Funcion de escritura de los atributos del objeto
    
        Parametros
        ----------
        self:                  BaseDatos
            objeto instanciado de la clase
        
        Returns
        ------
        string 
            Informacion sobre los atributos de la base de datos
    
        Ejemplo
        -------
        >>> bd = BaseDatos(host = "localhost",
                           puerto = 3306,
                           usuario = "root",
                           password = "root",
                           basedatos = "tfm") 
        >>> print(bd)  
    
        BaseDatos: localhost, 3306, root, root, tfm
        """
        
        return ("BaseDatos: "
                + str(self.host) + ", "
                + str(self.puerto) + ", "
                + str(self.usuario) + ", "
                + str(self.password) + ", "
                + str(self.basedatos))

    def crear_conexion(self):
         """
        Definicion del metodo crear_conexion:
            
            Funcion de crear conexion a la base de datos ya inicializada
    
        Parametros
        ----------
        self:                  BaseDatos
            objeto instanciado de la clase
        
        Returns
        ------
        con:                   Objeto de tipo mysql.connector.connect
            Conexion a la base de datos inicializada en self
        
        Ejemplo
        -------
        >>> bd = BaseDatos(host = "localhost",
                           puerto = 3306,
                           usuario = "root",
                           password = "root",
                           basedatos = "tfm")
        >>> print(bd)  
    
        BaseDatos: localhost, 3306, root, root, tfm
        
        >>> con = bd.crear_conexion()
        """
        
         con = mysql.connector.connect(host = self.host,
                                       port = self.puerto,            
                                       user = self.usuario,            
                                       password = self.password,        
                                       database = self.basedatos)
         return con
    
    def ejecutar_queries_select(self, con, sql_query, columnas, argumentos = ()):
         """
        Definicion del metodo ejecutar_queries_select:
            
            Funcion de ejecutar queries a la base de datos ya inicializada
    
        Parametros
        ----------
        self:                  BaseDatos
            objeto instanciado de la clase
        
        con:                   Objeto de tipo mysql.connector.connect
            Conexion a la base de datos con funcion crear_conexion()

        sql_query:             string
            SQL query a realizar
        
        columnas:               list[string]
            Lista que contiene el nombre de las columnas del dataframe
        
        argumentos(opcional):   tuple()
            Tupla que contiene los argumentos de las queries
        
        Returns
        ------
        df:                    Pandas Dataframe
            Dataframe que contiene los resultados de la query
        
        Ejemplo
        -------
        >>> bd = BaseDatos(host = "localhost",
                           puerto = 3306,
                           usuario = "root",
                           password = "root",
                           basedatos = "tfm")
        >>> print(bd)  
    
        BaseDatos: localhost, 3306, root, root, tfm
        
        >>> con = bd.crear_conexion()

        >>> sql_query_coche = "SELECT * FROM ElectricCar WHERE BRAND = %s AND MODEL = %s"
            columnas_coche = ["BRAND","MODEL","RANGE_KM","EFFICIENCY_WHKM","FASTCHARGE_KMH","RAPIDCHARGE","PLUGTYPE", "BATTERY_CAPACITY"]
            argumentos_coche= (args.marca_coche, args.modelo_coche)
            df_electricar =  bd.ejecutar_queries(con = con,
                                                 sql_query = sql_query_coche,
                                                 columnas = columnas_coche,
                                                 argumentos = argumentos_coche)
        """

         cur = con.cursor()
         cur.execute(sql_query, argumentos)
         df = pd.DataFrame(cur.fetchall(), columns = columnas)
         return df