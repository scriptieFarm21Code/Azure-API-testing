import sys
import matplotlib.pyplot as plt
import mysql.connector
from pymongo import MongoClient
from weatherApi import getWeatherData
from weatherApi import convertTimeStap
from requestPrediction import getPrediction

client = MongoClient('mongodb://localhost:27017/')
farm21DB = mysql.connector.connect(
    host="127.0.0.1",
    user="homestead",
    password="secret",
    database="homestead"
)
sensorId = 100
cursor = farm21DB.cursor(dictionary=True, buffered=True)

db = client.weatherDataFarm21

mongoItem = list(db.readingDataRaw.find({'sensorId': sensorId}).sort('_id', -1).limit(1))
latestID = mongoItem[0]['readingId']
# latestID = 248597

# Get latest Items
cursor.execute(f"SELECT * FROM readings WHERE id > {latestID} AND sensor_id = {sensorId} LIMIT 72")
result = cursor.fetchall()

for newReading in result:

    predictionData = getWeatherData(newReading['measured_at'], newReading['latitude'], newReading['longitude'])
    predictionData['soil_moisture_10'] = float(newReading['soil_moisture_10'])
    predictionData['soil_moisture_20'] = float(newReading['soil_moisture_20'])
    predictionData['soil_moisture_30'] = float(newReading['soil_moisture_30'])
    predictionData['soil_temperature'] = float(newReading['soil_temperature'])
    predictionData['lat'] = float(newReading['latitude'])
    predictionData['long'] = float(newReading['longitude'])
    predictionData['sensorId'] = int(newReading['sensor_id'])
    predictionData['readingId'] = int(newReading['id'])
    predictionData['sensorGroupId'] = int(newReading['group_id'])
    predictionData['timestampReading'] = str(newReading['measured_at'])
    predictionData['airTempSensor'] = float(newReading['air_temperature'])
    predictionData['sensorHumidity'] = float(newReading['humidity'])
    predictionData['cropType'] = str(newReading['crop_type'])
    predictionData['cropRace'] = str(newReading['race_type'])
    predictionData['typeField'] = str(newReading['cultivation_type'])
    predictionData['soilTypeId'] = int(newReading['soil_type_id'])
    predictionData['timestampReadingUnix'] = int(convertTimeStap(newReading['measured_at']))
    print(convertTimeStap(newReading['measured_at']))
    prediction = getPrediction(predictionData)
    predictionData['soil_moisture_10_prediction'] = prediction['soilMoistureTen']
    predictionData['soil_moisture_10_perctage'] = prediction['percentage']

    db.filter100.insert(predictionData)
    pass
