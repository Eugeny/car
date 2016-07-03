from gpiozero import LED
from flask import Flask, render_template
from threading import Thread
import time

app = Flask(__name__)
key_last_pressed = {}
gpio = {
    'up': LED(1),
    'down': LED(1),
    'left': LED(1),
    'right': LED(1),
}


def set_gpio(direction, state):
    if state:
        gpio[direction].on()
    else:
        gpio[direction].off()


def worker():
    while True:
        time.sleep(0.2)

        for key in ['up', 'down', 'left', 'right']:
            if time.time() - key_last_pressed.get(key, 0) > 500:
                set_gpio(key, False)
            else:
                set_gpio(key, True)


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
