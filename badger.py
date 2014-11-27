import os
import time
import badge
DEVICE = "/dev/ttyUSB0"
def main():
	currentMessage = 'Starting...'
	writeToLed(currentMessage)
	while True:
		dropboxInfo = checkDropBox()
		if dropboxInfo == 'news'
			wantedMessage = fetchRss()
		else:
			wantedMessage = dropboxInfo
		if wantedMessage != currentMessage:
			writeToLed(wantedMessage)
			currentMessage = wantedMessage
def writeToLed(msg):
	os.system("stty speed 38400 <" + DEVICE)
while True:
	print 'Now connecting to dropbox'
	os.system("wget -q https://dl.dropboxusercontent.com/u/2082167/ledbadge.txt -N")
	file = open("ledbadge.txt","r")
	dropboxInfo = file.read()
	file.close()
	if dropboxInfo == 'news':
		badgeMessage = 'Nyheter: '
		os.system('python rssFetcher.py')
		newsFile = open('news.txt','r')
		badgeMessage = badgeMessage+newsFile.read()
		newsFile.close()
	else:
		badgeMessage = dropboxInfo

	print 'Comparing messages'
	print 'Current:', currentText
	print 'Wanted: ', badgeMessage

	if currentText != badgeMessage:
		print 'Now trying to write to badge, ', badgeMessage
		#os.system("stty speed 38400 <" + DEVICE)
		f = open(DEVICE, "w")
		pkts = badge.build_packets(0x600, badge.message_file(badgeMessage, speed='4', action=badge.ACTION_ROTATE))
		for p in pkts:
			f.write(p.format())
		f.flush()
		f.close()
		currentText = badgeMessage
	print 'Now sleeping'
	for i in range(0,10):
		print '.',
		time.sleep(1)
	print '.'
