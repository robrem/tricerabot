# Tricerabot walks and roars, adapted from Adafruit industries Stumble Bot.
# See: https://learn.adafruit.com/stumble-bot-with-circuit-playground-and-crickit

import adafruit_irremote
import audioio
import board
import pulseio
import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_crickit import crickit


STEPS = 100                              # Number of steps to take
SOUND_FILE = 'dino_roar.wav'             # Sound file to play
IR_REMOTE_POWER = [255, 0, 93, 162]      # Code for power button on NEC remote

led = DigitalInOut(board.D13)            # Set up Red LED
led.direction = Direction.OUTPUT

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

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)

# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()


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

print("It's Tricerabot Time")

bot_is_on = False

while True:
    pulses = decoder.read_pulses(pulsein)

    try:
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses, debug=False)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        print("NEC repeat!")
        continue
    except adafruit_irremote.IRDecodeException as e:
        # Something got distorted or maybe its not an NEC-type remote?
        print("Failed to decode: ", e.args)
        continue

    if not bot_is_on and received_code == IR_REMOTE_POWER:
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
    elif bot_is_on and received_code == IR_REMOTE_POWER:
        print("Stopping Tricerabot")
        