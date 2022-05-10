from app import db
from datetime import datetime


class dev_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

class container_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

class connector_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    num_of_pins = db.Column(db.Integer, nullable=False)
    is_male = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

class containers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cont_type_id = db.Column(db.Integer, db.ForeignKey('connector_types.id'), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey('containers.id'), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
