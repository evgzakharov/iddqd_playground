from Raspi_MotorHAT import Raspi_MotorHAT
import time

__max_speed = 100
__motor = Raspi_MotorHAT(addr=0x6f, freq=250).getMotor(1)


def breakdown():
    __motor.MC.setPin(__motor.IN1pin, 1)
    __motor.MC.setPin(__motor.IN2pin, 1)


def forward(speed):
    speed = min(__max_speed, speed)
    __motor.setSpeed(speed)
    __motor.run(Raspi_MotorHAT.FORWARD)


def backward(speed):
    speed = min(__max_speed, speed)
    __motor.setSpeed(speed)
    __motor.run(Raspi_MotorHAT.BACKWARD)


def impluse(speed, delay=0.5):
    if speed < 0:
        backward(abs(speed))
    else:
        forward(speed)
    time.sleep(delay)
    breakdown()


def roll():
    __motor.run(Raspi_MotorHAT.RELEASE)
