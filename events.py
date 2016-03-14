import time
import json
import csv
import os
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
directory = "./clean-dir"
def createtotalevents():
	count = 1
	total_events = {}
	for subdir,dirs, files in os.walk(directory):
	    #print len(files)
	    file1=""
	    file2=""
	    for file in files:
	    	if file.find("_win.txt") != -1:
	    		file1= os.path.join(subdir, file)
	    	if file.find("_clean_log.txt") != -1:
		    	file2=os.path.join(subdir, file) 
		#print file1
		if file1!="" and file2!="":
			total_events[count] = getevents(file1, file2)
			count=count+1
	return total_events


def printevents(total_events):
	count1 = 0
	while (count1 < len(total_events)):
		# print total_events.get(count1)
		count1 = count1 + 1


def getevents(filename, filename1):
	#print filename1+"djh "+filename
	events = []
	# print date
	sdate_time = date + ' 15:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	sepoch = float(time.mktime(time.strptime(sdate_time, pattern)))
	# print sepoch
	eepoch = float(time.mktime(time.strptime(edate_time, pattern)))
	#filename = filename + ".txt"
	#filename1 = filename1 + ".json"
	#print "filename"
	with open(filename) as data_file:
		data = json.load(data_file)
	windows = {}
	for attribute, value in data.iteritems():
		if attribute!='z':
			#print "attribute   " + attribute
			value1=attribute.decode('base64','strict')
			#print "decoded value "+ value1
			windows[value] = (value1)
	with open(filename1) as f:
		count=0
		for line in f:
			# print line
			if count!=0:
				#print "not"	
				if "mouse" in line:
					#print line
					e = line.split(',')
					#print e[2][0:2]
					if sepoch <= float(e[2]) <= eepoch:
						#print line
						#print (windows.get(int(e[4])))
						line = line + "," + str(windows.get(int(e[4])))
						# print line
						events.append(line)
				else:
					# print line
					e1 = line.split(',')
					if sepoch <= float(e1[0]) <= eepoch:
						# print line
						# print "in keys"
						#print (windows.get(int(e1[1])))
						line = line + "," + str(windows.get(int(e1[1])))
						# print line
						events.append(line)
			count=count+1
	print len(events)			
	return events


def getvector(total_events):
	vector = []
	data=[]
	pdf=[]
	pdftime=[]
	Sublime=[]
	Sublimetime=[]
	Word=[]
	Wordtime=[]
	Notepad=[]
	Notepadtime=[]
	data.append(['Time', 'Studentno 1'])
	vector.append(['Time', 'Studentno 1', 'Studentno 2', 'Studentno 3'])
	sdate_time = date + ' 15:00:00'
	edate_time = date + ' 18:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	#print type(time)
	sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
	#print sepoch
	eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
	while (sepoch != eepoch):
		twindows = []
		value = 0
		x = " "
		final=[" "]*(totalstudents+1)
		arr = [0] * (totalstudents+1)
		pdft = [0] * (totalstudents+1)
		txtt = [0] * (totalstudents+1)
		wrdt = [0] * (totalstudents+1)
		slmt = [0] * (totalstudents+1)
		arr1 = []
		windowframe=[0]*4
		for key in total_events:
				#print len(total_events[key])
				mclicks = 0
				keystrokes = 0
				for event in total_events[key]:
					if "mouse" in event:
						e = event.split(',')
						if sepoch <= int(float(e[2])) <= sepoch + 60:
							#print event
							#print mclicks
							mclicks = mclicks + 1;
							if ".pdf" in e[len(e)-1]:
								pdft[key]=key;
							elif "Sublime Text" in e[len(e)-1]:
								slmt[key]=key
							elif "Microsoft Word Document" in e[len(e)-1]:
								wrdt[key]=key
							elif ".txt" in e[len(e)-1]:
								txtt[key]=key
							else:
								continue

					else:
						e = event.split(',')
						if sepoch <= int(float(e[0])) <= sepoch + 60:
							keystrokes =keystrokes+1
							if ".pdf" in e[len(e)-1]:
								pdft[key]=key;
							elif "Sublime Text" in e[len(e)-1]:
								slmt[key]=key
							elif "Microsoft Word Document" in e[len(e)-1]:
								wrdt[key]=key
							elif ".txt" in e[len(e)-1]:
								txtt[key]=key
							else:
								continue
				arr[key]=(mclicks+keystrokes)
				arr1.append(windowframe)
		final[0]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sepoch))
		#print final[0]
		#print arr
		#print arr1
		# for pdf files
		for p in range(1,totalstudents+1):
			if pdft[p]!=0:
				pdf.append(pdft[p])
				pdftime.append(final[0])
		#print pdf
		#print pdftime
		# for sublime windows
		for p in range(1,totalstudents+1):
			if slmt[p]!=0:
				Sublime.append(slmt[p])
				Sublimetime.append(final[0])
		#print Sublime
		#print Sublimetime
		# for word files
		for p in range(1,totalstudents+1):
			if wrdt[p]!=0:
				Word.append(wrdt[p])
				Wordtime.append(final[0])
		#print Word
		#print Wordtime
		# for notepad files
		for p in range(1,totalstudents+1):
			if txtt[p]!=0:
				Notepad.append(txtt[p])
				Notepadtime.append(final[0])
		# for csv file
		for r in range(1,totalstudents+1):
			final[r]=str(arr[r])
		vector.append(final)
		t1=final[0].split(' ')
		timestamp=t1[len(t1)-1]

		for r in range(1,len(final)):
			data1=[]
			if(final[r]=="0"):
				#data1[0]=timestamp
				#data1[1]="0";
				data.append([timestamp[3:5],0])
			else:
				#data1[0]=timestamp
				#data1[1]=r;
				#print "r "+ r
				data.append([timestamp[3:5],r])
		
		sepoch = sepoch + 60
	with open('vector.csv', 'w') as fp:
		a = csv.writer(fp, delimiter=',');
		a.writerows(data)
	plotWindows(pdf,pdftime,Sublime,Sublimetime,Notepad,Notepadtime,Word,Wordtime)
	#print data
def plotWindows(pdf,pdftime,Sublime,Sublimetime,Notepad,Notepadtime,Word,Wordtime):
	trace0 = go.Scatter(
	    x = pdftime,
	    y = pdf,
	    name = 'PDF',
	    mode = 'markers',
	    marker = dict(
	        size = 10,
	        color = 'rgba(152, 0, 0, .8)',
	        line = dict(
	            width = 2,
	            color = 'rgb(0, 0, 0)'
	        )
	    )
	)

	trace1 = go.Scatter(
	    x = Sublimetime,
	    y = Sublime,
	    name = 'Sublime',
	    mode = 'markers',
	    marker = dict(
	        size = 10,
	        color = 'rgba(255, 182, 193, .9)',
	        line = dict(
	            width = 2,
	        )
	    )
	)
	
	trace2 = go.Scatter(
	    x = Notepadtime,
	    y = Notepad,
	    name = 'Notepad',
	    mode = 'markers',
	    marker = dict(
	        size = 10,
	        color = 'blue',
	        line = dict(
	            width = 2,
	        )
	    )
	)
	
	trace3 = go.Scatter(
	    x = Wordtime,
	    y = Word,
	    name = 'Word',
	    mode = 'markers',
	    marker = dict(
	        size = 10,
	        color = 'green',
	        line = dict(
	            width = 2,
	        )
	    )
	)
	data = [trace0, trace1, trace2, trace3]
	layout = dict(title = 'Styled Scatter',
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )
	fig = dict(data=data, layout=layout)
	plot(fig)

total_events = {}
totalstudents = 87
date = '01.03.2016'
getvector(createtotalevents())