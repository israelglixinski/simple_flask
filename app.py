from flask import Flask
import db_mongo


app = Flask(__name__)

@app.route('/')
def home():
    return db_mongo.encontrar_pertinentes()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
