#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Edited by Edgardo Peregrino on July 19, 2021
# import libraries
from time import sleep
import aiy.voice.tts
from gpiozero import OutputDevice, AngularServo, LED, PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import argparse
import locale
import logging
from flask import Flask, request, render_template, json
from aiy.cloudspeech import CloudSpeechClient

# Define app
app = Flask(__name__)

# Define factories
factory = PiGPIOFactory(host='192.168.0.22')
factory2 = PiGPIOFactory(host='192.168.0.23')

# Define both robots
en_1 = PWMOutputDevice(12, pin_factory=factory)
en_2 = PWMOutputDevice(26, pin_factory=factory)
motor_in1 = OutputDevice(13,  pin_factory = factory)
motor_in2 = OutputDevice(21,  pin_factory = factory)
motor_in3 = OutputDevice(17,  pin_factory = factory)
motor_in4 = OutputDevice(27,  pin_factory = factory)

pin1 = OutputDevice(7,  pin_factory = factory2)
pin2 = OutputDevice(8,  pin_factory = factory2)
pin3 = OutputDevice(9,  pin_factory = factory2)
pin4 = OutputDevice(10,  pin_factory = factory2)

#Define the eye
linus_eye = LED(16, pin_factory=factory)

# Define the servos
angular_servo = AngularServo(22, min_angle=-90, max_angle=90, pin_factory=factory)
angular_servo2 = AngularServo(23, min_angle=-90, max_angle=90, pin_factory=factory)

# Define functions
def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('go forward',
                'go backward',
                'go left',
                'go right',
                'go up',
                'go down'
                'turn left',
                'turn right',
                'blink the light',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def forwards():
    pin1.off()
    pin2.on()
    pin3.on()
    pin4.off()
        

def backwards():
    pin1.on()
    pin2.off()
    pin3.off()
    pin4.on()
       

def left():
    pin1.on()
    pin2.off()
    pin3.on()
    pin4.off()
        
    
def right():
    pin1.off()
    pin2.on()
    pin3.off()
    pin4.on()
        

def stop():
    pin1.off()
    pin2.off()
    pin3.off()
    pin4.off()

# forwards
def direction_one():
    motor_in1.on()
    motor_in2.off()
    motor_in3.on()
    motor_in4.off()
    

# backwards
def direction_two():
    motor_in1.off()
    motor_in2.on()
    motor_in3.off()
    motor_in4.on()
    

#right
def direction_three():
    motor_in1.on()
    motor_in2.off()
    motor_in3.off()
    motor_in4.on()
    

# left
def direction_four():
    motor_in1.off()
    motor_in2.on()
    motor_in3.on()
    motor_in4.off()

def stop_two():
    motor_in1.off()
    motor_in2.off()
    motor_in3.off()
    motor_in4.off()

# Check the status on the app
@app.route('/status')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Status request successfull')
    return response

# Check the metrics of the app
@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    func()

# Gracefully shutdown app
@app.route('/shutdown', methods=['GET'])
def shutdown_server():
    shutdown()
    return 'Server shutting down'

# Main index
@app.route('/')
def index():
    return render_template('dual_robot_voice.html')

@app.route('/main')
def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    while True:
        if hints:
            logging.info('Say something, e.g. %s.' % ', '.join(hints))
        else:
            logging.info('Say something.')
        text = client.recognize(language_code=args.language, hint_phrases=hints)
        if text is None:
            logging.info('You said nothing.')
            continue
        logging.info('You said: "%s"' % text)
        text = text.lower()
        if 'go forward' in text:
            aiy.voice.tts.say('Okay I will go forward')
            forward()
            sleep(1)
            stop()
        elif 'go backward' in text:
            aiy.voice.tts.say('Okay I will go backward')
            backward()
            sleep(1)
            stop()
        elif 'go left' in text:
            aiy.voice.tts.say('Okay I will go left')
            left()
            sleep(0.3)
            stop()
        elif 'go right' in text:
            aiy.voice.tts.say('Okay I will go right')
            right()
            sleep(0.3)
            stop()
        elif 'go up' in text:
            aiy.voice.tts.say('Okay I will go up')
            direction_one()
            sleep(1)
            stop_two()
        elif 'go down' in text:
            aiy.voice.tts.say('Okay I will go down')
            direction_two()
            sleep(1)
            stop_two()
        elif 'turn left' in text:
            aiy.voice.tts.say('Okay I will go left')
            direction_four()
            sleep(0.3)
            stop_two()
        elif 'turn right' in text:
            aiy.voice.tts.say('Okay I will go right')
            direction_three()
            sleep(0.3)
            stop_two()
        elif 'blink the light' in text:
            aiy.voice.tts.say('Okay I will blink the light')
            linus_eye.blink(n=2)
        elif 'goodbye' in text:
            aiy.voice.tts.say('Goodbye')
            stop()
            break
    return render_template('dual_robot_voice.html')

# Servo control
@app.route('/angle', methods=['POST'])
def angle():
    slider1 = request.form["slider1"]
    slider2 = request.form["slider2"]
    angular_servo.angle = int(slider1)
    angular_servo2.angle = int(slider2)
    return render_template('dual_robot_voice.html')

# PWM control
@app.route('/pwm', methods=['POST'])
def pwm():
    slider3 = request.form["slider3"]
    slider4 = request.form["slider4"]
    en_1.value = int(slider3) / 10
    en_2.value = int(slider4) / 10
    return render_template('dual_robot_voice.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
