import os
import random
import time
import badge
DEVICE = "/dev/ttyUSB0"
rssFeed = 'http://www.dn.se/nyheter/m/rss'
def main():
	currentMessage = 'Starting...'
	writeToLed(currentMessage,'4')
	time.sleep(2)
	while True:
		dropboxInfo = checkDropBox()
		if dropboxInfo[0:4].find('news') != -1:
			print 'News detected'
			print dropboxInfo
			wantedMessage = fetchRss(dropboxInfo.split()[1])
		else:
			wantedMessage = dropboxInfo
		if wantedMessage == currentMessage:
			print 'Nothing new...'
		else:
			writeToLed(wantedMessage,'4')
			currentMessage = wantedMessage
			
		print 'Now sleeping'
		for i in range(0,10):
			print '.'
			time.sleep(1)
	print '.'
def writeToLed(msg,spd):
	os.system("stty speed 38400 <" + DEVICE)
	f = open(DEVICE, "w")
	pkts = badge.build_packets(0x600, badge.message_file(msg, speed=spd, action=badge.ACTION_ROTATE))
	for p in pkts:
		f.write(p.format())
	f.flush()
	f.close()

def checkDropBox():
	print 'Now connecting to dropbox'
	os.system("wget -q https://dl.dropboxusercontent.com/u/2082167/ledbadge.txt -N")
	file = open("ledbadge.txt","r")
	dropboxInfo = file.read()
	file.close()
	return dropboxInfo
	
def fetchRss(feed):
	allFeeds=['http://www.dn.se/nyheter/m/rss','http://rss.cnn.com/rss/edition.rss','http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989']
	if feed == 'random':
		print 'Random feed'
		return fetchRss(allFeeds[random.randint(0,1)])
	if feed == 'DN':
		print 'DN'
		return fetchRss(allFeeds[0])
	if feed == 'Al-Jazeera':
		print feed
		return fetchRss(allFeeds[2])
	elif feed == allFeeds[0]:
		print 'Feed detected:',feed
		os.system('wget '+feed+' -O rss')
		f = open('rss','r')
		for line in f:
			temp = line.find('[CDATA')
			if temp != -1 and line.find('<img') == -1:
				message =  line[temp:].split('[')[2].split(']')[0]
				if message.find('Nyheter - Nyheter') == -1:
					return 'DN: '+message
		f.close()
	
	elif feed == allFeeds[1]:
		print 'Feed detected:', feed
		os.system('wget '+feed+' -O rss')
		f = open('rss','r')
		for line in f:
			temp = line.find('<title>')
			if temp != -1 and line.find('CNN.com - Top Stories') == -1:
				message = line.split('<')[1].split('>')[1]
				print message
				return 'CNN: '+message
	else:
		print 'Feed not supported:',feed
		return 'Feed not supported'
	
	
main()
