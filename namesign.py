import os
import time

import badge

DEVICE = "/dev/ttyUSB0"
badgeMessage = ''
os.system("stty speed 38400 <" + DEVICE)
while True:
	print 'Now connecting to dropbox'
	os.system("wget -q https://dl.dropboxusercontent.com/u/2082167/ledbadge.txt -N")
	file = open("ledbadge.txt","r")
	temp = file.read()
	file.close()
	print 'Comparing messages', temp, badgeMessage
	if temp != badgeMessage:
		badgeMessage = temp
		print 'Now trying to write to badge, ', badgeMessage
		#os.system("stty speed 38400 <" + DEVICE)
		f = open(DEVICE, "w")
		pkts = badge.build_packets(0x600, badge.message_file(badgeMessage, speed='4', action=badge.ACTION_ROTATE))
		for p in pkts:
			f.write(p.format())
		f.flush()
		f.close()
	print 'Now sleeping'
	for i in range(0,10):
		print '.',
		time.sleep(1)
	print '.'
