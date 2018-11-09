dateutil_tz = True

import sys
import subprocess
import select
import threading
from threading import Timer
import time
from collections import deque
from datetime import datetime
import getopt
import os
import os.path
import json
import re
import string
import base64

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import re

# ------------------------------------------------------------
# low-level data prefix
# ------------------------------------------------------------

LL_PREFIX_1 = '\xFF'
LL_PREFIX_LORA = '\xFE'
# add here other data prefix for other type of low-level radio gateway


# list here other radio type
LORA_RADIO = 1

# will be dynamically determined according to the second data prefix
radio_type = LORA_RADIO

# ------------------------------------------------------------
# last pkt information
# ------------------------------------------------------------
pdata = "0,0,0,0,0,0,0,0"
rdata = "0,0,0"
tdata = "N/A"

dst = 0
ptype = 0
ptypestr = "N/A"
src = 0
seq = 0
datalen = 0
SNR = 0
RSSI = 0
bw = 0
cr = 0
sf = 0

_hasRadioData = False
# ------------------------------------------------------------

# ------------------------------------------------------------
# for managing the input data when we can have aes encryption
# ------------------------------------------------------------
_linebuf = "the line buffer"
_linebuf_idx = 0
_has_linebuf = 0

# ------------------------------------------------------------
# for google cloud sub/pub service
# ------------------------------------------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Lora-Radio-040a700bc68e.json"
_project="lora-radio"
_subTopic="temperature"

from google.cloud import pubsub_v1

# publisher = pubsub_v1.PublisherClient();
# topic_path = publisher.topic_path(_project, _subTopic)


def getSingleChar():
    global _has_linebuf
    # if we have a valid _linebuf then read from _linebuf
    if _has_linebuf == 1:
        global _linebuf_idx
        global _linebuf
        if _linebuf_idx < len(_linebuf):
            _linebuf_idx = _linebuf_idx + 1
            return _linebuf[_linebuf_idx - 1]
        else:
            # no more character from _linebuf, so read from stdin
            _has_linebuf = 0
            return sys.stdin.read(1)
    else:
        return sys.stdin.read(1)


def getAllLine():
    global _linebuf_idx
    p = _linebuf_idx
    _linebuf_idx = 0
    global _has_linebuf
    _has_linebuf = 0
    global _linebuf
    # return the remaining of the string and clear the _linebuf
    return _linebuf[p:]


def fillLinebuf(n):
    global _linebuf_idx
    _linebuf_idx = 0
    global _has_linebuf
    _has_linebuf = 1
    global _linebuf
    # fill in our _linebuf from stdin
    _linebuf = sys.stdin.read(n)


# use custom font
# font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                                      'fonts', 'C&C Red Alert [INET].ttf'))
# font2 = ImageFont.truetype(font_path, 12)
device = get_device()

def displayData(temp):
    with canvas(device) as draw:
        draw.text((0, 0), "Group: Dumb", fill="white")
        if device.height >= 32:
            draw.text((0, 14), "Temp: " + temp, fill="white")
            draw.text((0, 44), '____________________', fill="white")
            #draw time at bottom
            now = datetime.now()
            draw.text((0, 55), "U: " + now.strftime('%x')+ ' ' + now.strftime('%X'), fill="white")

def publishToGoogleSub(message):
    # UTF-8 encoding
    data = message.encode('utf-8')
    # Publish to google cloud
    publisher.publish(topic_path, data, temptime=str(int(round(time.time() * 1000))));

# Init display
displayData("--")

#Main loop
while True:
    sys.stdout.flush()
    ch = getSingleChar()

    if(ch=='^'):
        now = datetime.now()
        ch=sys.stdin.read(1)

        if(ch=='p'):
            pdata = sys.stdin.readline()
            print(now.isoformat())
            print("rcv ctrl pkt info (^p): " + pdata,)
            arr = map(int, pdata.split(','))
            print("splitted in: ",)
            print(arr)

    if(ch=='\\' and _hasRadioData==True):
        _hasRadioData = False
        now = datetime.now()

        ch = getSingleChar()
        if(ch == '!'):
            ldata = sys.stdin.readline()
            print("rcv msg to log (\$) in log file: " + ldata)
            # Check whether for temporature
            if("#TC" in ldata):
                #Display temporature
                #Try extract temprature
                tc = re.findall(r"TC\/\d+\.*\d*", ldata)
                if(tc):
                    # Display
                    temprature = re.findall(r"\d+\.*\d*",tc[0])
                    displayData(temprature[0])
#                     publishToGoogleSub(temprature[0])
#                     os.system('curl -H "Content-Type: application/json" -H "Authorization: OAuth PL6O1oU7O67GBmvIj7Cq" -d \'{"messages":[{"body":"' + ldata.rstrip() + '"}]}\' "http://mq-aws-eu-west-1-1.iron.io/3/projects/5b57cb0f0b29d90009fb5f82/queues/lora_gateway/messages"')
                else:
                    displayData("ERR")





    if (ch == LL_PREFIX_1):
        print("got first framing byte")
        ch = getSingleChar()

        if (ch == LL_PREFIX_LORA):
            print("--> got LoRa data prefix")
            radio_type = LORA_RADIO

            _hasRadioData = True