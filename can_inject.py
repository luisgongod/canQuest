from m5stack import *
from m5ui import *
from uiflow import *
from machine import CAN
import utime

current_frame = 0

rgb.setBrightness(80)
rgb.setColorAll(0x666666)

msg_ON = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
msg_OFF = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
msg_ACK = [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]
msg_CLR = [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10]


color_ON = 0x00FF00
color_OFF = 0xFF0000
color_ACK = 0x0000FF

toggle_send = False
toggle_mode = False
time_now = 0

can = CAN(0, extframe=True, mode=CAN.NORMAL, baudrate=CAN.BAUDRATE_250K, tx_io=22, rx_io=19, auto_restart=False)
msg_to_send = msg_ACK
id_to_send = 0x00

#working
def on_wasPressed():
    global toggle_send, toggle_mode, time_now
    time_now = utime.ticks_ms()
    
    while btnA.isPressed():
        if utime.ticks_diff(utime.ticks_ms(), time_now) > 800:
            # Long Press:
            toggle_send = True
            return
        wait_ms(2)
    
    # Short Press:
    if toggle_send:
        toggle_send = False
    else:
        toggle_mode = not toggle_mode    
    pass
btnA.wasPressed(on_wasPressed)


while True:

    
    
    if toggle_mode:            
        msg_to_send = msg_ON
        id_to_send = 0x100
        rgb.setColorAll(color_ON)
    else:            
        msg_to_send = msg_OFF
        id_to_send = 0x200      
        rgb.setColorAll(color_OFF)
    
    if toggle_send:
        if toggle_mode:
            can.send(msg_ACK, 0x300)
            utime.sleep(0.05)
            can.send(msg_CLR, 0x300)
            utime.sleep(0.05)
            
        can.send(msg_to_send, id_to_send)
        rgb.setBrightness(0)
        utime.sleep(0.2)
        rgb.setBrightness(80)
        utime.sleep(0.2)
    else:
        rgb.setBrightness(80)

    wait_ms(2)
