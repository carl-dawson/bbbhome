from flask import Flask, render_template, jsonify, request
from flask_basicauth import BasicAuth
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

scheduler = BackgroundScheduler()

file = open("/var/www/bbbhome/auth.txt", "r")
auth = file.readlines()
auth = [x.strip() for x in auth]
app.config['BASIC_AUTH_USERNAME'] = auth[0]
app.config['BASIC_AUTH_PASSWORD'] = auth[1]

basic_auth = BasicAuth(app)

# Initialize GPIO pin
GPIO.setup("P9_11", GPIO.OUT)
GPIO.setup("P9_11", GPIO.OUT, delay=50)
GPIO.setup("P9_13", GPIO.IN)
GPIO.setup("P9_13", GPIO.IN, delay=50)

# Initialize ADC pin
#ADC.setup()
#time.sleep(0.1)
#ADC.setup()
analog_pin = "P9_33"


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/thermostat')
@basic_auth.required
def thermostat():
    return render_template("thermostat.html")


@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/on_off', methods=['GET', 'POST'])
def on_off():
    x = request.form.get('status', 0, type=int)
    print x
    if x == 1:
        GPIO.output("P9_11", GPIO.HIGH)
        return "Fire ON"
    elif x == 0:
        GPIO.output("P9_11", GPIO.LOW)
        return "Fire OFF"


@app.route('/get_status')
def get_status():
    #temp = ADC.read(analog_pin)*1.8
    #temp = temp * 1.8 + 32
    temp = 42
    return jsonify([GPIO.input("P9_13"), temp])

if __name__ == "__main__":
    app.run()
