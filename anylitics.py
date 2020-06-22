import matplotlib.pyplot as plt
from pymongo import MongoClient
import mysql.connector
import pandas as pd

sensorId = 100


farm21DB = mysql.connector.connect(
    host="127.0.0.1",
    user="homestead",
    password="secret",
    database="homestead"
)

# Get all data
cursor = farm21DB.cursor(dictionary=True, buffered=True)
client = MongoClient('mongodb://localhost:27017/')
db = client.predictions
dbFarm21 = client.weatherDataFarm21

allPredictionData = db.nnNoUvNoVis.find({})

# Difference Calculater in percentages


def calculateDiff(actual, prediction):
    return ((float(actual)-float(prediction))/float(prediction))*100


differencePercentage = []
differenceAbsolute = []

# Calculate the diffs and print this in console.
for prediction in allPredictionData:
    print(f"actual soil Moisture: {prediction['soil_moisture_10']} prediction: {prediction['soil_moisture_10_prediction']} difference {calculateDiff(prediction['soil_moisture_10'], prediction['soil_moisture_10_prediction'])}")
    differencePercentage.append(abs(calculateDiff(prediction['soil_moisture_10'], prediction['soil_moisture_10_prediction'])))
    differenceAbsolute.append(prediction['soil_moisture_10'] - prediction['soil_moisture_10_prediction'])
    pass

print(f'AVAERAGE OF DIFFERENT PERCENTAGE: {sum(differencePercentage)/len(differencePercentage)}')

cursor.execute(f"SELECT name FROM sensors WHERE id = {sensorId}")
sensorName = cursor.fetchall()[0]['name']

print(sensorName)


# Making graph
predictionData = pd.DataFrame(db.nnNoUvNoVis.find({}))
predictionData['differenceData'] = differencePercentage
predictionData['differenceAbsolute'] = differenceAbsolute


# Create graphs
plt.title(f'All Soil Moisture Sensor {sensorName} ({sensorId}) Prediction')
plt.ylabel('Percentage')
plt.xlabel('Dates')
plt.grid(True)
plt.autoscale(axis='x', tight=False)
plt.plot(predictionData['soil_moisture_10'], label="Actual")
plt.plot(predictionData['soil_moisture_10_prediction'], label="Prediction")
test = int(predictionData.shape[0] / 10)
plt.xticks(range(0,  predictionData.shape[0], test), predictionData['timestampReading'][::test], rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.autoscale()
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
plt.rcParams["figure.figsize"] = (20, 7)
plt.show()


movingAvg = predictionData.differenceData.ewm(span=35, adjust=False).mean()
# relative difference
plt.title(f'Afwijking over Data sensor {sensorId} naam: {sensorName}')
plt.ylabel('Percentage')
plt.xlabel('Dates')
plt.grid(True)
plt.autoscale(axis='x', tight=False)
plt.plot(differencePercentage, label="Actual")
plt.plot(movingAvg, label='moving Average')
test = int(predictionData.shape[0] / 10)
plt.xticks(range(0,  predictionData.shape[0], test), predictionData['timestampReading'][::test], rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.autoscale()
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
plt.rcParams["figure.figsize"] = (20, 7)
plt.show()

# Absolute difference
movingAvg = predictionData.differenceAbsolute.ewm(span=35, adjust=False).mean()

plt.title(f'Moisture Difference Sensor {sensorId} naam: {sensorName}')
plt.ylabel('Percentage')
plt.xlabel('Dates')
plt.grid(True)
plt.autoscale(axis='x', tight=False)
plt.plot(differenceAbsolute, label="Actual")
plt.plot(movingAvg, label='moving Average')
test = int(predictionData.shape[0] / 10)
plt.xticks(range(0,  predictionData.shape[0], test), predictionData['timestampReading'][::test], rotation=45)
plt.subplots_adjust(bottom=0.2)
plt.autoscale()
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
plt.rcParams["figure.figsize"] = (20, 7)
plt.show()
