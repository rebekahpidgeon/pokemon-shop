from datetime import datetime
from email.policy import default
from flask_login import UserMixin
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ecological_impact = db.Column(db.Text, nullable=False)
    carbon_footprint = db.Column(db.Float, nullable=False)
    origins = db.Column(db.Text, nullable=False)
    provider = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.png')

    def __repr__(self):
        return f"Item('{self.name}', '{self.price}', '{self.description}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password,password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





