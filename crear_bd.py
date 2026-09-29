import pymysql

# Crea solo la base de datos; las tablas las crea SQLAlchemy con db.create_all()
conexion = pymysql.connect(host="localhost", user="root", password="root")

try:
    with conexion.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS usuarios_app")
    conexion.commit()
    print("Base de datos 'usuarios_app' lista.")
finally:
    conexion.close()
