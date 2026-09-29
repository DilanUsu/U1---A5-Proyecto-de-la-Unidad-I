class Config:
    SECRET_KEY = "cambia-esta-clave-secreta"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/usuarios_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
