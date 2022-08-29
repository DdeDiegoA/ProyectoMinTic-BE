from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import dotenv_values

config = dotenv_values('.env')
app = Flask(__name__)


@app.route('/')
def hello_word():
    dictToReturn = {'message': 'Hola mundirilijillo'}
    return jsonify(dictToReturn)


print(__name__)

if __name__ == '__main__':
    app.run(host='localhost', port=config["PORT"], debug=True)
