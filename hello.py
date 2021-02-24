import flask
from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

pets = [
    {
        'name': 'Miso',
        'owner': 'Mike'
    },
    {
        'name': 'Tuna',
        'owner': 'Liza'
    }
]

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
  
@app.route('/api/pets/all', methods=['GET'])
def api_all():
    return jsonify(pets)
  
app.run()