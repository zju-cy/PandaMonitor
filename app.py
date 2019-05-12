import gear
import sensor
import camera
import json
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route("/")
def index():
    jsonData = data()
    return render_template('index.html', **json.loads(jsonData))


@app.route("/data")
def data():
    hum, temp = sensor.get_sensor_data()
    jsonData = {'temp': temp, 'hum': hum}
    return json.dumps(jsonData)


@app.route("/move/<direction>")
def move(direction):
    gear.move(direction, 10)
    jsonData = data()
    return render_template('index.html', **json.loads(jsonData))


@app.route('/video/<width>/<height>')
def video(width, height):
    return Response(_gen(camera.Camera(int(width), int(height))), mimetype='multipart/x-mixed-replace; boundary=frame')


def _gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def init():
    print("PandaMonitor: init start")
    gear.middle()
    gear.clean()
    gear.init()
    sensor.get_sensor_data()
    print("PandaMonitor: init finished\r\n")


if __name__ == '__main__':
    init()
    app.run(host='192.168.0.15', port=80, debug=False, threaded=True)
