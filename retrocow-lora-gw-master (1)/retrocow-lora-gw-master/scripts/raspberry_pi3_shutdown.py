
import RPi.GPIO as GPIO
import os
from time import sleep

from demo_opts import get_device
from luma.core.render import canvas

gpio_pin_number=21
#Replace YOUR_CHOSEN_GPIO_NUMBER_HERE with the GPIO pin number you wish to use
#Make sure you know which rapsberry pi revision you are using first
#The line should look something like this e.g. "gpio_pin_number=7"

GPIO.setmode(GPIO.BCM)
#Use BCM pin numbering (i.e. the GPIO number, not pin number)
#WARNING: this will change between Pi versions
#Check yours first and adjust accordingly

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#It's very important the pin is an input to avoid short-circuits
#The pull-up resistor means the pin is high by default
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.HIGH)

try:
    GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
    #Use falling edge detection to see if pin is pulled
    #low to avoid repeated polling

    # turn off radio service
    os.system("sudo systemctl stop lora.service")

    #display shutdown message and wait for 5 seconds...
    device = get_device()
    device.clear()
    with canvas(device) as draw:
        draw.text((0, 20), "shutting down ...", fill="white")

    # sleep for 5 seconds ...
    sleep(5)

    #turn off display
    device.clear()
    device.hide()

    #turn off light
    GPIO.output(26, GPIO.LOW)

    os.system("sudo shutdown -h now")
    #Send command to system to shutdown
except:
    pass

GPIO.cleanup()
#Revert all GPIO pins to their normal states (i.e. input = safe)