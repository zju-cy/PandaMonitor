from util import gear
from util import sensor
from util import cpu
from util import database as db
from util.camera import Camera
import json
import io
from flask import Flask, render_template, Response, make_response, request
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


@app.route("/")
def index():
    hum, temp = sensor.get_sensor_data()
    cpuTemp, cpuUsage, ramUsage = cpu.getInfo()
    data = {'temp': temp, 'hum': hum, 'cpuTemp': cpuTemp, 'cpuUsage': cpuUsage, 'ramUsage': ramUsage}
    return render_template('index.html', **data)


@app.route("/data")
def data():
    hum, temp = sensor.get_sensor_data()
    db.insertData(temp, hum)
    jsonData = {'temp': temp, 'hum': hum}
    return json.dumps(jsonData)


@app.route("/cpu")
def cpu_info():
    cpuTemp, cpuUsage, ramUsage = cpu.getInfo()
    jsonData = {'cpuTemp': cpuTemp, 'cpuUsage': cpuUsage, 'ramUsage': ramUsage}
    return json.dumps(jsonData)


@app.route("/move/<direction>")
def move(direction):
    gear.move(direction, 10)
    jsonData = data()
    return render_template('index.html', **json.loads(jsonData))


@app.route('/video/<width>/<height>')
def video(width, height):
    return Response(_gen(Camera(int(width), int(height))), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/plot/temp')
def plot_temp():
    times, temps, hums = db.selectLast24HData()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Last 24H Temperature [`C]")
    axis.set_xlabel("Time")
    axis.grid(True)
    axis.set_ylim(-10, 50)
    xs = range(len(times))
    ys = temps
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/plot/hum')
def plot_hum():
    times, temps, hums = db.selectLast24HData()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Last 24H Humidity [%]")
    axis.set_xlabel("Time")
    axis.grid(True)
    axis.set_ylim(0, 100)
    xs = range(len(times))
    ys = hums
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


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
