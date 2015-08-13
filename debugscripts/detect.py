import sys
import urllib2
import string

avail_unames = []

try:
	user = 'lksjdflkj'
	url = 'http://' + user + '.deviantart.com/' # I know this account is deactivated
	
	page = urllib2.urlopen(url)
	data = page.read()
except urllib2.HTTPError, e:
	if e.read().find("This account is inactive.") == -1:
		print user + ' is available!'
		avail_unames += [user]
	else:
		print 'This account is inactive.'

file = open("test_names.txt", "w")
for uname in avail_unames:
	file.write(uname + '\n')