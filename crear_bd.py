import pymysql

# Solo crea la base de datos; las tablas las crea db.create_all() en app.py
conexion = pymysql.connect(host="localhost", user="root", password="root")
conexion.cursor().execute("CREATE DATABASE IF NOT EXISTS app_db")
conexion.close()
print("Base de datos app_db lista.")
