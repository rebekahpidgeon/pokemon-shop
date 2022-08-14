from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ece44c8fc979b2e412e5267bb5d927116dadc8caf4c55d11'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21052836:Thepidgeonfamily10@csmysql.cs.cf.ac.uk:3306/c21052836_cm1102_shop'

db = SQLAlchemy(app)

from shop import routes

