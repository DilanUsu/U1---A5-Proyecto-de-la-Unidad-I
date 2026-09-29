from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, session

from models import db
from models.user import User
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)


def login_required(f):
    """Exige sesión iniciada y que el usuario sea el dueño del perfil."""
    @wraps(f)
    def wrapper(id):
        if "user_id" not in session:
            flash("Debes iniciar sesión.", "error")
            return redirect(url_for("users.login"))
        if session["user_id"] != id:
            flash("No tienes permiso para modificar este perfil.", "error")
            return redirect(url_for("users.profile", id=id))
        return f(id)
    return wrapper


@users_bp.route("/")
def index():
    return render_template("user_list.html", usuarios=User.query.all())


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usuario = User(username=form.username.data, email=form.email.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("users.login"))
    if form.is_submitted():
        flash("Revisa los datos del registro.", "error")
    return render_template("register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            session["user_id"] = usuario.id
            flash(f"Bienvenido, {usuario.username}.", "success")
            return redirect(url_for("users.profile", id=usuario.id))
    if form.is_submitted():
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html", form=form)


@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("users.index"))


@users_bp.route("/profile/<int:id>")
def profile(id):
    return render_template("profile.html", usuario=User.query.get_or_404(id))


@users_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    usuario = User.query.get_or_404(id)
    form = EditProfileForm(obj=usuario)
    if form.validate_on_submit():
        duplicado = User.query.filter(User.id != id, (User.username == form.username.data)
                                      | (User.email == form.email.data)).first()
        if not duplicado:
            usuario.username = form.username.data
            usuario.email = form.email.data
            db.session.commit()
            flash("Perfil actualizado.", "success")
            return redirect(url_for("users.profile", id=id))
    if form.is_submitted():
        flash("No se pudo actualizar: datos inválidos o ya en uso.", "error")
    return render_template("edit_profile.html", form=form)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    db.session.delete(User.query.get_or_404(id))
    db.session.commit()
    session.clear()
    flash("Cuenta eliminada.", "success")
    return redirect(url_for("users.index"))
