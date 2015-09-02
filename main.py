#!/usr/bin/python
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

		
		
		bytecode.split('\n')        #######modifying response according to user needs
		data=''
		for i in bytecode:
			data+=i.strip()
		

		openmatch='("state":"open",).*?("created_at":")([0-9A-Z-:]{20})'		###pattern for extracting the time of opened issues	
	
		currentTime=datetime.datetime.now()    #####current time in IST (my laptop timing)
		today=0                       #########number of opened issues in less than 24 hours
		thisWeek=0 					##########number of opened issues in between 24 hours and 7 days								
		old=0 						########number of opened issues older than 7 days
		a=re.findall(openmatch,data)
		for k in a:
			openedTime=datetime.datetime(int(k[2][:4]),int(k[2][5:7]),int(k[2][8:10]),int(k[2][11:13]),int(k[2][14:16]),int(k[2][17:19])) ##last opened time of issue
			timeDifference=(currentTime-openedTime).days*24+(currentTime-openedTime).seconds/3600-5.5       #####time differnce in hours
			if(timeDifference<=24): 
				today+=1
					###if number difference between current and last opened is under 1 Week						
			elif(timeDifference>=24 and timeDifference<=168):
				thisWeek+=1
					###if number difference between current and last opened is older than 1 week						
			else:
				old+=1
		pagination=2     #######index for page number of api request
		if(a):     
			while(1):
				newUrl=url+'&page='+str(pagination)         #########modified url for every api request
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
				openmatch='("state":"open",).*?("created_at":")([0-9A-Z-:]{20})'		###pattern for extracting the time of opened issues		
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
		print "Total number of open issues:                         %d" %(today+thisWeek+old)
        print "Number of  issued  opened within 24 hours:           %d"	%today
        print "Number of issues opened between 24 hours and 7 days: %d" %thisWeek
        print "Number of issues opened more than 7 days ago:        %d" %old

	###user response for continueing programm
	response=raw_input("press y/Y to continue or any other key to exit\n")
	if(response=='y' or response=='Y'):
		pass
	else:
		break	
    
