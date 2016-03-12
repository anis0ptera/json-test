import urllib.request
import json
#import xmlrpc.client
#from xml.dom.minidom import parseString

def getPageJson(url):
	
	serviceurl = url
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

	print ('Retrieving', serviceurl)

	headers={'User-Agent':user_agent,}
	request=urllib.request.Request(url,None,headers)
	uh = urllib.request.urlopen(request)
	hdata = uh.read()

	print ('Retrieved',len(hdata),'characters')

	datas = json.loads(hdata.decode("utf8"))
	return datas
	

page=0
grandTrue=0
grandFalse=0
grandUnassigned=0

f = open('viki-json-test.txt','w')

while True:
	page+=1
	surl = 'http://api.viki.io/v4/videos.json?app=100250a&per_page=10&page=' + str(page)

	#print (surl)
	jdata = getPageJson(surl)

	print("more: ",jdata["more"])

	if jdata["more"] != True:
		break

	true = 0
	false = 0
	unassigned = 0
	for rix in range(len(jdata["response"])):
		#print(jdata["response"][rix]["flags"]["hd"])
		if jdata["response"][rix]["flags"]["hd"] == True:
			true+=1
		elif jdata["response"][rix]["flags"]["hd"] == False:
			false+=1
		else:
			unassigned+=1
			
	grandTrue += true
	grandFalse += false
	grandUnassigned += unassigned
	
	print ("")
	print ("Total hd=true for page ",page,": ",true)
	print ("Total hd=false for page ",page,": ",false)
	print ("Total unassigned for page ",page,": ",unassigned)

	f.write("\n")
	f.write("Total hd=true for page "+str(page)+": "+str(true)+"\n")
	f.write("Total hd=false for page "+str(page)+": "+str(false)+"\n")
	f.write("Total unassigned for page "+str(page)+": "+str(unassigned)+"\n")


print ("")

print ("Grand total hd=true: ",grandTrue)
print ("Grand total hd=false: ",grandFalse)
print ("Grand total hd=unassigned: ",grandUnassigned)

f.write("\n\n")
f.write("Grand total hd=true: "+str(grandTrue)+"\n")
f.write("Grand total hd=false: "+str(grandFalse)+"\n")
f.write("Grand total unassigned: "+str(grandUnassigned)+"\n")
f.close()
