#!/bin/bash

# Copiar la carpeta de ElectricRoute dentro de la de Docker
cp -r ../ElectricRoute/flask_auth_app/project app/.

mkdir app/project/BE/
cp -r ../Python/calcular_caminos_entre_puntos.py app/project/BE/.
cp -r ../Python/Modelo app/project/BE/.
cp -r ../Python/Output app/project/BE/.
