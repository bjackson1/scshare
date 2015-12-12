from flask import Flask
from flask import request
from flask import render_template
import RPi.GPIO as gpio
import yaml

devstream = file('devices.yaml')
devices = yaml.load(devstream)

app = Flask(__name__)

@app.route('/')
def index():
  reader = request.args.get('reader')
  state = request.args.get('state')

  return request.path

@app.route('/<format>/<readerid>/<poweredstate>/<insertedstate>')
def reader(format, readerid, poweredstate, insertedstate):
  if readerid in devices['cards']:
    pwio = devices['cards'][readerid]['gpio']['power']
    swio = devices['cards'][readerid]['gpio']['switch']
    
    gpio.setmode(gpio.BCM)
    gpio.setup(pwio, gpio.OUT)
    gpio.output(pwio, False if poweredstate == 'on' else True)
    gpio.setup(swio, gpio.OUT)
    gpio.output(swio, False if insertedstate == 'in' else True)

    print render_template('cardstatechange.text', readerid=readerid, poweredstate=poweredstate, insertedstate=insertedstate, powergpio=pwio, switchgpio=swio)

    return render_template('cardstatechange.' + format, readerid=readerid, poweredstate=poweredstate, insertedstate=insertedstate, powergpio=pwio, switchgpio=swio)
  else:
    print readerid + " does not exist"
    return readerid + " does not exist"

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')


