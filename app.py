from flask import Flask
from flask_wtf.csrf import CSRFProtect

from models import db
from routes.users import users_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/app_db"

db.init_app(app)
CSRFProtect(app)
app.register_blueprint(users_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
