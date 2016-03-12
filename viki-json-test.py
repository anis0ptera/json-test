#! /usr/bin/python

import urllib.request
import json

def getPageJson(url):
	
	# Accepts URL string and returns JSON object in string form
	serviceurl = url
	
	# Program needs to mimic a browser by presenting user agent
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}

	print ('Retrieving', serviceurl)

	# Making request to address via URL
	request=urllib.request.Request(url,None,headers)
	uh = urllib.request.urlopen(request)
	hdata = uh.read()

	print ('Retrieved',len(hdata),'characters')

	# Return decoded JSON in string form
	datas = json.loads(hdata.decode("utf8"))
	return datas
	
# Initialize counter vars
page=0
grandTrue=0
grandFalse=0
grandUnassigned=0

# Open output file
f = open('viki-json-test.txt','w')

# Main loop
while True:
	# Increment page and build URL for page
	page+=1
	surl = 'http://api.viki.io/v4/videos.json?app=100250a&per_page=10&page=' + str(page)

	# Call the function to retrieve JSON
	jdata = getPageJson(surl)

	# Test page for more value
	print("more: ",jdata["more"])

	# Break loop on last page
	if jdata["more"] != True:
		break

	# Initialize counter vars
	true = 0
	false = 0
	unassigned = 0
	
	# Loop for geting hd values
	for rix in range(len(jdata["response"])):
		#print(jdata["response"][rix]["flags"]["hd"])
		if jdata["response"][rix]["flags"]["hd"] == True:
			true+=1
		elif jdata["response"][rix]["flags"]["hd"] == False:
			false+=1
		else:
			unassigned+=1
			
	# Increment grand totals-
	grandTrue += true
	grandFalse += false
	grandUnassigned += unassigned
	
	# print totals to the screen
	print ("")
	print ("Total hd=true for page ",page,": ",true)
	print ("Total hd=false for page ",page,": ",false)
	print ("Total unassigned for page ",page,": ",unassigned)

	# print totals to file
	f.write("\n")
	f.write("Total hd=true for page "+str(page)+": "+str(true)+"\n")
	f.write("Total hd=false for page "+str(page)+": "+str(false)+"\n")
	f.write("Total unassigned for page "+str(page)+": "+str(unassigned)+"\n")

# print grand totals to the screen
print ("")
print ("Grand total hd=true: ",grandTrue)
print ("Grand total hd=false: ",grandFalse)
print ("Grand total hd=unassigned: ",grandUnassigned)

# print grand totals to file
f.write("\n\n")
f.write("Grand total hd=true: "+str(grandTrue)+"\n")
f.write("Grand total hd=false: "+str(grandFalse)+"\n")
f.write("Grand total unassigned: "+str(grandUnassigned)+"\n")
f.close()
