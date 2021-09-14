from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from weathers import Tempratures,Weather,AllWeather
import os

app=Flask(__name__)

api=Api(app)



api.add_resource(Weather,'/weather/<string:city>')
api.add_resource(AllWeather,'/AllWeather')
api.add_resource(Tempratures,'/temperatures/<string:city>')

if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
