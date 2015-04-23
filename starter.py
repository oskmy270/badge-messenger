import os
import badge
import time
import subprocess

DEVICE = "/dev/ttyUSB0"

def setText(text):
	os.system("stty speed 38400 <" + DEVICE)
	f = open(DEVICE, "w")
	print 'Writing this to badge:', text
	pkts = badge.build_packets(0x600, badge.message_file(text, speed='3', action=badge.ACTION_HOLD))
	for p in pkts:
		f.write(p.format())
	f.flush()
	f.close()

def connectModem():
	print 'Connecting modem'
	p = subprocess.Popen(['sudo', '/usr/bin/modem3g/sakis3g', 'connect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	print out
	

setText('Connecting')
connectModem()


