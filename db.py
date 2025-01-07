import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
from app import app
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, Length, ValidationError


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'


db = SQLAlchemy()
db.init_app(app)

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

    def populate_lists(self, user_ids):
        users = []
        for id in user_ids:
            if id > 0: users.append(db.session.get(users, id))
        self.users = users

    #def __init__(self, username, password):
    #    self.username = username
    #    self.password = password

class RegisterForm(FlaskForm):
    username = StringField(validators=[input_required(),Length(
        min=3, max=15)], render_kw={"placeholder": "Nutzername"})
    password = PasswordField(validators=[input_required(),Length(
        min=3, max=15)], render_kw={"placeholder": "Passwort"})    
    submit = SubmitField("Registrieren")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Der Name ist vergeben. Bitte nehme einen anderen.')
        
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           input_required(), Length(min=4, max=20)], render_kw={"placeholder": "Nutzername"})

    password = PasswordField(validators=[
                            input_required(), Length(min=3, max=20)], render_kw={"placeholder": "Passwort"})

    submit = SubmitField('Anmelden')

with app.app_context():
    db.create_all()

@click.command('init-db')
def init():  
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo('Database has been initialized.')

app.cli.add_command(init)  # (2.)

def insert_sample(): #Diese Methode funktioniert noch nicht, ich weiß nicht warum
    
    db.session.execute(db.delete(User))


    # Sample Daten die Passwörter sind nicht bcrypted, was dazu führt, dass sie nicht richtig geprüft werden können, wegen dem derzeitigen Aufbau des codes/ Diese Methode sollte nicht benutzt werden
    # user1 = User(username = 'Nayon', password= '1')
    # user2 = User(username = 'Mert', password= '12')
    # user3 = User(username = 'Anil', password= '123')
    # user4 = User(username = 'Tamer', password= '1234')
    # user5 = User(username = 'Anas', password= '12345') 


   
    # db.session.add_all([user1, user2, user3, user4, user5])
    # db.session.commit()