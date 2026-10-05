import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from models import db
from routes.users import users_bp

# Carga las variables del archivo .env (que NO se sube a Git)
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.environ['DB_USER']}:{quote_plus(os.environ['DB_PASSWORD'])}"
    f"@{os.environ.get('DB_HOST', 'localhost')}/{os.environ.get('DB_NAME', 'app_db')}"
)

db.init_app(app)
CSRFProtect(app)
app.register_blueprint(users_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
