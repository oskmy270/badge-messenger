#-*- coding: utf-8 -*-
import os
import random
import time
import badge


DEVICE = "/dev/ttyUSB0"
rssFeed = 'http://www.dn.se/nyheter/m/rss'
timeToSleep = 20 #seconds
dropBoxUserWeather = 'https://dl.dropboxusercontent.com/u/2082167/'
dropBoxUser = 'https://dl.dropboxusercontent.com/u/2082167/'
def main():
	currentMessage = 'Starting...'
	writeToLed(currentMessage,'4')
	time.sleep(2)
	while True:
		dropboxInfo = checkDropBox(dropBoxUser,'ledbadge.txt')
		if len(dropboxInfo) == 0:
			dropboxInfo = ' '
		elif dropboxInfo.lower().strip() == 'news':
			wantedMessage = fetchRss('random')
		elif dropboxInfo[0:4].lower().find('news') != -1 and len(dropboxInfo.split()) > 1:
			print 'News detected'
			print dropboxInfo
			wantedMessage = fetchRss(dropboxInfo.split()[1].lower())
		elif dropboxInfo.lower() == 'ip':
			print 'IP detected'
			print dropboxInfo
			wantedMessage = 'IP: '+str(os.popen("ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'").read()).strip()
			print 'wantedMessage:',wantedMessage
		elif dropboxInfo.lower() == 'update':
			print 'Update triggered'
			tempText = updateGit()
			print 'Return from update prompt:', tempText
			if tempText.find('Already up-to-date') != -1:
				wantedMessage = 'Nothing new to update'
			elif tempText.find('Updating') != -1:
				wantedMessage = 'Update complete'
		elif dropboxInfo.lower() == 'weather':
			print 'Weather detected'
			print dropboxInfo
			wantedMessage = checkDropBox(dropBoxUserWeather,'weather.txt') #Weather
		else:
			wantedMessage = dropboxInfo
		if wantedMessage.lower() == 'fix': #Escape to try to restore  
			writeToLed('Trying to restore','4')
			time.sleep(7)
			writeToLed('Trying to restore, try to update dropbox file now.','4')
			wantedMessage = 'Update dropbox file now'

		if wantedMessage == currentMessage:
			print 'Nothing new...'
		else:
			writeToLed(wantedMessage,'4')
			currentMessage = wantedMessage
			
		print 'Now sleeping'
		for i in range(0,timeToSleep):
			print timeToSleep-i
			time.sleep(1)
	print '.'

def updateGit():
	return os.popen('python /home/pi/gitUpdate.py').read().strip()
	
def writeToLed(msg,spd):
	maxTextLength = 150
	if len(msg) == 0:
		msg = '...nothing to write, try fix...or reboot...'
	if len(msg) > maxTextLength:
		msg = msg[0:maxTextLength]
		print 'Shortening text'
	print len(msg), 'Writing this to led:', msg
	os.system("stty speed 38400 <" + DEVICE)
	f = open(DEVICE, "w")
	pkts = badge.build_packets(0x600, badge.message_file(msg, speed=spd, action=badge.ACTION_ROTATE))
	for p in pkts:
		f.write(p.format())
	f.flush()
	f.close()

def checkDropBox(url,file):
	print 'Now connecting to dropbox'
	os.system("wget -q "+url+file+" -N") #https://dl.dropboxusercontent.com/u/2082167/ledbadge.txt -N")
	file = open(file,"r")
	dropboxInfo = file.read()
	file.close()
	print 'Read from dropbox:',dropboxInfo
	return dropboxInfo
	
def fetchRss(feed):
	allFeeds=['http://www.dn.se/nyheter/m/rss','http://rss.cnn.com/rss/edition.rss','http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989']
	feedTitle = random.randint(0,3)
	print 'Looking for title number',feedTitle
	if feed == 'random':
		print 'Random feed'
		return fetchRss(allFeeds[random.randint(0,2)])
	if feed == 'cnn':
		print 'CNN'
		return fetchRss(allFeeds[1])
	if feed == 'dn':
		print 'DN'
		return fetchRss(allFeeds[0])
	if feed == 'Al-Jazeera':
		print feed
		return fetchRss(allFeeds[2])
	elif feed == allFeeds[0]:
		print 'Feed detected:',feed
		os.system('wget '+feed+' -O rss')
		f = open('rss','r')
		iterator = 0
		for line in f:
			#temp = line.find('[CDATA')
			temp = line.find('<title>')
			if temp != -1 and line.find('Nyheter - Nyheter') == -1:
				message =  line[temp:].split('[')[2].split(']')[0]
				if iterator == feedTitle:
					return 'DN: '+message
				else:
					iterator += 1
		f.close()
	
	elif feed == allFeeds[1]:
		print 'Feed detected:', feed
		os.system('wget '+feed+' -O rss')
		f = open('rss','r')
		iterator = 0
		for line in f:
			temp = line.find('<title>')
			if temp != -1 and line.find('CNN.com - Top Stories') == -1:
				message = line.split('<')[1].split('>')[1]
				print message
				if iterator == feedTitle:
					return 'CNN: '+message
				else:
					iterator += 1
	elif feed == allFeeds[2]:
		print 'Feed detected:', feed
		os.system('wget '+feed+' -O rss')
		f = open('rss','r')
		iterator = 0
		for line in f:
			temp = line.find('<title>')
			if temp != -1 and line.find('AJE') == -1:
				message = line.split('<')[1].split('>')[1]
				print message
				if iterator == feedTitle:
					return 'Al-Jazeera: '+message
				else:
					iterator += 1
	else:
		print 'Feed not supported:',feed
		return 'Feed not supported'
	
	
main()
