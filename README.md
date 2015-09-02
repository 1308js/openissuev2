# openissuev2
Another python utiity to get the details of opened issue from a public github directory implemented using github APIs

######################################
Uses :
:~run the file main.py
:~ This will ask you for the github directory link.
Valid directory links that can be given 
	https://github.com/user/directory/issues
	http://github.com/user/directory/issues
	https://www.github.com/user/directory/issues
	http://www.github.com/user/directory/issues
	https://github.com/user/directory
	https://github.com/user/directory/

Output format:
	Number of total open issues :                        234
	Number of  issued  opened within 24 hours:           2
	Number of issues opened between 24 hours and 7 days: 8
	Number of issues opened more than 7 days ago:        224
	
Next:
	After this it will ask you whether you want to continue or not



########################################
Issues:
This utility is implemented using unauthenticated requests. So after some time you may get unwanted result as github allows a limited number of APIs queries made by single IP in a particular timespan.
Ractification:
	Same utility can be implemented with minor modification to use authenticated queries so that the request limit can be increased. 