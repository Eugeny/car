from gpiozero import OutputDevice
from flask import Flask, render_template
from threading import Thread
import time

app = Flask(__name__)
key_last_pressed = {}
gpio = {
    'motor1': OutputDevice(13),
    'motor2': OutputDevice(19),
    'motor_enable': OutputDevice(26),
}


def set_gpio(keys):
    if 'up' in keys or 'down' in keys:
        if 'up' in keys:
            gpio['motor1'].on()
            gpio['motor2'].off()
        else:
            gpio['motor1'].off()
            gpio['motor2'].on()
        gpio['motor_enable'].on()
    else:
        gpio['motor_enable'].off()


def worker():
    while True:
        time.sleep(0.05)
        keys_pressed = set()
        for key in ['up', 'down', 'left', 'right']:
            if time.time() - key_last_pressed.get(key, 0) > 500:
                keys_pressed.add(key)
        set_gpio(keys_pressed)


@app.before_first_request
def start_worker():
    t = Thread(target=worker)
    t.daemon = True
    t.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/key/<key>/<action>')
def key(key, action):
    if action == 'press':
        key_last_pressed[key] = time.time()
    if action == 'release':
        key_last_pressed[key] = 0
    return ('', 200)


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True, host='0.0.0.0')
