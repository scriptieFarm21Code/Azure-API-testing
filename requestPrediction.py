import urllib.request
import json


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
                    'soil_moisture_10': "",
                    'sensorId': requestData['sensorId'],
                    # 'sensorGroupId': requestData['sensorGroupId'],
                    # 'cropType': requestData['cropxType'],
                    # 'cropRace': requestData['cropRace'],
                    # 'typeField': requestData['typeField'],
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
        result = json.loads(result)
        print(result)
        return {'soilMoistureTen': float(result['Results']['output1'][0]['Scored Label Mean']), 'percentage': result['Results']['output1'][0]['Scored Label Standard Deviation']}
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
