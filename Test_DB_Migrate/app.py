from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import inspect
import sys
from db_classes import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crjurnal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route('/add/<string:table_name>', methods=['POST', 'GET'])
def add_any_row(table_name):
    '''
    Admin page for maintenance any table by hand
    '''
    table_rows = globals()[table_name].query.order_by(globals()[table_name].title).all()
    table_columns = tables[table_name]
    if request.method == 'POST':
        title = request.form['title']
        is_present = False
        for el in table_rows:
            if title == str(el.title):
                is_present = True
                return 'Такая запись уже есть!'
        if not is_present:
            new_els = {key: request.form[key] for key in table_columns}
            new_row = globals()[table_name](**new_els)  # Как сюда запихать список полей?
            try:
                db.session.add(new_row)
                db.session.commit()
                return redirect(f'/add/{table_name}')
            except Exception as e:
                return "Ошибка записи в БД: " + str(e)

#    return render_template(f'add/{table_name}.html', cont_types=cont_types)
    return render_template('add/row.html', table_rows=table_rows, table_columns=table_columns, table_name=table_name)


def make_table_list():
    '''
    Make list of usefull columns in dict of tables.
    Some unusefull columns, such as 'id' and 'creation_date', excluded.
    '''

    unuseful = ('id', 'creation_date') # Tuple of unuseful collumns
    result ={}
    classes = [(cls_name, cls_obj) for cls_name, cls_obj in inspect.getmembers(sys.modules['db_classes']) if inspect.isclass(cls_obj)] # List of all classes

    for db_class in classes:
        attributes = []
        for cl in inspect.getmembers(db_class[1]):
            if ('attributes' in str(type(cl[1]))) and (cl[0] not in unuseful): # 'attributes' - property of SQLAlchemy collumns
                attributes.append(cl[0])
        if attributes: # Need for exclude datetime class
            result[db_class[0]] = attributes
    return result        


if __name__ == '__main__':
    tables = make_table_list()
    print(make_table_list())    
    app.run(debug=True)