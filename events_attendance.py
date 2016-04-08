import time
import json
import csv
import os
import operator
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
from collections import OrderedDict
from itertools import izip
from datetime import datetime
directory = "./clean-dir"

# def createtotalevents():
# 	count = 1
# 	total_events = {}
# 	for file in os.listdir(directory):
# 	    #print filename
# 	    #print " lenght of files" + str(len(files))
# 	    file1=""
# 	    file2=""
# 	    name=""
# 	    if file.find("_win_2016-04-01.txt") != -1:
# 	    	name=file
# 	    	file1= os.path.join(directory, file)
# 	    if file.find("_log_2016-04-01new.txt") != -1:
# 	    	file2=os.path.join(directory, file) 
# 		print file1
# 		print file2
# 		if file1!="" and file2!="":
# 			#print file1
# 			#print file2
# 			v=name.index("@")
# 			key=name[0:v]
# 			num2name[count]=key
# 			total_events[count] =getevents(file1, file2)
# 			count=count+1
# 	return total_events

def createtotalevents():
	filelist=[]
	file1=""
	file2=""
	count=0
	for file in os.listdir(directory):
		filelist.append(file)
	f=0
	while(f<len(filelist)):
		file1=filelist[f]
		name=file1
		f=f+1
		file2=filelist[f]
		f=f+1
		print file1
		print file2
		file1=os.path.join(directory, file1)
		file2=os.path.join(directory, file2)
		v=name.index("@")
		key=name[0:v]
		num2name[count]=key
		total_events[key] =getevents(file2, file1)
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
	sdate_time = date + ' 14:00:00'
	edate_time = date + ' 23:59:59'
	pattern = '%d.%m.%Y %H:%M:%S'
	sepoch = float(time.mktime(time.strptime(sdate_time, pattern)))
	print sepoch
	eepoch = float(time.mktime(time.strptime(edate_time, pattern)))
	#filename = filename + ".txt"
	#filename1 = filename1 + ".json"
	#print filename
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
		#print f
		for line in f:
			#print line
			#line=line.decode('base64','strict')
			#print line
			if count!=0 and  line[0]!=' ' and  line[0]!='*':
				#line=line.decode('base64','strict')
				#line=line.decode('base64','strict')
				#print line
				#print "not"	
				if "mouse" in line:
					#print line
					e = line.split(',')
					#print e[2][0:2]
					if sepoch <= float(e[1]) <= eepoch:
						#print line
						#print (windows.get(int(e[4])))
						line = line + "," + str(windows.get(int(e[2])))
						# print line
						events.append(line)
				else:
					
						#print line
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
	totaltime = [0] * (totalstudents+1)
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
	sdate_time = date + ' 14:00:00'
	edate_time = date + ' 24:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	#print type(time)
	sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
	#print sepoch
	eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
	while (sepoch != eepoch):
		twindows = []
		value = 0
		x = " "
		time1 = [0] * (totalstudents+1)
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
							time1[key]=1
							# if ".pdf" in e[len(e)-1]:
							# 	pdft[key]=key;
							# elif "Sublime Text" in e[len(e)-1]:
							# 	slmt[key]=key
							# elif "Microsoft Word Document" in e[len(e)-1]:
							# 	wrdt[key]=key
							# elif ".txt" in e[len(e)-1]:
							# 	txtt[key]=key
							# else:
							# 	continue

					else:
						e = event.split(',')
						if sepoch <= int(float(e[0])) <= sepoch + 60:
							keystrokes =keystrokes+1
							time1[key]=1
							# if ".pdf" in e[len(e)-1]:
							# 	pdft[key]=key;
							# elif "Sublime Text" in e[len(e)-1]:
							# 	slmt[key]=key
							# elif "Microsoft Word Document" in e[len(e)-1]:
							# 	wrdt[key]=key
							# elif ".txt" in e[len(e)-1]:
							# 	txtt[key]=key
							# else:
							# 	continue
				arr[key]=(mclicks+keystrokes)
				arr1.append(windowframe)
		final[0]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sepoch))
		#print final[0]
		#print arr
		#print arr1
		for t in range(0,totalstudents+1):
			totaltime[t]=totaltime[t]+time1[t]
		# for pdf files
		# for p in range(1,totalstudents+1):
		# 	if pdft[p]!=0:
		# 		pdf.append(pdft[p])
		# 		pdftime.append(final[0])
		# #print pdf
		# #print pdftime
		# # for sublime windows
		# for p in range(1,totalstudents+1):
		# 	if slmt[p]!=0:
		# 		Sublime.append(slmt[p])
		# 		Sublimetime.append(final[0])
		# #print Sublime
		# #print Sublimetime
		# # for word files
		# for p in range(1,totalstudents+1):
		# 	if wrdt[p]!=0:
		# 		Word.append(wrdt[p])
		# 		Wordtime.append(final[0])
		# #print Word
		# #print Wordtime
		# # for notepad files
		# for p in range(1,totalstudents+1):
		# 	if txtt[p]!=0:
		# 		Notepad.append(txtt[p])
		# 		Notepadtime.append(final[0])
		# # for csv file
		# for r in range(1,totalstudents+1):
		# 	final[r]=str(arr[r])
		# vector.append(final)
		# t1=final[0].split(' ')
		# timestamp=t1[len(t1)-1]

		# for r in range(1,len(final)):
		# 	data1=[]
		# 	if(final[r]=="0"):
		# 		#data1[0]=timestamp
		# 		#data1[1]="0";
		# 		data.append([timestamp[3:5],0])
		# 	else:
		# 		#data1[0]=timestamp
		# 		#data1[1]=r;
		# 		#print "r "+ r
		# 		data.append([timestamp[3:5],r])
		
		sepoch = sepoch + 60
	print totaltime
	# with open('vector.csv', 'w') as fp:
	# 	a = csv.writer(fp, deimiter=',');
	# 	a.writerows(data)
	# plotWindows(pdf,pdftime,Sublime,Sublimetime,Notepad,Notepadtime,Word,Wordtime)
	#print data


def generateidletime(total_events):
	sdate_time = date + ' 14:00:00'
	edate_time = date + ' 23:59:59'
	pattern = '%d.%m.%Y %H:%M:%S'
	keyandclicks={}
	for key in total_events:
		sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
		#print sepoch
		eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
		atime=0
		stime=0
		keystrokes=0;
		mouseclicks=0
		while(sepoch<=eepoch):
			stime=0
			for event in total_events[key]:
				if "mouse" in event:
					e = event.split(',')
					if sepoch <= int(float(e[1])) <= sepoch + 300:
						stime=5
						mouseclicks=mouseclicks+1			
				else:
					e = event.split(',')
					if sepoch <= int(float(e[0])) <= sepoch + 300:
						stime=5
						keystrokes=keystrokes+1
			atime=atime+stime
			sepoch = sepoch + 300
		#t=(eepoch - sepoch)/60
		idletime[key]=540-atime
		print key
		keyandclicks[key]=str(mouseclicks)+ " "+ str(keystrokes)
	sorted_x = sorted(idletime.items(), key=operator.itemgetter(1),reverse=True)
	print idletime
	print sorted_x
	idletimes=[]
	idletimes.append(['Student', 'Idletime','Keystrokes','Mouseclicks'])
	for l in sorted_x:
		k=keyandclicks[l[0]].split(" ")
		name=l[0].split("_")
		idletimes.append([name[0],l[1],k[1],k[0]])
	#print idletimes
	filename="IIIT-"+str(date)+".csv"
	with open(filename, 'wb') as fp:
			a = csv.writer(fp, delimiter=',');
			a.writerows(idletimes)



def mastersheet(total_events):
	sdate_time = date + ' 14:00:00'
	edate_time = date + ' 23:59:59'
	s2='05:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	for key in total_events:
		sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
		#print sepoch
		eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
		vector=[]
		vector.append(['Time', 'WindowTitle','Keystrokes','Mouseclicks'])
		idletimec=0
		start=0
		end=0
		flag=0
		while(sepoch<=eepoch):
			keystrokes=0.
			mouseclicks=0
			windowtitle=""
			for event in total_events[key]:
				if "mouse" in event:
					e = event.split(',')
					if sepoch <= int(float(e[1])) <= sepoch + 300:
						windowtitle=e[len(e)-1]
						mouseclicks=mouseclicks+1
				else:
					e = event.split(',')
					if sepoch <= int(float(e[0])) <= sepoch + 300:
						windowtitle=e[len(e)-1]
						keystrokes=keystrokes+1
			if windowtitle=="" and flag==0:
				start=sepoch
				flag=1
			if windowtitle!=""and flag==1:
				flag=0
				end=sepoch
				tb=time.strftime('%H:%M:%S', time.localtime(start))
				FMT = '%H:%M:%S'
				tdelta = datetime.strptime(tb, FMT) - datetime.strptime(s2, FMT)
				tbe=time.strftime('%H:%M:%S', time.localtime(end))
				tdelta1 = datetime.strptime(tbe, FMT) - datetime.strptime(s2, FMT)
				vector.append([str(tdelta)+" - "+str(tdelta1),"Not Active","0","0"])
			if windowtitle!="":
				flag=0
				tb=time.strftime('%H:%M:%S', time.localtime(sepoch))
				FMT = '%H:%M:%S'
				tdelta = datetime.strptime(tb, FMT) - datetime.strptime(s2, FMT)
				vector.append([str(tdelta),str(windowtitle),str(keystrokes),str(mouseclicks)])
			sepoch=sepoch+300
		filename=str(key)+".csv"
		with open(filename, 'wb') as fp:
			a = csv.writer(fp, delimiter=',');
			a.writerows(vector)
		print "wrote "+ filename +" ....."

def vector(total_events):
	sdate_time = date + ' 14:00:00'
	edate_time = date + ' 24:00:00'
	pattern = '%d.%m.%Y %H:%M:%S'
	for key in total_events:
		sepoch = int(time.mktime(time.strptime(sdate_time, pattern)))
		#print sepoch
		eepoch = int(time.mktime(time.strptime(edate_time, pattern)))
		vector=[]
		vector.append(['Time', 'WindowTitle'])
		while(sepoch<=eepoch):
			windowtitle=""
			for event in total_events[key]:
				if "mouse" in event:
					e = event.split(',')
					if sepoch <= int(float(e[1])) <= sepoch + 60:
						windowtitle=e[len(e)-1]
				else:
					e = event.split(',')
					if sepoch <= int(float(e[0])) <= sepoch + 60:
						windowtitle=e[len(e)-1]
			vector.append([str(time.strftime('%H:%M:%S', time.localtime(sepoch))),str(windowtitle)])
			sepoch=sepoch+60
		filename=str(key)+".csv"
		with open(filename, 'wb') as fp:
			a = csv.writer(fp, delimiter=',');
			a.writerows(vector)
		print "wrote "+ filename +" ....."

def plotWindows(pdf,pdftime,Sublime,Sublimetime,Notepad,Notepadtime,Word,Wordtime):
	trace0 = go.Scatter(
	    x = pdfpadtime,
	    y = pdftime,
	    name = 'pdf',
	    mode = 'markers',
	    marker = dict(
	        size = 10,
	        color = 'red',
	        line = dict(
	            width = 2,
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
num2name={}
total_events = {}
idletime={}
totalstudents = 0
date = '04.04.2016'
total_events=createtotalevents()
#vector(total_events)
generateidletime(createtotalevents())
#mastersheet(total_events)