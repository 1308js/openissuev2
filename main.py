#!/usr/bin/python
import json
from pprint import pprint
import urllib2   #module for http requests
import re 		#module for regular expression
import datetime  #module for time function
#fucntion to check the validity of the url
def checkUrl(url):
	a='((http://)|(https://))?(www.)?(github.com/)'  ##regular expression for valid url according to app
	a=re.compile(a)									
	if(a.match(url)):							
		return 1   									# return success if valid url
	else:
		return 0			
def useUrl(url):									##function to extract useful part of url
	a='((http://)|(https://))?(www.)?(github.com)'   
	url=re.sub(a,'',url)
	if(url[len(url)-7:]=='/issues'):  ##check if the url consist issue part or not
		pass	
	else:
		if(url[len(url)-1]=='/'):
			url+='issues'		
		else:
			url+='/issues'			
	return url

while(1):											#Infinite loop for cheking different urls						
	url=raw_input("Enter the public github profile to check open issues\n")    ##input from user for url
	if(checkUrl(url)):											##if url is valid
		url='https://api.github.com/repos'+useUrl(url)+'?state=open'					##modifying url according to github api needs
		try:
			r=urllib2.urlopen(url)							
			bytecode=r.read()									##reading the response of the request
			r.close()				
			print "Wait your request is being made::"							
		except urllib2.HTTPError,error:
			bytecode=error.read()

		
		#print type(bytecode)
		bytecode.split('\n')
		data=''
		for i in bytecode:
			data+=i.strip()
		#print data

		openmatch='("state":"open",).*?("updated_at":")([0-9A-Z-:]{20})'			
		#openmatch='("state": "open",)'
		currentTime=datetime.datetime.now()
		today=0
		thisWeek=0
		old=0
		a=re.findall(openmatch,data)
		for k in a:
			openedTime=datetime.datetime(int(k[2][:4]),int(k[2][5:7]),int(k[2][8:10]),int(k[2][11:13]),int(k[2][14:16]),int(k[2][17:19]))
			timeDifference=(currentTime-openedTime).days*24+(currentTime-openedTime).seconds/3600-5.5
			if(timeDifference<=24):
				today+=1
					###if number difference between current and last opened is under 1 Week						
			elif(timeDifference>=24 and timeDifference<=168):
				thisWeek+=1
					###if number difference between current and last opened is older than 1 week						
			else:
				old+=1
		pagination=2
		if(a):
			while(1):
				newUrl=url+'&page='+str(pagination)
				pagination+=1
				try:
					r=urllib2.urlopen(newUrl)							
					bytecode=r.read()									##reading the response of the request
					r.close()				
					#print "Wait your request is being made::"							
				except urllib2.HTTPError,error:
					bytecode=error.read()
	
				bytecode.split('\n')
				data=''
				for i in bytecode:
					data+=i.strip()
				openmatch='("state":"open",).*?("updated_at":")([0-9A-Z-:]{20})'			
				#openmatch='("state": "open",)'
				a=re.findall(openmatch,data)
				if(a):
					currentTime=datetime.datetime.now()
					for k in a:
						openedTime=datetime.datetime(int(k[2][:4]),int(k[2][5:7]),int(k[2][8:10]),int(k[2][11:13]),int(k[2][14:16]),int(k[2][17:19]))
						timeDifference=(currentTime-openedTime).days*24+(currentTime-openedTime).seconds/3600-5.5
						if(timeDifference<=24):
							today+=1
								###if number difference between current and last opened is under 1 Week						
						elif(timeDifference>=24 and timeDifference<=168):
							thisWeek+=1
								###if number difference between current and last opened is older than 1 week						
						else:
							old+=1
				else:
					break	
		print "total :%d" %(today+thisWeek+old)
        print "Number of  issued  opened within 24 hours:           %d"	%today
        print "Number of issues opened between 24 hours and 7 days: %d" %thisWeek
        print "Number of issues opened more than 7 days ago:        %d" %old

	###user response for continueing programm
	response=raw_input("press y/Y to continue or any other key to exit\n")
	if(response=='y' or response=='Y'):
		pass
	else:
		break	
    
