# Tricerabot walks and roars, adapted from Adafruit industries Stumble Bot.
# See: https://learn.adafruit.com/stumble-bot-with-circuit-playground-and-crickit

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_crickit import crickit

# for dinosaur roar
import audioio


STEPS = 100                               # Number of steps to take
SOUND_FILE = 'dino_roar.wav'              # Sound file to play

led = DigitalInOut(board.D13)            # Set up Red LED
led.direction = Direction.OUTPUT

button_A = DigitalInOut(board.BUTTON_A)  # Set up switch A
button_A.direction = Direction.INPUT
button_A.pull = Pull.DOWN

# Create servos list
servos = [crickit.servo_1, crickit.servo_2]

# TowerPro servos like 500/2500 pulsewidths
servos[0].set_pulse_width_range(min_pulse=500, max_pulse=2500)
servos[1].set_pulse_width_range(min_pulse=500, max_pulse=2500)

# starting angle, middle
servos[1].angle = 90
servos[0].angle = 90

# enable the speaker
spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True


def servo_front(direction):
    if direction > 0:
        index = 50
        while index <= 100:
            servos[1].angle = index
            time.sleep(0.040)
            index = index + 2
    if direction < 0:
        index = 100
        while index >= 50:
            servos[1].angle = index
            time.sleep(0.040)
            index = index - 2
    time.sleep(0.002)

def servo_back(direction):
    if direction > 0:
        index = 60
        while index <= 90:
            servos[0].angle = index
            time.sleep(0.040)
            index = index + 4
    if direction < 0:
        index = 90
        while index >= 60:
            servos[0].angle = index
            time.sleep(0.040)
            index = index - 4
    time.sleep(0.020)
    
def play_file(filename):
    print("Playing file: " + filename)
    wave_file = open(filename, "rb")
    with audioio.WaveFile(wave_file) as wave:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    print("Finished playing: " + filename)

print("It's TriceraBot Time")

while True:
    if button_A.value:     # If button A is pressed, start bot
        led.value = True   # Turn on LED 13 to show we're gone!
        for i in range(STEPS):
            print("back 1")
            servo_back(1)
            time.sleep(0.100)
            print("front 1")
            servo_front(1)
            time.sleep(0.100)
            print("back 2")
            servo_back(-1)
            time.sleep(0.100)
            print("front 2")
            servo_front(-1)
            time.sleep(0.100)
            if i % 5 == 0:
                play_file(SOUND_FILE)
        led.value = False
        