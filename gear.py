import RPi.GPIO as GPIO
import time

# pwm pin define
zPanelPin = 18
xPanelPin = 12
pinMode = GPIO.BCM
# pwm property
DUTY = 50
T = 1 / DUTY
# duty cycle (sg90, 2.5-12.5, mid is 7.5)
zPanelDutyCycle = 7
xPanelDutyCycle = 7.5
minDutyCycle = 2.5
maxDutyCycle = 12.5
disDutyCycle = 0.5
TotalAngel = 180

# set pin
GPIO.setmode(pinMode)
GPIO.setup(zPanelPin, GPIO.OUT, initial=False)
GPIO.setup(xPanelPin, GPIO.OUT, initial=False)
# define pwm
zPWM = GPIO.PWM(zPanelPin, DUTY)
xPWM = GPIO.PWM(xPanelPin, DUTY)
# dic
directions = ['L', 'R', 'U', 'D']
direction_panel = {'L': zPWM, 'R': zPWM, 'U': xPWM, 'D': xPWM}


def init():
    # set pin
    GPIO.setmode(pinMode)
    GPIO.setup(zPanelPin, GPIO.OUT, initial=False)
    GPIO.setup(xPanelPin, GPIO.OUT, initial=False)
    # define pwm
    global zPWM, xPWM
    zPWM = GPIO.PWM(zPanelPin, DUTY)
    xPWM = GPIO.PWM(xPanelPin, DUTY)


def _l(change_duty):
    global zPanelDutyCycle
    zPanelDutyCycle -= change_duty
    if zPanelDutyCycle < (minDutyCycle + disDutyCycle):
        zPanelDutyCycle = minDutyCycle + disDutyCycle
    return zPanelDutyCycle


def _r(change_duty):
    global zPanelDutyCycle
    zPanelDutyCycle += change_duty
    if zPanelDutyCycle > (maxDutyCycle - disDutyCycle):
        zPanelDutyCycle = maxDutyCycle - disDutyCycle
    return zPanelDutyCycle


def _u(change_duty):
    global xPanelDutyCycle
    xPanelDutyCycle -= change_duty
    if xPanelDutyCycle < (minDutyCycle + disDutyCycle):
        xPanelDutyCycle = minDutyCycle + disDutyCycle
    return xPanelDutyCycle


def _d(change_duty):
    global xPanelDutyCycle
    xPanelDutyCycle += change_duty
    if xPanelDutyCycle > (maxDutyCycle - disDutyCycle):
        xPanelDutyCycle = maxDutyCycle - disDutyCycle
    return xPanelDutyCycle


switch = {
    'R': _l,
    "L": _r,
    'U': _u,
    'D': _d
}


def move(direction, angle=1.8):
    if direction not in directions:
        return

    change_duty_cycle = (maxDutyCycle - minDutyCycle) * angle / TotalAngel
    duty_cycle = switch[direction](change_duty_cycle)
    pwm = direction_panel.get(direction)
    print('-Gear: {} direction, {} angle, {} duty'.format(direction, angle, duty_cycle))
    _move(pwm, duty_cycle)


def continue_move(direction):
    while True:
        move(direction)


def _move(pwm, duty_cycle):
    pwm.start(0)
    time.sleep(T)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(T)
    pwm.ChangeDutyCycle(0)
    time.sleep(T)
    time.sleep(0.1)


def stop(direction):
    pwm = direction_panel.get(direction)
    pwm.ChangeDutyCycle(0)
    time.sleep(T)


def middle():
    global zPanelDutyCycle, xPanelDutyCycle
    zPanelDutyCycle = 7
    xPanelDutyCycle = 7.5
    _move(zPWM, zPanelDutyCycle)
    _move(xPWM, xPanelDutyCycle)
    print('-Gear: set to middle position')

def left():
    move('L', 180)

def right():
    move('R', 180)

def up():
    move('U', 180)

def down():
    move('D', 180)

def clean():
    zPWM.stop()
    xPWM.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    middle()
    move('L', 30)
    move('R', 60)
    move('U', 30)
    move('D', 60)
    left()
    right()
    up()
    down()
    middle()
    clean()