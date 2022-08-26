from unicodedata import name
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_word():
    dictToReturn = {'message':'Hola mundirilijillo'}
    return jsonify(dictToReturn)
    