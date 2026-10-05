import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

# Solo crea la base de datos; las tablas las crea db.create_all() en app.py
nombre_bd = os.environ.get("DB_NAME", "app_db")
conexion = pymysql.connect(
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
)
conexion.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{nombre_bd}`")
conexion.close()
print(f"Base de datos {nombre_bd} lista.")
