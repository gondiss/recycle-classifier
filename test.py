from gpiozero import LED, Button, PWMLED
from time import sleep

# libcamera-still --width 256 --height 256 -o image.jpeg

button = Button(6)

rled = PWMLED(17)
gled = PWMLED(27)
bled = PWMLED(22)

recycleled = LED(13) 
trashled = LED(19) 
errorled = LED(26) 

while True:
    button.wait_for_press()
    
    rled.value = 1  # off
    gled.value = 0.25  # off
    bled.value = 0  # off
    sleep(10)
    rled.value = 0  # off
    gled.value = 1  # off
    bled.value = 1  # off
    sleep(10)
    rled.value = 1  # off
    gled.value = 0  # off
    bled.value = 1  # off
    sleep(10)

    recycleled.on()
    sleep(3)
    recycleled.off()
    
    trashled.on()
    sleep(3)
    trashled.off()
    
    errorled.on()
    sleep(3)
    errorled.off()

    trashled.on()
