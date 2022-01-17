import urllib2
import requests
import simplejson as json
import subprocess
import ctypes
import socket
#import struct
import time
import Agent_Config
import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import QTimer,QString,pyqtSlot,Qt,SIGNAL,SLOT
from Agent_log import write_log
from struct import unpack, pack
import random

 

def get_macaddress(host,email="None",password="None"):
    """ Returns the MAC address of a network host, requires >= WIN2K. """
    
    # Check for api availability
    try:
        SendARP = ctypes.windll.Iphlpapi.SendARP
    except:
        raise NotImplementedError('Use only Windows 2000 and above')
        
    # Doesn't work with loopbacks, but let's try and help.
    if host == '127.0.0.1' or host.lower() == 'localhost':
        host = socket.gethostname()
    
    # gethostbyname blocks, so use it wisely.
    try:
        inetaddr = ctypes.windll.wsock32.inet_addr(host)
        if inetaddr in (0, -1):
            raise Exception
    except:
        hostip = socket.gethostbyname(host)
        inetaddr = ctypes.windll.wsock32.inet_addr(hostip)
    
    buffer = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(buffer))
    if SendARP(inetaddr, 0, ctypes.byref(buffer), ctypes.byref(addlen)) != 0:
        raise WindowsError('Retreival of mac address(%s) - failed' % host)
    
    # Convert binary data into a string.
    macaddr = ''
    for intval in unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr = '-'.join([macaddr, hex(intval).replace(replacestr, '')])
    
   
    
    
    macaddr=macaddr.split("-",7)
    
    
    
    return email,password,macaddr[1]+':'+macaddr[2]+':'+macaddr[3]+':'+macaddr[4]+':'+macaddr[5]+':'+macaddr[6],hostip


    



from multiprocessing import Process
import os

def nearline_alife_check(Nearline_ip):    
    res = subprocess.call(['ping', '-n', '1','-w','750', Nearline_ip],stdout = subprocess.PIPE)             
    if res == 0:
        print "XCC Nearline Spectro: Ping Nearline Spectro %s OK"% Nearline_ip 
        write_log('XCC Nearline Spectro: Ping Nearline Spectro %s OK'% Nearline_ip) 
        return 1
    else:                
        print "XCC Nearline Spectro: Ping Nearline Spectro %s no communication"% Nearline_ip
        write_log('XCC Nearline Spectro: Ping Nearline Spectro %s no communication'% Nearline_ip)
        return 2
        
            
def connect_to_nearline_spectro(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode=1):
    Config_array=Agent_Config.Configfile()                    
    proxy=Config_array[0]
    proxysetting=(Config_array[1],Config_array[2])        
    try:
        write_log('XCC Nearline Spectro: Created Socket %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,5)
        try:
            write_log('XCC Nearline Spectro: Set Socket Options %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,2)
            # connect to the server on local computer
            try: 
                write_log('XCC Nearline Spectro: Connect %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                sock.connect((Nearline_ip, Nearline_port))  
                
                VID='CM'
                VID_size = len(VID)
                CID = Job_id
                CID_size = len(CID)
                #Job_Measure_Mode=0 #all
                #Job_Measure_Mode=1 #M0
                #Job_Measure_Mode=2 #M1
                #Job_Measure_Mode=3 #M2
                CheckChartAvailable_format_string = '<i%dsi%ds' % (VID_size, CID_size)  
                CheckChartAvailable_payload= pack (CheckChartAvailable_format_string,VID_size,VID,CID_size,CID)
                
                CheckChartAvailable_trans_id=random.randrange(1, 65535)
                CheckChartAvailable_flags=128
                CheckChartAvailable_reserved=0
                CheckChartAvailable_status=256
                
                CheckChartAvailable_packet_size=pack('<iHBBI',0,CheckChartAvailable_trans_id, CheckChartAvailable_flags, CheckChartAvailable_reserved, CheckChartAvailable_status)                
                CheckChartAvailable_p_size = len (CheckChartAvailable_packet_size) + len(CheckChartAvailable_payload)
                
                
                CheckChartAvailable_request=pack('<iHBBI',CheckChartAvailable_p_size,CheckChartAvailable_trans_id, CheckChartAvailable_flags, CheckChartAvailable_reserved, CheckChartAvailable_status)                
                try:
                    write_log('XCC Nearline Spectro: Send CheckChartAvailable to Spectro %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                    sock.send(CheckChartAvailable_request)
                
                    time.sleep(1)
                
                    sock.send(CheckChartAvailable_payload)
                    time.sleep(1)
                
                    CheckChartAvailable_recv_size=len(pack('<iHBBII',0,0,0,0,0,0))
                
                    CheckChartAvailable_recv_data = sock.recv(CheckChartAvailable_recv_size)
                
                
                    CheckChartAvailable_recv_pyload_size, CheckChartAvailable_recv_trans_id, CheckChartAvailable_recv_flags, CheckChartAvailable_recv_reserved,CheckChartAvailable_recv_command, CheckChartAvailable_recv_status   = unpack ('<IHBBII', CheckChartAvailable_recv_data) 
                
                    if CheckChartAvailable_recv_status == 0:
                        write_log('XCC Nearline Spectro: Check Chart Available Receive Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                        CheckChartAvailable_recv_pyload_size -= len(CheckChartAvailable_recv_data)
                        CheckChartAvailable_total_recv_data=""
                        CheckChartAvailable_recv_data =None                        
                        while CheckChartAvailable_recv_data != "":                         
                            CheckChartAvailable_recv_data = sock.recv(CheckChartAvailable_recv_pyload_size)
                            CheckChartAvailable_recv_pyload_size -= len(CheckChartAvailable_recv_data)
                            CheckChartAvailable_total_recv_data +=CheckChartAvailable_recv_data
                            time.sleep(1)
                    
                        CheckChartAvailable_recv2_pyload_size1, CheckChartAvailable_recv2_trans_id, CheckChartAvailable_recv2_flags, CheckChartAvailable_recv2_status  = unpack ('<i22sQI', CheckChartAvailable_total_recv_data[:38]) 
                    
                    
                        if CheckChartAvailable_recv2_status==0:
                            write_log('XCC Nearline Spectro: Chart is Available %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                            sock.close()
                            try: 
                                write_log('XCC Nearline Spectro: Created Socket For Receiving Spectral Data  %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
                                sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,5)
                                try:
                                    write_log('XCC Nearline Spectro: Set Socket Options For Receiving Spectral Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                    sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,2)
                                    # connect to the server on local computer
                                    try: 
                                        write_log('XCC Nearline Spectro: Connect For Receiving Spectral Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                        sock.connect((Nearline_ip, Nearline_port))                        
                                        GetChartData_format_string = '<i%dsi%dsBB' % (VID_size, CID_size)  
                                        GetChartData_payload= pack (GetChartData_format_string,VID_size,VID,CID_size,CID,0,Job_Measure_Mode) 
                        
                                        GetChartData_trans_id=random.randrange(1, 65535)
                                        GetChartData_flags=128
                                        GetChartData_reserved=0
                                        GetChartData_status=257
                        
                                        GetChartData_packet_size=pack('<iHBBI',0,GetChartData_trans_id, GetChartData_flags, GetChartData_reserved, GetChartData_status)                        
                                        GetChartData_packet_p_size = len (GetChartData_packet_size) + len(GetChartData_payload)
                        
                        
                                        GetChartData_request=pack('<iHBBI',GetChartData_packet_p_size,GetChartData_trans_id, GetChartData_flags, GetChartData_reserved, GetChartData_status)                        
                                        write_log('XCC Nearline Spectro: Send Get Chart Spectral Data to Spectro %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))                        
                                        sock.send(GetChartData_request)                        
                                        time.sleep(1)
                        
                                        sock.send(GetChartData_payload)
                                        time.sleep(1)
                        
                                        GetChartData_recv_size=len(pack('<iHBBII',0,0,0,0,0,0))
                        
                                        GetChartData_recv_data = sock.recv(GetChartData_recv_size)
                        
                        
                                        GetChartData_recv_pyload_size, GetChartData_recv_trans_id, GetChartData_recv_flags, GetChartData_recv_reserved,GetChartData_recv_command, GetChartData_recv_status   = unpack ('<IHBBII', GetChartData_recv_data) 
                                        if GetChartData_recv_status==0:
                                            write_log('XCC Nearline Spectro: Check Get Chart Spectral Data Receive Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                            
                            
                                            GetChartData_recv_pyload_size -= len(GetChartData_recv_data)
                                            GetChartData_total_recv_data=""
                                            GetChartData_recv_data =None
                            
                                            while GetChartData_recv_data != "":
                                                GetChartData_recv_data = sock.recv(GetChartData_recv_pyload_size)
                                                GetChartData_recv_pyload_size -= len(GetChartData_recv_data)
                                                GetChartData_total_recv_data +=GetChartData_recv_data
                                                time.sleep(1)
                            
                            
                            
                                            if len(GetChartData_total_recv_data)!=0:
                                                write_log('XCC Nearline Spectro: Get All Chart Spectral Data Receive Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                                GetChartData_find_job_id,GetChartData_job_id = unpack ('<i22s', GetChartData_total_recv_data[:26])
                                
                                                import urllib2
						if(proxy =="True"):
						    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
						else:
						    proxy_handeler = urllib2.ProxyHandler({})
						opener_proxy = urllib2.build_opener(proxy_handeler)						
						get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")
										
						read_Post_URL = opener_proxy.open(get_Post_URL)
						Post_URL = json.load(read_Post_URL)
						print "XCC Nearline Spectro: Post URL %s"%Post_URL['Post_URL']						
                                                import base64
                                                import MultipartPostHandler
                                                write_log('XCC Nearline Spectro: Send Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                            
                                                params = {'file_data':base64.b64encode(GetChartData_total_recv_data)}
                                                opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
                                                urllib2.install_opener(opener)
                                                req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_network_spectro.php?Job_id=%s" % GetChartData_job_id, params)
                                                if(proxy =="True"):
                                                    req.set_proxy('%s:%s'% proxysetting, 'http')                                
						global seconds
						seconds = 10						    
						try:
						    response = opener.open(req, timeout=45).read().strip()
						    print "XCC Nearline Spectro: %s"%response
						    write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
						    Result_upload = json.loads(response)						    
						    Show_msg(Result_upload['Result_msg'])
						    return 2
						except urllib2.URLError as e:    
						    print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
						    write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
						    time.sleep(5)
						    try:
							response = opener.open(req, timeout=45).read().strip()
							print "XCC Nearline Spectro: %s"%response
							write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							Result_upload = json.loads(response)									
							Show_msg(Result_upload['Result_msg'])
							return 2
						    except urllib2.URLError as e:    
							print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							time.sleep(5)
							try:
							    response = opener.open(req, timeout=45).read().strip()
							    print "XCC Nearline Spectro: %s"%response
							    write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    Result_upload = json.loads(response)							    
							    Show_msg(Result_upload['Result_msg'])
							    return 2
							except urllib2.URLError as e:    
							    print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							    write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1    
							except socket.timeout:
							    print "XCC Nearline Spectro: Timeout error when sent to XCC"
							    write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1							
						    except socket.timeout:
							print "XCC Nearline Spectro: Timeout error when sent to XCC"
							write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							time.sleep(5)
							try:
							    response = opener.open(req, timeout=45).read().strip()
							    print "XCC Nearline Spectro: %s"%response
							    write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    Result_upload = json.loads(response)							   
							    Show_msg(Result_upload['Result_msg'])
							    return 2
							except urllib2.URLError as e:    
							    print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							    write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1    
							except socket.timeout:
							    print "XCC Nearline Spectro: Timeout error when sent to XCC"
							    write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1						    
						except socket.timeout:
						    print "XCC Nearline Spectro: Timeout error when sent to XCC"
						    write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
						    time.sleep(5)
						    try:
							response = opener.open(req, timeout=45).read().strip()
							print "XCC Nearline Spectro: %s"%response
							write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							Result_upload = json.loads(response)									
							Show_msg(Result_upload['Result_msg'])
							return 2
						    except urllib2.URLError as e:    
							print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							time.sleep(5)
							try:
							    response = opener.open(req, timeout=45).read().strip()
							    print "XCC Nearline Spectro: %s"%response
							    write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    Result_upload = json.loads(response)							    
							    Show_msg(Result_upload['Result_msg'])
							    return 2
							except urllib2.URLError as e:    
							    print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							    write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1    
							except socket.timeout:
							    print "XCC Nearline Spectro: Timeout error when sent to XCC"
							    write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1							
						    except socket.timeout:
							print "XCC Nearline Spectro: Timeout error when sent to XCC"
							write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							time.sleep(5)
							try:
							    response = opener.open(req, timeout=45).read().strip()
							    print "XCC Nearline Spectro: %s"%response
							    write_log('XCC Nearline Spectro: Sended Spectral Data to Cloud %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    Result_upload = json.loads(response)							    
							    Show_msg(Result_upload['Result_msg'])
							    return 2
							except urllib2.URLError as e:    
							    print "XCC Nearline Spectro: Error when sent to XCC (%s) " % e.reason
							    write_log('XCC Nearline Spectro: Error when sent to XCC (%s) ' % e.reason)
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1    
							except socket.timeout:
							    print "XCC Nearline Spectro: Timeout error when sent to XCC"
							    write_log('XCC Nearline Spectro: Timeout error when sent to XCC')
							    write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
							    sock.close()
							    return 1                                                
                                            else:
                                                write_log('XCC Nearline Spectro: Error Get All Chart Spectral Data Receive Not Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                                sock.close()
                                                return 1                            
                                        else:
                                            sock.close()
                                            write_log('XCC Nearline Spectro: Check Get Chart Spectral Data Receive NOT Correct Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                            return 1
                                    except:
                                        write_log('XCC Nearline Spectro: Error Connect For Receiving Spectral Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                        return 1              
                                except:
                                    write_log('XCC Nearline Spectro: Error Set Socket Options For Receiving Spectral Data %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                    return 1        
                            except:
                                write_log('XCC Nearline Spectro: Error Created Socket For Receiving Spectral Data  %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                                return 1          
                            
                            
                            
                                                
                            
                        elif CheckChartAvailable_recv_status == 256:
                            write_log('XCC Nearline Spectro: Chart is Not Available %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                            sock.close()
                            # chart has not been measured
                            return 0                        
                        else:
                            write_log('XCC Nearline Spectro: Error Chart is Available But Measure Error %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                            sock.close()
                            return 1                        
                    elif CheckChartAvailable_recv_status == 256:
                        write_log('XCC Nearline Spectro: Chart is Not Available %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                        sock.close()
                        # chart has not been measured
                        return 0                        
                    else:
                        write_log('XCC Nearline Spectro: Error Chart is Available But Measure Error %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                        sock.close()
                        return 1 
                except:
                    
                    write_log('XCC Nearline Spectro: CheckChartAvailable Spectro In Process %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                    sock.close()                    
                    return 1                
                
            except:
                write_log('XCC Nearline Spectro: Error Connect %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
                return 1              
        except:
            write_log('XCC Nearline Spectro: Error Set Socket Options %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
            return 1        
    except:
        write_log('XCC Nearline Spectro: Error Created Socket %s:%s Job id %s Measure Mode %s'%(Nearline_ip,Nearline_port,Job_id,Job_Measure_Mode))
        return 1          
        
                 
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
	       
	    
def Show_msg(msg):
    app 	 = QApplication(sys.argv)
    
	    
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
    messageBox.setText(msg)
    
    messageBox.setStandardButtons(QMessageBox.Ok)
    messageBox.setDefaultButton(QMessageBox.Ok)  
    messageBox.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.WindowMaximizeButtonHint)
	    
    messageBox.connect(timer,SIGNAL("timeout()"),
                       messageBox,SLOT("timeoutSlot()"))
    
    timer.start(1000)
    messageBox.show() 
    app.exec_()      





if __name__ == '__main__':      
    	    
						    
    print "XCC Nearline Spectro: Start XCC Agent Version %s" % Agent_Config.XCC_Agent_Version 
    write_log('XCC Nearline Spectro: Start XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
    run=0
    while (run < 1):  
        Config_array=Agent_Config.Configfile()
                
        proxy=Config_array[0]
        proxysetting=(Config_array[1],Config_array[2])
	print "XCC Nearline Spectro: Check for new task"
        write_log('XCC Nearline Spectro: Check for new task')
        import base64
        if(proxy =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)	
        get_waiting_nearline_project= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_nearline_project.php?%s_%s_%s_%s_B64" % get_macaddress('localhost',email=base64.b64encode(Config_array[4]),password=base64.b64encode(Config_array[5])))
        
        try:   
	    
            read_waiting_nearline_project = opener_proxy.open(get_waiting_nearline_project)
            try:      
                waiting_nearline_project = json.load(read_waiting_nearline_project)        
                print "XCC Nearline Spectro: Json array %s"%waiting_nearline_project 
                print "XCC Nearline Spectro: Amount of Jobs %s"%waiting_nearline_project['Amount']
                if waiting_nearline_project['Amount'] != 0:
                    print "XCC Nearline Spectro: Execute Jobs."
                    for Nearline_jobs in waiting_nearline_project['Nearline_jobs']:
                        for Nearline_spectros in waiting_nearline_project['Nearline_Spectro']:
                            if nearline_alife_check(str(Nearline_spectros['Nearline_spectro_ip'])) == 1:
                                if connect_to_nearline_spectro(str(Nearline_spectros['Nearline_spectro_ip']),int(Nearline_spectros['Nearline_spectro_port']),str(Nearline_jobs['Job_id']),int(Nearline_jobs['Job_Measurement_Mode'])) == 2:
                                    break
                       
                              
                    print "XCC Nearline Spectro: Wait"      
                    time.sleep(int(waiting_nearline_project['Agent_Timer']))                                         
                elif waiting_nearline_project['Stop_Agent'] != '0':
                    print "XCC Nearline Spectro: Force stop."
                    write_log('XCC Nearline Spectro: Force stop')
                    run=1                         
                else:   
                    print 'XCC Nearline Spectro: Agent Timer %s'% int(waiting_nearline_project['Agent_Timer'])
                    time.sleep(int(waiting_nearline_project['Agent_Timer']))
                
            except:
                print "XCC Nearline Spectro: Retrieved corrupt data"
                
                write_log('XCC Nearline Spectro: Retrieved corrupt data')
                time.sleep(30)
        except:
            print "XCC Nearline Spectro: XCC web not visual"
            write_log('XCC Nearline Spectro: XCC web not visual')
            time.sleep(30)
                 



    
    
    
