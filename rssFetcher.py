import os
rssFeed='http://www.dn.se/nyheter/m/rss'
#rssFeed='http://nlt.se/1.27311'
os.system('wget '+rssFeed+' -O rss')
headers = 1
f = open('rss','r')
outfile = open('news.txt','w')
i = 0
for line in f:
	temp = line.find('[CDATA')
	if temp != -1 and line.find('<img') == -1:
		message =  line[temp:].split('[')[2].split(']')[0]
		if message.find('Nyheter - Nyheter') == -1 and i < headers:
			outfile.write(message)
			print message
			i += 1
			
outfile.close()
