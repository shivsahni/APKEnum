#!/usr/bin/python
import os
import sys
import ntpath
import time
import re
import urlparse, urllib2
import hashlib
import thread
import traceback

class bcolors:
    TITLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    INFO = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    UNDERLINE = '\033[4m'
    FGWHITE = '\033[37m'
    FAIL = '\033[95m'



rootDir=os.path.expanduser("~")+"/.SourceCodeAnalyzer/" #ConfigFolder ~/.SourceCodeAnalyzer/
projectDir=""
apkFilePath=""
apkFileName=""
apkHash=""
scopeMode=False


scopeList=[]


authorityList=[]
inScopeAuthorityList=[]
publicIpList=[]
s3List=[]
s3WebsiteList=[]


urlRegex='(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'#regex to extract domain
apktoolPath="./Dependencies/apktool_2.4.1.jar"
s3Regex1="https://(.+?)\.s3\..+?\.amazonaws\.com\/.+?"
s3Regex2="https://s3\..+?\.amazonaws\.com\/(.+?)\/.+?"
s3Regex3="S3://(.+?)/"
s3Website1="https*://(.+?)\.s3-website\..+?\.amazonaws\.com"
s3Website2="https*://(.+?)\.s3-website-.+?\.amazonaws\.com"
publicIp="https*://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31))(?<!127)(?<!^10)(?<!^0)\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!192\.168)(?<!172\.(16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31))\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(?<!\.255$))"

def myPrint(text, type):
	if(type=="INFO"):
		print bcolors.INFO+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="INFO_WS"):
		print bcolors.INFO+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="PLAIN_OUTPUT_WS"):
		print bcolors.INFO+text+bcolors.ENDC
		return
	if(type=="ERROR"):
		print bcolors.BGRED+bcolors.FGWHITE+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="MESSAGE_WS"):
		print bcolors.TITLE+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="MESSAGE"):
		print bcolors.TITLE+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="INSECURE"):
		print bcolors.OKRED+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="INSECURE_WS"):
		print bcolors.OKRED+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="OUTPUT"):
		print bcolors.OKBLUE+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return
	if(type=="OUTPUT_WS"):
		print bcolors.OKBLUE+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="SECURE_WS"):
		print bcolors.OKGREEN+bcolors.BOLD+text+bcolors.ENDC
		return
	if(type=="SECURE"):
		print bcolors.OKGREEN+bcolors.BOLD+text+bcolors.ENDC+"\n"
		return


def isNewInstallation():
	if (os.path.exists(rootDir)==False):
		myPrint("Thank you for installing APKEnum", "OUTPUT_WS")
		os.mkdir(rootDir)
		return True
	else:
		return False

def isValidPath(apkFilePath):
	global apkFileName
	myPrint("I: Checking if the APK file path is valid.", "INFO_WS")
	if (os.path.exists(apkFilePath)==False):
		myPrint("E: Incorrect APK file path found. Please try again with correct file name.", "ERROR")
		print
		exit(1)
	else:
		myPrint("I: APK File Found.", "INFO_WS")
		apkFileName=ntpath.basename(apkFilePath)

def printList(lst):
	counter=0
	for item in lst:
		counter=counter+1
		entry=str(counter)+". "+item
		myPrint(entry, "PLAIN_OUTPUT_WS")

def reverseEngineerApplication(apkFileName):
	global projectDir
	myPrint("I: Initiating APK decompilation process", "INFO_WS")
	projectDir=rootDir+apkFileName+"_"+hashlib.md5().hexdigest()
	if (os.path.exists(projectDir)==True):
		myPrint("I: The APK is already decompiled. Skipping decompilation and proceeding with scanning the application.", "INFO_WS")
		return projectDir
	os.mkdir(projectDir)
	myPrint("I: Decompiling the APK file using APKtool.", "INFO_WS")
	result=os.system("java -jar "+apktoolPath+" d "+"--output "+'"'+projectDir+"/apktool/"+'"'+' "'+apkFilePath+'"'+'>/dev/null')
	if (result!=0):
		myPrint("E: Apktool failed with exit status "+str(result)+". Please Try Again.", "ERROR")
		print
		exit(1)
	myPrint("I: Successfully decompiled the application. Proceeding with scanning code.", "INFO_WS")

def findS3Bucket(line):
	temp=re.findall(s3Regex1,line)
	if (len(temp)!=0):
		for element in temp:
			s3List.append(element[0])


	temp=re.findall(s3Regex2,line)
	if (len(temp)!=0):
		for element in temp:
			s3List.append(element[0])


	temp=re.findall(s3Regex3,line)
	if (len(temp)!=0):
		for element in temp:
			s3List.append(element[0])


def findS3Website(line):
	temp=re.findall(s3Website1,line)
	if (len(temp)!=0):
		for element in temp:
			s3WebsiteList.append(element[0])

	temp=re.findall(s3Website2,line)
	if (len(temp)!=0):
		for element in temp:
			s3WebsiteList.append(element[0])


def findUrls(line):
	temp=re.findall(urlRegex,line)
	if (len(temp)!=0):
		for element in temp:
			authorityList.append(element[0]+"://"+element[1])
			if(scopeMode):
				for scope in scopeList:
					if scope in element[1]:
						inScopeAuthorityList.append(element[0]+"://"+element[1])

def findPublicIPs(line):
	temp=re.findall(publicIp,line)
	if (len(temp)!=0):
		for element in temp:
			publicIpList.append(element[0])


def identifyURLs():
	global domainList, authorityList, inScopeDomainList, inScopeAuthorityList
	filecontent=""
	for dir_path, dirs, file_names in os.walk(rootDir+apkFileName+"_"+hashlib.md5().hexdigest()):
		for file_name in file_names:
			try:
				fullpath = os.path.join(dir_path, file_name)
				fileobj= open(fullpath,mode='r')
				filecontent = fileobj.read()
				fileobj.close()
			except Exception as e:
				myPrint("E: Exception while reading "+fullpath,"ERROR")
			
			try:
				thread.start_new_thread(findUrls, (filecontent,))
				thread.start_new_thread(findPublicIPs, (filecontent,))
				thread.start_new_thread(findS3Bucket, (filecontent,))
				thread.start_new_thread(findS3Website, (filecontent,))
			except Exception as e:
				myPrint("E: Error while spawning threads", "ERROR")					
						
def displayResults():
	global inScopeAuthorityList, authorityList, s3List, s3WebsiteList, publicIpList
	inScopeAuthorityList=set(inScopeAuthorityList)
	authorityList=set(authorityList)
	s3List=set(s3List)
	s3WebsiteList=set(s3WebsiteList)
	publicIpList=set(publicIpList)
	if (len(authorityList)==0):
		myPrint("\nNo URL found", "INSECURE")
	else:
		myPrint("\nList of URLs found in the application", "SECURE")
		printList(authorityList)
		
	if(scopeMode and len(inScopeAuthorityList)==0):
		myPrint("\nNo in-scope URL found", "INSECURE")
	elif scopeMode:
		myPrint("\nList of in scope URLs found in the application", "SECURE")
		printList(inScopeAuthorityList)

	if (len(s3List)==0):
		myPrint("\nNo S3 buckets found", "INSECURE")
	else:
		myPrint("\nList of in S3 buckets found in the application", "SECURE")
		printList(s3List)

	if (len(s3WebsiteList)==0):
		myPrint("\nNo S3 websites found", "INSECURE")
	else:
		myPrint("\nList of in S3 websites found in the application", "SECURE")
		printList(s3WebsiteList)

	if (len(publicIpList)==0):
		myPrint("\nNo public IPs found", "INSECURE")
	else:
		myPrint("\nList of in public IPs found in the application", "SECURE")
		printList(publicIpList)
	print ""

####################################################################################################


####################################################################################################

print(bcolors.OKBLUE+""" 

:::'###::::'########::'##:::'##:'########:'##::: ##:'##::::'##:'##::::'##:
::'## ##::: ##.... ##: ##::'##:: ##.....:: ###:: ##: ##:::: ##: ###::'###:
:'##:. ##:: ##:::: ##: ##:'##::: ##::::::: ####: ##: ##:::: ##: ####'####:
'##:::. ##: ########:: #####:::: ######::: ## ## ##: ##:::: ##: ## ### ##:
 #########: ##.....::: ##. ##::: ##...:::: ##. ####: ##:::: ##: ##. #: ##:
 ##.... ##: ##:::::::: ##:. ##:: ##::::::: ##:. ###: ##:::: ##: ##:.:: ##:
 ##:::: ##: ##:::::::: ##::. ##: ########: ##::. ##:. #######:: ##:::: ##:
..:::::..::..:::::::::..::::..::........::..::::..:::.......:::..:::::..::
	"""+bcolors.OKRED+bcolors.BOLD+"""         				
                  # Developed By Shiv Sahni - @shiv__sahni
"""+bcolors.ENDC)


if (len(sys.argv)<3):
	myPrint("E: Please provide the required arguments to initiate", "ERROR")
	print ""
	myPrint("E: Usage: python APKEnum.py -p/--path <apkPathName> [ -s/--scope \"comma, seperated, list\"]","ERROR")
	myPrint("E: Please try again!!", "ERROR") 
	print ""
	exit(1);

if ((len(sys.argv)>4) and (sys.argv[3]=="-s" or sys.argv[3]=="--scope")):
	scopeString=sys.argv[4].strip()
	scopeList=scopeString.split(',')
	if len(scopeList)!=0:
		scopeMode=True

if (sys.argv[1]=="-p" or sys.argv[1]=="--path"):
	apkFilePath=sys.argv[2]
	try:
		isNewInstallation()
		isValidPath(apkFilePath)
		reverseEngineerApplication(apkFileName)
		identifyURLs()
		displayResults()
	except KeyboardInterrupt:
		myPrint("I: Acknowledging KeyboardInterrupt. Thank you for using APKEnum", "INFO")
		exit(0)
myPrint("Thank You For Using APKEnum","OUTPUT")