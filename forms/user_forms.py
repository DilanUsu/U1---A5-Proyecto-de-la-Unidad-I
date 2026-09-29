from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from models.user import User


class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[
        DataRequired(), EqualTo("password", message="Las contraseñas no coinciden.")])
    submit = SubmitField("Registrarme")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ese usuario ya existe.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Ese correo ya existe.")


class LoginForm(FlaskForm):
    email = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")


class EditProfileForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Correo", validators=[DataRequired(), Email()])
    submit = SubmitField("Guardar")
