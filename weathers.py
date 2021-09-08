import sqlite3
from flask_restful import Resource,reqparse
import requests

url="http://api.openweathermap.org/data/2.5/weather?q={}&appid=b5455fb37b7f7b962c60388cc1ede5da"
class Tempratures(Resource):
    global url
    def get(self,city):
        try:
            self.city_name=url.format(city)

            req=requests.get(self.city_name).json()
            min_temp=req['main']['temp_min']
            max_temp=req['main']['temp_max']
            min_temp-=273
            max_temp-=273

            return {"min_temp":"{:.2f}".format(min_temp),"max_temp":"{:.2f}".format(max_temp)}
        except:
            return {"message":"No such city exists in this planet"},404


class Weather(Resource):
    global url

    def get(self,city):
        name=self.find_by_name(city)
        if name is None:
            return {"message":"city not found"},404
        try:
            self.city_name=url.format(name[city])

            req=requests.get(self.city_name).json()
            #print(req['coord'])

            return requests.get(self.city_name).json()
        except:
            return {"message":"No such city exists in this planet"},404

    @classmethod
    def find_by_name(cls,city):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM cities WHERE city=?"
        result=cursor.execute(query,(city,))
        row=result.fetchone()
        connection.close()
        if row:
            return {city:row[1]}
        return None


    def post(self,city):
        if self.find_by_name(city):
            return {"message":"'{}' alredy in list".format(city)},400
        self.city_name=url.format(city)

        if requests.get(self.city_name).json()==None:
            return {"message":"No such city exists"},400
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="INSERT INTO cities VALUES(NULL,?)"
        cursor.execute(query,(city,))
        connection.commit()
        connection.close()
        return {"message":"'{}' added".format(city)},201

    def delete(self,city):
        if self.find_by_name(city):
            connection=sqlite3.connect('data.db')
            cursor=connection.cursor()
            query="DELETE FROM  cities WHERE city=?"
            cursor.execute(query,(city,))
            connection.commit()
            connection.close()
            return {"message":"city deleted from list"}
        return {"message":"city not found in list"}


class AllWeather(Resource):

    def get(self):
        global url
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM cities"
        result=cursor.execute(query)
        weather_list=[]
        for city in result:
            self.city_name=url.format(city[1])

            req=requests.get(self.city_name).json()
            #print(req['coord'])
            weather_list.append({city[1]:req})

            #return requests.get(self.city_name).json()
        connection.close()
        return {"AllWeather":weather_list}
