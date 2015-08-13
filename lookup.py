import sys
import urllib2
import string
import threading
import Queue
import time

# Multithreading framework based off of  http://stackoverflow.com/questions/16199793/python-3-3-simple-threading-event-example

# Debug arguments

def get_cur_millis():
	return time.time() * 1000

# http://bytes.com/topic/python/answers/600880-formatting-milliseconds-certain-string
def get_eta_str(start_millis, end_millis, units):
	duration = int(end_millis) - int(start_millis)
	t = duration * units
	return time.strftime("%H:%M:%S", time.gmtime(t/1000)) + ',%03d' % (t%1000)

num_unames_checked = 0
avail_unames = []
last_time = get_cur_millis()
	
alphabet = string.lowercase
digits = '1234567890'
chars = alphabet + digits

if len(sys.argv) < 2:
	print 'Too few arguments. Reference the README.'
	sys.exit()

homepage = sys.argv[1]
format = ''
num_threads = 2

underscores = False
hyphens = False
for i in range(2, len(sys.argv)):
	arg = sys.argv[i]
	if arg == 'b' or arg == 'a':
		format = arg
	elif arg == 'u':
		underscores = True
	elif arg == 'h':
		hyphens = True
	elif arg.startswith('t'):
		num_threads = int(arg[1:])

if underscores:
	chars += '_'
if hyphens:
	chars += '-'
print chars

if format != 'b' and format != 'a':
	print 'No format specified.'
	sys.exit()
	
num_possible_names = len(chars) * len(chars) * len(chars)

# lock to serialize console output
lock = threading.Lock()

def do_work(user):
	global num_unames_checked
	global avail_unames
	
	num_unames_checked += 1
	
	start_time = get_cur_millis()
	
	try:
		url = 'http://'
		
		if format == 'b':
			url += user + '.' + homepage + '/'
		else:
			url += homepage + '/' + user
			
		# print url
		
		page = urllib2.urlopen(url)
		# data = page.read()
		# print data
	except urllib2.HTTPError, e:
		if e.read().find("This account is inactive.") == -1:
			print user + ' is available!'
			avail_unames += [user]
			
	end_time = get_cur_millis()
	eta_str = get_eta_str(start_time, end_time, num_possible_names - num_unames_checked)
			
	if num_unames_checked % 100 == 0:
		print '-- ETA ' + eta_str + ' (%d/%d)' % (num_unames_checked,num_possible_names)
	
	# Make sure the whole print completes or threads can mix up output in one line.
	with lock:
		pass#print(threading.current_thread().name,user)

# The worker thread pulls an item from the queue and processes it
def worker():
	while True:
		item = q.get()
		do_work(item)
		q.task_done()

# Create the queue and thread pool.
q = Queue.Queue()
for i in range(num_threads):
	 t = threading.Thread(target=worker)
	 t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
	 t.start()

# stuff work items on the queue (in this case, just a number).
for char1 in chars: # First char
	for char2 in chars: # Second char
		for char3 in chars: # Third char
			user = char1 + char2 + char3
			q.put(user)

q.join()	   # block until all tasks are done

avail_unames = sorted(avail_unames)

file = open("available_names.txt", "w")
for uname in avail_unames:
	file.write(uname + '\n')

