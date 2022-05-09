from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crjurnal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-container-type', methods=['POST', 'GET'])
def add_container_type():
    cont_types = container_types.query.order_by(container_types.title).all()
    if request.method == 'POST':
        title = request.form['title']
        is_present = False
        for el in cont_types:
            if title == str(el.title):
                is_present = True
                return 'Такой контейнер уже есть!'
            else:
                is_present = False
        if is_present:
            cont_type = container_types(title=title)
            try:
                db.session.add(cont_type)
                db.session.commit()
                return redirect('/add-container-type')
            except Exception as e:
                return "Ошибка записи в БД: " + str(e)

    return render_template('add-container-type.html', cont_types=cont_types)




if __name__ == '__main__':
    app.run(debug=True)