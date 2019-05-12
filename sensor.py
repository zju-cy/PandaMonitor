import Adafruit_DHT
import time

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
# pin = 'P8_11'

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO4.
pin = 4


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
def get_sensor_data():
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    if h is not None and t is not None:
        print('-Sensor: Temp={0:0.1f}`C  Humidity={1:0.1f}%'.format(t, h))
        # time.sleep(2)
        return h, t
    print('-Sensor: Failed to get reading. Try again!')
    # time.sleep(2)
    return 0.0, 0.0


# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if __name__ == '__main__':
    humidity, temperature = get_sensor_data()
