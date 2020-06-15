import sys
import matplotlib.pyplot as plt
import mysql.connector
from pymongo import MongoClient
import urllib.request
import json

farm21DB = mysql.connector.connect(
    host="127.0.0.1",
    user="homestead",
    password="secret",
    database="homestead"
)

cursor = farm21DB.cursor(dictionary=True, buffered=True)

client = MongoClient('mongodb://localhost:27017/')
db = client.weatherDataFarm21
dbPrediction = client.predictions
predictedData = db.filterNN.find({})


def getPrediction(requestData):
    data = {
        "Inputs": {
            "input1":
            [
                {
                    'temp': requestData['temp'],
                    'airPressure': requestData['airPressure'],
                    'windSpeed': requestData['windSpeed'],
                    'rain': requestData['rain'],
                    'windBearing': requestData['windBearing'],
                    'cloudCover': requestData['cloudCover'],
                    'uvIndex': requestData['uvIndex'],
                    'visibility': requestData['visibility'],
                    'dewPoint': requestData['dewPoint'],
                    'humidity': requestData['humidity'],
                    'apparentTemperature': requestData['apparentTemperature'],
                    'sensorId': requestData['sensorId'],
                    'soil_moisture_10_raw': "",
                    'lat': requestData['lat'],
                    'long': requestData['long'],
                    'soilTypeId': requestData['soilTypeId'],
                    'unixTimestampReading': requestData['timestampReadingUnix'],
                }
            ],
        },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    url = ''
    api_key = ''  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        # print(result)
        result = json.loads(result)
        print(result)
        return {'soilTenRaw': float(result['Results']['output1'][0]['Scored Labels'])}
        # return {'soilTenRaw': float(result['Results']['output1'][0]['Scored Label Mean'])}

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))


def getRawReading(readingId):
    # Get latest Items
    cursor.execute(
        f"SELECT raw.soil_moisture_10, raw.soil_moisture_20, raw.soil_moisture_30 FROM readings JOIN raw_readings AS raw ON readings.raw_reading_id = raw.id WHERE readings.id = {readingId}")
    result = cursor.fetchall()
    return result


for data in predictedData:
    print(data['readingId'])
    prediction = getPrediction(data)
    data['soil_ten_raw'] = prediction['soilTenRaw']
    raw = getRawReading(data['readingId'])
    data['soil_moisture_10_raw'] = float(raw[0]['soil_moisture_10'])
    data['soil_moisture_20_raw'] = float(raw[0]['soil_moisture_20'])
    data['soil_moisture_30_raw'] = float(raw[0]['soil_moisture_30'])
    dbPrediction.tenRawPredictionNNGaussianFilter.insert(data)
    pass
