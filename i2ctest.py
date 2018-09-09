# -*- coding: UTF-8 -*-
import smbus
import time

bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
  bus.write_byte(address, value)
  return -1

def readNumber():
  number = bus.read_i2c_block_data(address,0,4)
  return number

while True:
  var = input("Enter 1 – 9: ")
  if not var:
    continue
  writeNumber(var)
  print "RPI: Hi Arduino, I sent you ", var
  # sleep one second
  time.sleep(1)

  number = readNumber()
  result = number[0] + (number[1] << 8) + (number[2] << 16) + (number[3] << 24)
  print "Arduino: Hey RPI, I received first byte ", result
#, " second byte ", readNumber(), "third byte ", readNumber(), "fourth byte ", readNumber()
  print
