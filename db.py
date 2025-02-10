import click
from flask import json
from flask_sqlalchemy import SQLAlchemy as sa
import werkzeug
from app import app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, Length, ValidationError, EqualTo


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


db = sa()
db.init_app(app)

@click.command('init-db')
def init():  
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo('Database has been initialized.')

app.cli.add_command(init)  


class Report(db.Model):
    id = db.Column("ID", db.Integer, primary_key = True, autoincrement=True)
    file = db.Column("Reportfile",db.LargeBinary, nullable=False)
    parent_id = db.mapped_column(db.ForeignKey("user.id"))
    parent = db.relationship("User", back_populates="children")
    

    
  


login_manager = LoginManager() 
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), nullable=False, unique=True)
    password = db.Column("password", db.String(80), nullable=False)
    children = db.relationship("Report", back_populates="parent")


    def populate_lists(self, user_ids):
        users = []
        for id in user_ids:
            if id > 0: users.append(db.session.get(users, id))
        self.users = users


class RegisterForm(FlaskForm):
    username = StringField(validators=[input_required(),Length(
        min=3, max=15)], render_kw={"placeholder": "Nutzername"})
    password = PasswordField(validators=[input_required(),Length(
        min=3, max=15)], render_kw={"placeholder": "Passwort"})   
    confirmPw = PasswordField(validators=[input_required(),Length(
        min=3, max=15), EqualTo('password', message='Passwörter stimmen nicht überein')], render_kw={"placeholder": "Passwort bestätigen"})   
    submit = SubmitField("Registrieren")

    def validate_username(self, username):
        userRow =  db.session.execute(db.select(User).filter_by(username = username.data)).first()
        existing_user_username = userRow[0]
        #existing_user_username = User.query.filter_by(
        #   username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Der Name ist vergeben. Bitte nehme einen anderen.')
    
        
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           input_required(), Length(min=4, max=20)], render_kw={"placeholder": "Nutzername"})

    password = PasswordField(validators=[
                            input_required(), Length(min=3, max=20)], render_kw={"placeholder": "Passwort"})

    submit = SubmitField('Anmelden') 

    def validate_username(self, username):
        userRow = db.session.execute(
            db.select(User).filter_by(username=username.data)
        ).first()
        
        if not userRow:
            raise ValidationError('Nutzer existiert nicht.')

        self.user = userRow[0]  # Speichert das Benutzerobjekt im Formular für spätere Verwendung

    # Prüft, ob das Passwort korrekt ist
    def validate_password(self, password):
        if not hasattr(self, 'user'):  
            return  # Falls `validate_username` fehlschlägt, nicht weiter prüfen

        if not werkzeug.security.check_password_hash(self.user.password, password.data):
            raise ValidationError('Passwort ist falsch.')


