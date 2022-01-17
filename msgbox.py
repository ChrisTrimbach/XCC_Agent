"""import pdb, os
import subprocess
import re
from subprocess import Popen, PIPE

# This will only work within the netmask of the machine the program is running on cross router MACs will be lost
ip ="172.16.0.255"

#PING to place target into system's ARP cache 
process = subprocess.Popen(['ping', '-n', '1','-w','750', ip], stdout=subprocess.PIPE)
process.wait()

result = process.stdout.read()


#MAC address from IP
pid = Popen(["arp", "-a", ip], stdout=PIPE)
s = pid.communicate()[0]

# [a-fA-F0-9] = find any character A-F, upper and lower case, as well as any number
# [a-fA-F0-9]{2} = find that twice in a row
# [a-fA-F0-9]{2}[:|\-] = followed by either a ?:? or a ?-? character (the backslash escapes the hyphen, since the  # hyphen itself is a valid metacharacter for that type of expression; this tells the regex to look for the hyphen character, and ignore its role as an operator in this piece of the expression)
# [a-fA-F0-9]{2}[:|\-]? = make that final ?:? or ?-? character optional; since the last pair of characters won't be followed by anything, and we want them to be included, too; that's a chunk of 2 or 3 characters, so far
# ([a-fA-F0-9]{2}[:|\-]?){6} = find this type of chunk 6 times in a row
print s
if s !='No ARP Entries Found.\r\n':    
    test=s.split("Type");
    test= test[1].split(ip);
    test= test[1].split('dynamic');
    test= test[0].split('static');
    mac=re.sub(r" ", "" ,test[0])
    print mac

tes2= re.sub(r'Type.*$', "", s)

print tes2
""""""
print(re.sub(r"", "" ,mac))

s=
matchObj = re.match( r'Type', s, re.M|re.I)
if matchObj:
   print "matchObj.group() : ", matchObj.group()
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
else:
   print "No match!!"

"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

seconds = 10	#Start counting down from 10

class myMessageBox(QMessageBox):
    
    @pyqtSlot()    
    def timeoutSlot(self):    
    
	#This is to avoid UnboundLocalError
	global seconds
	
	#Decrease seconds here
	seconds -= 1
	
	#Update QMessageBox text here
	#QMessageBox.setText(self,"QMessageBox will close after "+QString.number(seconds)+" seconds")
	
	 #If reached 0,close the messagebox	
	if seconds==0:
	  QMessageBox.close(self)
   
def main(msg_id,msg):    

    app 	 = QApplication(sys.argv)
    messageBox	 = myMessageBox(0,"Auto-Close QMessagebox","QMessageBox will close after 10 seconds")
    timer	 = QTimer()
    
    
    
    _fromUtf8 = QString.fromUtf8
			    
    _encoding = QApplication.UnicodeUTF8   
    def _translate(context, text, disambig):
	return QApplication.translate(context, text, disambig, _encoding)        
    
    icon = QIcon()
						
    icon.addPixmap(QPixmap(_fromUtf8("XCC.ico")), QIcon.Normal, QIcon.Off)           
			    
    messageBox = myMessageBox()
    messageBox.setWindowIcon(QIcon(icon))
				   
    messageBox.setWindowTitle(_translate("Dialog", "XCC Automated Settings", None))
    messageBox.setText("Not supported File<br>"+msg)
    #msgBox.setInformativeText("Do you want to save your changes?")
    messageBox.setStandardButtons(QMessageBox.Ok)
    messageBox.setDefaultButton(QMessageBox.Ok)    
        
    messageBox.connect(timer,SIGNAL("timeout()"),
		       messageBox,SLOT("timeoutSlot()"))

    timer.start(1000)
    messageBox.show() 
    app.exec_()
    #sys.exit(app.exec_())

if __name__ == '__main__':
    n=0
    while n <=10:
	seconds = 1
	n+=1
	main(1,'1')
	