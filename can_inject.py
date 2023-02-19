from m5stack import *
from m5ui import *
from uiflow import *
from machine import CAN
import utime

current_frame = 0

from . import messages

msg_ACK = messages.msg_ACK
msg_CLR = messages.msg_CLR
msg_ON  = messages.msg_ON
msg_OFF = messages.msg_OFF

id_ACK = messages.id_ACK
id_CLR = messages.id_CLR
id_ON  = messages.id_ON
id_OFF = messages.id_OFF

class sm:
    ack = 0
    idle_on = 1
    idle_off = 2
    send_on = 3
    send_off = 4
    
state = sm.ack

WAIT_TIME_MS = 200

color_ON = 0x00FF00
color_OFF = 0xFF0000
color_ACK = 0x0000FF

BRIGHTNESS = 80
time_now = 0

can = CAN(0, extframe=True, mode=CAN.NORMAL, baudrate=CAN.BAUDRATE_250K, tx_io=22, rx_io=19, auto_restart=False)


def on_wasPressed():
    global time_now, state
    time_now = utime.ticks_ms()
    
    while btnA.isPressed():
        if utime.ticks_diff(utime.ticks_ms(), time_now) > 800:
            # Long Press:
            if state==sm.idle_on:
                state = sm.send_on
            elif state==sm.idle_off:
                state = sm.send_off
            else:
                return
        wait_ms(2)
    
    # Short Press:
    if state == sm.ack:
        state = sm.idle_on
    elif state == sm.idle_on:
        state = sm.idle_off
    elif state == sm.idle_off:
        state = sm.idle_on
    elif state == sm.send_on:
        state = sm.idle_on
    elif state == sm.send_off:
        state = sm.idle_off
    pass
btnA.wasPressed(on_wasPressed)


while True:
    if state == sm.ack:
        rgb.setColorAll(color_ACK)
        rgb.setBrightness(BRIGHTNESS)
        if can.any():
            frame = can.recv()

            wait_ms(100)
            rgb.setBrightness(0)
            wait_ms(100)
            can.clear_rx_queue()

    elif state == sm.idle_on:
        rgb.setColorAll(color_ON)
        rgb.setBrightness(BRIGHTNESS)
    elif state == sm.idle_off:
        rgb.setColorAll(color_OFF)
        rgb.setBrightness(BRIGHTNESS)
    elif state == sm.send_on:
        rgb.setColorAll(color_ON)
        rgb.setBrightness(BRIGHTNESS)
        
        can.send(msg_ACK, id_ACK)
        wait_ms(20)
        can.send(msg_CLR, id_CLR)
        wait_ms(20)
        can.send(msg_ON, id_ON)
        
        rgb.setBrightness(0)
        wait_ms(WAIT_TIME_MS)        
    
    #Turn OFF 
    elif state == sm.send_off:
        rgb.setColorAll(color_OFF)
        rgb.setBrightness(BRIGHTNESS)        
        
        can.send(msg_OFF, id_OFF)

        wait_ms(300)
        rgb.setBrightness(0)
        wait_ms(300)    
    




    wait_ms(2)
