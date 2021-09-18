import warnings
#sys.path.append("")
import serial
import serial.tools.list_ports


print ('\n\nPYSERIAL\n')
sPort = '/dev/cu.usbmodem14101'           #On Mac - find this using >ls /dev/cu.usb*

aSerialData = serial.Serial(sPort,9600)     #COM port object

while True:
    if (aSerialData.inWaiting()>0):
        sData = aSerialData.readline()
        print( sData )
