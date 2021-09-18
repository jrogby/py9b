#!python2-32
from py9b.link.base import LinkOpenException, LinkTimeoutException
from py9b.link.tcp import TCPLink
from py9b.link.ble import BLELink
from py9b.link.serial import SerialLink
from py9b.transport.base import BaseTransport as BT
from py9b.transport.packet import BasePacket as PKT
from py9b.transport.xiaomi import XiaomiTransport
from py9b.command.custom import ReadMem

ADDR = 0x1000
SIZE = 0x800
READ_CHUNK_SIZE = 0x10

link = SerialLink(dump=True)
#link = TCPLink()
#link = BLELink()

with link:
	print ("Scanning...")
	ports = link.scan()
	print (ports)

	tran = XiaomiTransport(link)

	#link.open(("192.168.1.45", 6000))
	link.open("/dev/cu.usbserial-10")
	print ("Connected")

	hfo = open("BmsEep.bin", "wb")
	for i in range(ADDR, ADDR+SIZE, READ_CHUNK_SIZE):
		print ("."),
		for retry in range(5):
			try:
				data = tran.execute(ReadMem(BT.BMS, i, "16s"))[0]
			except LinkTimeoutException:
				continue
			break
		else:
			print ("No response !")
			break
		hfo.write(data)

	hfo.close()
	link.close()
