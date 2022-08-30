from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import dotenv_values
from routes.mesa_route import mesa_Module

config = dotenv_values('.env') #instanciamos las variables de entonro
app = Flask(__name__)
cors = CORS(app)

# registramos Blue print
app.register_blueprint(mesa_Module, url_prefix="/mesa")  # Url_prefix = path


@app.route('/')
def hello_word():
    dictToReturn = {'message': 'Hola mundirilijillo'}
    return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run(host='localhost', port=config["PORT"], debug=True)
