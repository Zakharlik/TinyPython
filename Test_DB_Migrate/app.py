from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crjurnal.db'
app.config['SQLALCEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class dev_types(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime)

if __name__ == '__main__':
    app.run(debug=True)