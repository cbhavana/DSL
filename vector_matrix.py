import time
import json
import csv


def createtotalevents():
	count = 1
	total_events = {}
	while (count <= totalstudents):
		filename = str(count) + "keylog&clicklog"
		filename1 = str(count) + "keylog&clicklogwin"
		# print count
		total_events[count] = getevents(filename, filename1)
		count = count + 1
	return total_events


def printevents(total_events):
	count1 = 0
	while (count1 < len(total_events)):
		# print total_events.get(count1)
		count1 = count1 + 1


def getevents(filename, filename1):
	events = []
	# print date
	sdate_time = date + ' 09:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	sepoch = float(time.mktime(time.strptime(sdate_time, pattern)))
	# print sepoch
	eepoch = float(time.mktime(time.strptime(edate_time, pattern)))
	filename = filename + ".txt"
	filename1 = filename1 + ".json"
	with open(filename1) as data_file:
		data = json.load(data_file)
	windows = {}
	for attribute, value in data.iteritems():
		windows[value] = (attribute.replace(u"\ufffd", "?"))
	with open(filename) as f:
		for line in f:
			# print line
			if "mouse" in line:
				# print line
				e = line.split(',')
				# print e[2][0:2]
				if sepoch <= float(e[2]) <= eepoch:
					# print line
					#print type(windows.get(int(e[4])))
					line = line + "," + str(windows.get(int(e[4])))
					# print line
					events.append(line)
			else:
				# print line
				e1 = line.split(',')
				if sepoch <= float(e1[0]) <= eepoch:
					# print line
					# print "in keys"
					# print type(windows.get(int(e1[1])))
					line = line + "," + str(windows.get(int(e1[1])))
					# print line
					events.append(line)
	return events


def getvector(total_events):
	vector = []
	vector.append(['Time', 'Studentno 1', 'Studentno 2', 'Studentno 3', 'Studentno 4', 'Studentno 5',])
	sdate_time = date + ' 09:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	#print type(time)
	sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
	#print sepoch
	eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
	while (sepoch != eepoch):
		twindows = []
		mclicks = 0
		keystrokes = 0
		value = 0
		x = " "
		final=[" "]*(totalstudents+1)
		arr = [0] * totalstudents
		for key in total_events:
			#print key
			#with open('vector.csv', 'w') as fp:
				#a = csv.writer(fp, delimiter=',');
				for event in total_events[key]:
					if "mouse" in event:
						e = event.split(',')
						if sepoch <= int(float(e[2])) <= sepoch + 60:
							# print type(e[4])
							# twindows.append(windows.get(int(e[4])))
							mclicks = mclicks + 1;
							arr[key-1]=1;
							break
					else:
						e1 = event.split(',')
						if sepoch <= int(float(e1[0])) <= sepoch + 60:
							# twindows.append(windows.get(int(e[1])))
							print "i am in"
							keystrokes =keystrokes+1
							arr[key-1]=1
							break
				# if mclicks >0:
				# 	#print " key"
				# 	#print key
				# 	arr[key - 1] = 1
				# if keystrokes >0:
				# 	arr[key - 1] = 1
				final[0]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sepoch))
				#final.append(arr)
				for r in range(1,totalstudents+1):
					final[r]=str(arr[r-1])
		print final
		vector.append(final)
		sepoch = sepoch + 60
	with open('vector.csv', 'w') as fp:
		a = csv.writer(fp, delimiter=',');
		a.writerows(vector)
total_events = {}
totalstudents = 5
date = '31.01.2016'
getvector(createtotalevents())
