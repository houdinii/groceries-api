import os

from flask import Flask
from flask_migrate import Migrate

from api import api
from models import db
from schema import ma

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'groceries.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

api.init_app(app)

ma.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
