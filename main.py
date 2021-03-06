import serial
import datetime
import time
from sense_hat import SenseHat
import BlynkLib
import struct

BLYNK_AUTH = '53688269a2e44b2b9c05d16fcba15dae' 
blynk = BlynkLib.Blynk(BLYNK_AUTH)

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)
sense = SenseHat()
sense.show_letter("E",[0, 0, 255],[0, 0, 0])
@blynk.VIRTUAL_READ(1)
def my_read_handler():
    sense = SenseHat()
    sense.clear()
    temp = sense.get_temperature()
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(1, int(temp)-10)

@blynk.VIRTUAL_READ(3)
def my_read_handler():
    sense = SenseHat()
    sense.clear()
    humidity = sense.get_humidity()
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(3, int(humidity)) 

@blynk.VIRTUAL_READ(5)
def my_read_handler():
    sense = SenseHat()
    sense.clear()
    pressure = sense.get_pressure()
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(5, int(pressure)) 

@blynk.VIRTUAL_READ(10)
def my_read_handler():
    rcv = read_pm_line(port)
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(10, rcv[4] * 256 + rcv[5]) 

@blynk.VIRTUAL_READ(12)
def my_read_handler():
    rcv = read_pm_line(port) 
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(12, rcv[6] * 256 + rcv[7])

@blynk.VIRTUAL_READ(14)
def my_read_handler():
    rcv = read_pm_line(port) 
    sense.show_letter("E",[0, 0, 255],[0, 0, 0])
    blynk.virtual_write(14, rcv[8] * 256 + rcv[9])

@blynk.VIRTUAL_READ(20)
def my_read_handler():
    target = 0
    blynk.virtual_write(20, target)
    
@blynk.VIRTUAL_READ(22)
def my_read_handler():
    target = 0
    blynk.virtual_write(22, target)
    
@blynk.VIRTUAL_WRITE(40)
def my_write_handler(value):
    print('Current V1 value: {}'.format(value))    
    
    
def read_pm_line(_port):
    rv = bytearray()
    while True:  
        ch1 = _port.read()
        if ch1[0] == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(30)
                return rv

blynk.run() 
# while True:
    # try:
        # rcv = read_pm_line(port)
        # res = {'timestamp': datetime.datetime.now(),
               # 'apm10': rcv[4] * 256 + rcv[5],
               # 'apm25': rcv[6] * 256 + rcv[7],
               # 'apm100': rcv[8] * 256 + rcv[9],
               # 'pm10': rcv[10] * 256 + rcv[11],
               # 'pm25': rcv[12] * 256 + rcv[13],
               # 'pm100': rcv[14] * 256 + rcv[15],
               # 'gt03um': rcv[16] * 256 + rcv[17],
               # 'gt05um': rcv[18] * 256 + rcv[19],
               # 'gt10um': rcv[20] * 256 + rcv[21],
               # 'gt25um': rcv[22] * 256 + rcv[23],
               # 'gt50um': rcv[24] * 256 + rcv[25],
               # 'gt100um': rcv[26] * 256 + rcv[27]
               # }
        # print('===============\n'
              # 'PM1.0(CF=1): {}\n'
              # 'PM2.5(CF=1): {}\n'
              # 'PM10 (CF=1): {}\n'
              # 'PM1.0 (STD): {}\n'
              # 'PM2.5 (STD): {}\n'
              # 'PM10  (STD): {}\n'
              # '>0.3um     : {}\n'
              # '>0.5um     : {}\n'
              # '>1.0um     : {}\n'
              # '>2.5um     : {}\n'
              # '>5.0um     : {}\n'
              # '>10um      : {}'.format(res['apm10'], res['apm25'], res['apm100'],
                                       # res['pm10'], res['apm25'], res['pm100'],
                                       # res['gt03um'], res['gt05um'], res['gt10um'],
                                       # res['gt25um'], res['gt50um'], res['gt100um']))

    # except KeyboardInterrupt:
        # break