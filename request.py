import urllib.request
import json

data = {
    "Inputs": {
        "input1":
        [
            {
                'temp': "1",
                'airPressure': "1",
                'windSpeed': "1",
                'rain': "1",
                'windBearing': "1",
                'cloudCover': "1",
                'uvIndex': "1",
                'visibility': "1",
                'dewPoint': "1",
                'humidity': "1",
                'apparentTemperature': "1",
                'soil_moisture_10': "1",
                'sensorId': "1",
                'sensorGroupId': "1",
                'cropType': "",
                'cropRace': "",
                'typeField': "",
                'lat': "1",
                'long': "1",
                'soilTypeId': "1",
                'unixTimestampReading': "1",
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
    print(result['Results']['output1'][0]['Scored Label Mean'])
    print(result['Results']['output1'][0]['Scored Label Standard Deviation'])
    print({'soilMoistureTen': result['Results']['output1'][0]['Scored Label Mean'], 'percentage': result['Results']['output1'][0]['Scored Label Standard Deviation']})
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
