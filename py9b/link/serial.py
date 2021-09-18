"""Direct serial link"""

from __future__ import absolute_import
import serial
import serial.tools.list_ports as lp
from binascii import hexlify
from .base import BaseLink, LinkTimeoutException, LinkOpenException


class SerialLink(BaseLink):
	def __init__(self, *args, **kwargs):
		super(SerialLink, self).__init__(*args, **kwargs)
		self.com = None


	def __enter__(self):
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		self.close()


#		ports = lp.comports()
#		res = [("%s %04X:%04X" % (port.device, port.vid, port.pid), port.device) for port in ports]
#		return res
	def scan(self):
		result1 = [{"port": p, "description": d, "hwid": h}
					for p, d, h in lp.comports() if p]
		ports = lp.comports()
		result2 = [("%s %s:%s" % (p.device, p.vid, p.pid), p.device)
					for p in ports if p]
    	# fix for PySerial
		# if not result and system() == "Darwin":
		# 	for p in glob("/dev/cu.*"):
		# 			result.append({"port": p, "description": "", "hwid": ""})
		return result2

	def open(self, port):
		try:
			self.com = serial.Serial(port, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout)
		except serial.SerialException:
			raise LinkOpenException


	def close(self):
		if self.com:
			self.com.close()
			self.com = None


	def read(self, size):
		try:
			data = self.com.read(size)
		except serial.SerialTimeoutException:
			raise LinkTimeoutException
		if len(data)<size:
			raise LinkTimeoutException
		if self.dump:
			print ("<")
			print (hexlify(data).upper())
		return data


	def write(self, data):
		if self.dump:
			print (">")
			print (hexlify(data).upper())
		self.com.write(data)


__all__ = ["SerialLink"]
