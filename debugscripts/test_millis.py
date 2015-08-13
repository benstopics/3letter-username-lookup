import time

def get_cur_millis():
	return time.time() * 1000

# http://bytes.com/topic/python/answers/600880-formatting-milliseconds-certain-string
def get_eta_str(start_millis, end_millis, units):
	print start_millis
	print end_millis
	print time.time() * 1000
	duration = int(end_millis) - int(start_millis)
	t = duration * units
	return time.strftime("%H:%M:%S", time.gmtime(t/1000)) + ',%03d' % (t%1000)

last_time = get_cur_millis()
print get_eta_str()