from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adata.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(120), unique=True, nullable=False)
    group_id = db.Column(db.Integer,  db.ForeignKey('group.id'))
    level = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    depart_id = db.Column(db.Integer, db.ForeignKey('depart.id'))

    def __repr__(self):
        return '<User %r>' % self.name

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    users = db.relationship("User", backref="group", lazy=True)

    def __repr__(self):
        return '<Group %r>' % self.name

class Depart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    users = db.relationship("User", backref="depart", lazy=True)

    def __repr__(self):
        return '<Depart %r>' % self.name

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    groups = db.relationship("Group", backref="faculty", lazy=True)
    departs = db.relationship("Depart", backref="faculty", lazy=True)

    def __repr__(self):
        return '<Faculty %r>' % self.name