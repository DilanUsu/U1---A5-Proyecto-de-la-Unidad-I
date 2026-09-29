from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, session

from extensions import db
from models.user import User
from forms.user_forms import RegisterForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return decorated


@users_bp.route("/")
def index():
    usuarios = User.query.order_by(User.created_at.desc()).all()
    return render_template("user_list.html", usuarios=usuarios)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usuario = User(username=form.username.data, email=form.email.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("users.login"))
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
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html", form=form)


@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("users.index"))


@users_bp.route("/profile/<int:id>")
def profile(id):
    usuario = User.query.get_or_404(id)
    return render_template("profile.html", usuario=usuario)


@users_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    if session["user_id"] != id:
        flash("No tienes permiso para editar este perfil.", "error")
        return redirect(url_for("users.profile", id=id))

    usuario = User.query.get_or_404(id)
    form = EditProfileForm(obj=usuario)

    if form.validate_on_submit():
        # Evita duplicados con otros usuarios (excluyendo al propio)
        if User.query.filter(User.username == form.username.data, User.id != id).first():
            form.username.errors.append("Ese nombre de usuario ya está en uso.")
        elif User.query.filter(User.email == form.email.data, User.id != id).first():
            form.email.errors.append("Ese correo ya está en uso.")
        else:
            usuario.username = form.username.data
            usuario.email = form.email.data
            db.session.commit()
            flash("Perfil actualizado correctamente.", "success")
            return redirect(url_for("users.profile", id=id))

    return render_template("edit_profile.html", form=form, usuario=usuario)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    if session["user_id"] != id:
        flash("No tienes permiso para eliminar este perfil.", "error")
        return redirect(url_for("users.profile", id=id))

    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    session.clear()
    flash("Tu cuenta ha sido eliminada.", "success")
    return redirect(url_for("users.index"))
