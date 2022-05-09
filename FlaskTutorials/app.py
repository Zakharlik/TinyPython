from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Some home text'

@app.route('/about')
def about():
    return 'Some about'

if __name__ == '__main__':
    app.run(debug=True)
    