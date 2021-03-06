import json
import csv
import time
from pprint import pprint


# a class to store the entire data of clicks and keys
class Data:
	def __init__(self, clicks, keystrokes):
		self.clicks = clicks
		self.keystrokes = keystrokes
		self.ccount = len(clicks)
		self.kcount = len(keystrokes)

	def getclickscount(self):
		return self.ccount

	def getkeyscount(self):
		return self.kcount

	# def gettimespanofwindow(self,clicks):
	# 	#print len(clicks)
	# 	if clicks[0][0:5]=="mouse":
	# 		first=clicks[0].split(',')
	# 		last=clicks[len(clicks)-1].split(',')
	# 		index=first[2].find('.')
	# 		index1=last[2].find('.')
	# 		return int(last[2][0:index1])-int(first[2][0:index])
	# 	else:
	# 		first=clicks[0].split(',')
	# 		last=clicks[len(clicks)-1].split(',')
	# 		index=first[0].find('.')
	# 		index1=last[0].find('.')
	# 		return int(last[0][0:index1])-int(first[0][0:index])


def getvector(date):
	vector = []
	vector.append(['Time', 'No of clicks', 'No of keystrokes', 'Window Title'])
	sdate_time = date + ' 09:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	print type(time)
	sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
	print sepoch
	eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
	while (sepoch != eepoch):
		twindows = []
		mclicks = 0
		keystrokes = 0
		x=" "
		for event in events:
			if "mouse" in event:
				e = event.split(',')
				if sepoch<=int(float(e[2]))<=sepoch+60:
					#print type(e[4])
					twindows.append(windows.get(int(e[4])))
					mclicks = mclicks + 1;
			else:
				e = event.split(',')
				if sepoch<=int(float(e[0]))<=sepoch+60:
					twindows.append(windows.get(int(e[1])))
					keystrokes = keystrokes + 1
		for twindow in twindows:
			x = x + str(twindow)
		vector.append([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sepoch)), mclicks, keystrokes, x])
		sepoch = sepoch + 60
	with open('vector.csv', 'w') as fp:
		a = csv.writer(fp, delimiter=',');
		a.writerows(vector)


def getevents(date):
	events = []
	print date
	sdate_time = date + ' 09:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	print type(time)
	sepoch = float(time.mktime(time.strptime(sdate_time, pattern)))
	print sepoch
	eepoch = float(time.mktime(time.strptime(edate_time, pattern)))
	with open('keylog&clicklog.txt') as f:
		for line in f:
			# print line
			if "mouse" in line:
				# print line
				e = line.split(',')
				# print e[2][0:2]
				if sepoch <= float(e[2]) <= eepoch:
					# print line
					events.append(line)
			else:
				# print line
				e1 = line.split(',')
				if sepoch <= float(e1[0]) <= eepoch:
					# print line
					events.append(line)
	return events


def timespan(value):
	time1 = []
	event1 = ""
	event2 = ""
	flag = 0
	# print value
	for event in events:
		temp = event.split(",")
		# print event
		if len(temp) > 3:
			if temp[4] == str(value):
				flag = 1
				if event1 == "":
					event1 = event
				# print 'event',event1
				else:
					event2 = event
			else:
				if flag == 1:
					clicks1 = []
					clicks1.append(event1)
					if event2 != "":
						clicks1.append(event2)
					# print event1,"###",event2
					# print clicks1[0],'##',len(clicks1)
					time1.append(gettimespanofwindow(clicks1))
					event1 = ""
					event2 = ""
					flag = 0
		else:
			if temp[1] == str(value):
				flag = 1
				if event1 == "":
					event1 = event
				else:
					event2 = event
			else:
				if flag == 1:
					clicks1 = []
					clicks1.append(event1)
					if event2 != "":
						clicks1.append(event2)
					# print event1," ",event2
					# print clicks1[0],'###'
					time1.append(gettimespanofwindow(clicks1))
					event1 = ""
					event2 = ""
					flag = 0
	return ttime(time1)


def gettimespanofwindow(clicks):
	# print 'time',clicks[0][0:5]
	first = clicks[0].split(',')
	last = clicks[len(clicks) - 1].split(',')
	if clicks[0][0:5] == "mouse":
		# print "if"
		index = first[2].find('.')
		num1 = int(first[2][0:index])
	else:
		# print "else"
		index = first[0].find('.')
		num1 = int(first[0][0:index])

	if clicks[len(clicks) - 1][0:5] == "mouse":
		# print "second if"
		index1 = last[2].find('.')
		num2 = int(last[2][0:index1])
	else:
		index1 = last[0].find('.')
		num2 = int(last[0][0:index1])
	# print num2-num1
	return num2 - num1


def ttime(time1=[]):
	time2 = 0
	for t in time1:
		time2 = time2 + t
	return time2


events = []
totalnoevents = 0
count = 0;
# report array used for  csv file
report = []
report.append(['No of clicks', 'No of keystrokes', 'Time span', 'Window Title'])
# opening the clicks and keystrokes file and stored them as a string in events array
# with open('keylog&clicklog.txt') as f:
#     for line in f:
# 		if line[0:5]=="mouse": 
# 			#print line	
# 			e=line.split(',')
# 			#print e[2][0:2]
# 			if e[2][0:2]=="14":
# 				#print line
# 				events.append(line)		
# 		else:
# 			e1=line.split(',')
# 			if e1[0][0:2]=="14":
# 				#print line
# 				events.append(line)
events = getevents('01.02.2016')
totalnoevents = len(events)
print"Total no of clicks  " + str(len(events))

# opening windows file store each value in dict along with data object
with open('keylog&clicklogwin.json') as data_file:
	data = json.load(data_file)
# dict with key as window title and data as object of class Data
dict = {}
windows = {}
noofwindowtitles = 0
for attribute, value in data.iteritems():
	timein = ""
	noofwindowtitles = noofwindowtitles + 1
	click = []
	keystroke = []
	for event in events:
		temp = event.split(",")
		# print temp[0][0:5]
		if temp[0][0:5] == "mouse":
			# print "value" + str(value)
			# print "temp[4]"+ temp[4]
			if temp[4] == str(value):
				# print "in"
				click.append(event)

		else:
			# print "in keystroke"
			if temp[1] == str(value):
				keystroke.append(event)
	# print click
	# print keystroke
	count = count + len(click)
	count = count + len(keystroke)
	data = Data(click, keystroke)
	if len(click) != 0:
		t = timespan(value)
		m, s = divmod(t, 60)
		h, m = divmod(m, 60)
		timein = str(h) + ':' + str(m) + ':' + str(s)

	dict[attribute] = data
	# print(attribute)
	# print data.getkeyscount()
	# print data.getclickscount()
	report.append([str(data.getclickscount()), str(data.getkeyscount()), timein, (attribute.replace(u"\ufffd", "?"))])
	windows[value] = (attribute.replace(u"\ufffd", "?"))
for attribute, value in windows.iteritems():
	print 	type(attribute), value
getvector('01.02.2016')
# writing in to a csv file named report.csv
with open('report.csv', 'w') as fp:
	a = csv.writer(fp, delimiter=',')
	a.writerows(report)
# print count
# print nofowindowtitles
