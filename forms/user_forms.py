from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from models.user import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                    Length(min=3, max=64, message="Debe tener entre 3 y 64 caracteres.")],
    )
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."),
                    Email(message="Correo no válido."),
                    Length(max=120)],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria."),
                    Length(min=6, message="Debe tener al menos 6 caracteres.")],
    )
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(message="Confirma tu contraseña."),
                    EqualTo("password", message="Las contraseñas no coinciden.")],
    )
    submit = SubmitField("Registrarme")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ese nombre de usuario ya está registrado.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Ese correo ya está registrado.")


class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."),
                    Email(message="Correo no válido.")],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria.")],
    )
    submit = SubmitField("Iniciar sesión")


class EditProfileForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                    Length(min=3, max=64, message="Debe tener entre 3 y 64 caracteres.")],
    )
    email = StringField(
        "Correo electrónico",
        validators=[DataRequired(message="El correo es obligatorio."),
                    Email(message="Correo no válido."),
                    Length(max=120)],
    )
    submit = SubmitField("Guardar cambios")
