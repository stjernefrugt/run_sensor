import time
import sys
import datetime
import Adafruit_DHT
from influxdb import InfluxDBClient
device ="pi2"

# Configure InfluxDB connection variables
host = "pi4.local" #  Pi 4 running influxdb and grafana
port = 8086 # default port
user = device # the user/password created for the pi, with write access
password = device 
dbname = "data" # the database we created earlier
interval = 10 # Sample period in seconds

# Create the InfluxDB client object
client = InfluxDBClient(host, port, user, password, dbname)

# Enter the sensor details
sensor = Adafruit_DHT.AM2302
sensor_gpio = 4

# think of measurement as a SQL table, it's not...but...
measurement = device
# location will be used as a grouping tag later
location = device

# Run until you get a ctrl^c
try:
    while True:
        # Read the sensor using the configured driver and gpio
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_gpio)
        iso = time.ctime()
        # Print for debugging, uncomment the below line
        # print("[%s] Temp: %s, Humidity: %s" % (iso, temperature, humidity)) 
        # Create the JSON data structure
        data = [
        {
          "measurement": measurement,
              "tags": {
                  "location": location,
              },
              "time": iso,
              "fields": {
                  "temperature" : temperature,
                  "humidity": humidity
              }
          }
        ]
        # Send the JSON data to InfluxDB
        client.write_points(data)
        # Wait until it's time to query again...
        time.sleep(interval)
 
except KeyboardInterrupt:
    pass

