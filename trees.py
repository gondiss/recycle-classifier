from gpiozero import LED, Button, PWMLED
from time import sleep
import subprocess
from classifier import classify
import time
import logging
import datetime

# libcamera-still --width 256 --height 256 -o image.jpeg

def get_time():
    return '{0:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logfile.log",
                    filemode = "a",
                    format = Log_Format,
                    level = logging.INFO)

logger = logging.getLogger()

logger.info("Started recycle classifier {}".format(get_time()))

button = Button(6)

rled = PWMLED(17)
gled = PWMLED(27)
bled = PWMLED(22)

greenled = LED(13) 

recycleled = LED(19) 
trashled = LED(26) 

def camera_capture_state():
    rled.value = 0  # off
    gled.value = 1  # off
    bled.value = 1  # off

def classifying_state():
    rled.value = 1  # off
    gled.value = 0  # off
    bled.value = 1  # off

def error_state():
    rled.value = 1  # off
    gled.value = 0  # off
    bled.value = 0  # off

def done_state():
    rled.value = 0  # off
    gled.value = 1  # off
    bled.value = 0  # off

def idle_state():
    rled.value = 0  # off
    gled.value = 0  # off
    bled.value = 0  # off

def post_process(item):
    file_name = get_time() + '.jpeg'
    dir_name = 'images'
    subprocess.run('mkdir -p images'.split())
    subprocess.run('mv image.jpeg {}/{}'.format(dir_name,file_name).split())
    logger.info('{} -{}'.format(file_name,item))
    with open("predictions.txt", "a") as f:
        f.write('{} - {}'.format(file_name,item))
        f.write('\n')

while True:
    idle_state()
    button.wait_for_press()
   
    camera_capture_state()
    res = subprocess.run('libcamera-still --width 256 --height 256 -o image.jpeg'.split(),capture_output=True)
    if res.returncode != 0:
        error_state()
        sleep(5)
        continue

    classifying_state()
    item = classify()
    done_state()

    if item == 'trash':
        print('trash')
        trashled.on()
        sleep(5)
        trashled.off()
    else:
        print('recycle')
        recycleled.on()
        sleep(5)
        recycleled.off()

    post_process(item)
