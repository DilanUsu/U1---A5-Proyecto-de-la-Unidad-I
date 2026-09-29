from flask_sqlalchemy import SQLAlchemy

# Instancia compartida para evitar imports circulares
db = SQLAlchemy()
