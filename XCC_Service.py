#from multiprocessing import pool
import urllib2
import requests
import simplejson as json
import subprocess
import ctypes
import socket
import struct
import time
from wmi import WMI
import Agent_Config
from Agent_log import write_log,sent_log_to_XCC


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
    for intval in struct.unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr = '-'.join([macaddr, hex(intval).replace(replacestr, '')])
    
    
    
    macaddr=macaddr.split("-",7)
    
    
    
    return email,password,macaddr[1]+':'+macaddr[2]+':'+macaddr[3]+':'+macaddr[4]+':'+macaddr[5]+':'+macaddr[6],hostip

#if __name__ == '__main__':
#print 'Your mac address is %s %s' % get_macaddress('localhost')
    



from multiprocessing import Process
import os

def alife_check(C_id):
    Config_array=Agent_Config.Configfile()
    
    proxy=Config_array[0]
    proxysetting=(Config_array[1],Config_array[2])    
    print "XCC Service: alife_check %s"%C_id
    if(proxy =="True"):
	proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
    else:
	proxy_handeler = urllib2.ProxyHandler({})
    opener_proxy = urllib2.build_opener(proxy_handeler)    
    walife_all_json= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_alife_check.php?A=C&C_id=%s" % C_id)
    
    
    walife_all_json= opener_proxy.open(walife_all_json)                                   
    walife_all_check = json.load(walife_all_json)
    response = []
    for walife_check in walife_all_check:
        res = subprocess.call(['ping', '-n', '1','-w','750', walife_check['w_ip']],stdout = subprocess.PIPE)             
        if res == 0:
            print 'XCC Service: Ping Ok, Workflow %s(%s)'% (walife_check['w_name'],walife_check['w_ip']) 
            write_log('XCC Service: Ping Ok, Workflow %s(%s)'% (walife_check['w_name'],walife_check['w_ip']))
            pid =  subprocess.Popen(["arp","-a",walife_check['w_ip']], stdout=subprocess.PIPE)
            s = pid.communicate()[0]
            #print s
            try:
                mac=s.split("Type")
                mac=mac[1].split(walife_check['w_ip'])
                mac=mac[1].split(" dy")
                mac=mac[0].split(" sta")
                import re
                mac=re.sub(r" ","",mac[0])                
            except:
                mac="not_found"
                
            print "XCC Service: %s"%mac
	    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	    s.connect((walife_check['w_ip'],80))
	    response_socket_ip=s.getsockname()[0]
	    s.close()
	    print "XCC Service: Response socket ip %s"% response_socket_ip
	    write_log('XCC Service: Response socket ip %s'% response_socket_ip)
	    response.append({'w_id': walife_check['w_id'], 'ping' : 1, 'mac': mac,  'rsip': response_socket_ip})                
	    
            #response.append({'w_id': walife_check['w_id'], 'ping' : 1, 'mac': mac})
        else:                
            print "XCC Service: Ping No communication, Workflow %s(%s)"% (walife_check['w_name'],walife_check['w_ip'])
            write_log('XCC Service: Ping No communication, Workflow %s(%s)'% (walife_check['w_name'],walife_check['w_ip']))
            response.append({'w_id': walife_check['w_id'], 'ping' : 0})
            
    get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")
    
    
    read_Post_URL = opener_proxy.open(get_Post_URL)
    Post_URL = json.load(read_Post_URL)
    print "XCC Service: Post URL %s"%Post_URL['Post_URL']	
    import base64 
    import MultipartPostHandler
    #print res.text.encode('utf-8')
    params = {'user':'foo','Check_data':base64.b64encode(json.dumps(response))}
    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
    urllib2.install_opener(opener)
    req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/workflow_alife_check.php?A=A&C_id=%s" % C_id, params)
    if(proxy =="True"):
        req.set_proxy('%s:%s'% proxysetting, 'http')
    response = urllib2.urlopen(req).read().strip()
    print "XCC Service: Response %s"%response    


def restart_program(program_name,log_name):
    program_pid = 0
    print "XCC Service: Force Restart %s" % log_name
    write_log('XCC Service: Force Restart %s' % log_name )
    task_manager_lines = os.popen("tasklist").readlines()
    for line in task_manager_lines:           
        try:
            if str(line[0:28]) == program_name + (28 - len(program_name) )* ' ':
                program_pid = int(line[29:34])  
                subprocess.Popen("taskkill /F /T /PID %i"%program_pid ,shell=True)
                write_log('XCC Service: Found and Stopped %s' % log_name )
                print "XCC Service: Found and Stopped %s" % log_name
                #break
        except:
            pass    
     
    time.sleep(2)
    try:
        write_log('XCC Service: Force Start %s' % log_name )
        print "XCC Service: Force Start %s" % log_name
        subprocess.Popen("%s"%program_name, shell=True)
    except:
        write_log('XCC Service: Fault to Start %s' % log_name )
        print "XCC Service: Fault to Start %s" % log_name
        
    


if __name__ == '__main__':
    
    PROCNAME_XCC_Agent = "XCC_Agent.exe"  
    PROCNAME_XCC_Agent_service = "XCC_Service.exe"  
    Start_XCC_Agent=0
    Start_XCC_Agent_service=0    
    
    """c = WMI ()
        
    for process in c.Win32_Process ():
        if process.Name ==PROCNAME_XCC_Agent:          
            Start_XCC_Agent+=1  
        if process.Name ==PROCNAME_XCC_Agent_service:          
            Start_XCC_Agent_service+=1
    """
    task_manager_lines = os.popen("tasklist").readlines()
    for line in task_manager_lines:
	if str(line[0:28]) == PROCNAME_XCC_Agent + (28 - len(PROCNAME_XCC_Agent) )* ' ':
	    Start_XCC_Agent+=1  
	if str(line[0:28]) == PROCNAME_XCC_Agent_service + (28 - len(PROCNAME_XCC_Agent_service) )* ' ':
	    Start_XCC_Agent_service+=1	    
    #Start_XCC_Agent+=1                   
    #Start_XCC_Agent_service+=1         
    if(Start_XCC_Agent==1): 
        if(Start_XCC_Agent_service==1):
            
            print "XCC Service: Start XCC Agent Version %s" % Agent_Config.XCC_Agent_Version 
            write_log('XCC Service: Start XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
            run=0
            while (run < 1):  
                Config_array=Agent_Config.Configfile()
                
                proxy=Config_array[0]
                proxysetting=(Config_array[1],Config_array[2]) 
		print "XCC Service: Check for new task"
                write_log('XCC Service: Check for new task')
                import base64
                if(proxy =="True"):
		    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
		else:
		    proxy_handeler = urllib2.ProxyHandler({})
		opener_proxy = urllib2.build_opener(proxy_handeler) 		
                #print "http://"+Agent_Config.Use_URL+".aspcolourmanagement.com/autoflow/workflow_project.php?%s_%s_%s_%s" % get_macaddress('localhost',email=Config_array[4],password=Config_array[5])
                get_waiting_project= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_project.php?%s_%s_%s_%s_B64" % get_macaddress('localhost',email=base64.b64encode(Config_array[4]),password=base64.b64encode(Config_array[5])))
                
                try:
		    read_waiting_project = opener_proxy.open(get_waiting_project)
                    try:      
                        waiting_project = json.load(read_waiting_project)        
                        print "XCC Service: Json Array %s"%waiting_project 
                        print "XCC Service: Amount of Jobs %s"%waiting_project['Amount']
                        if waiting_project['Amount'] != '0':
                            print "XCC Service: Execute Jobs."
                            
                            for workflow in waiting_project['Workflows']:
                                #print workflow
                                write_log('XCC Service: Start XCC Workflow Service for workflow %s (%s)' % (workflow['w_name'],workflow['w_id']) )## Naam workflow
                                subprocess.Popen("XCC_Workflow_Service.exe %s" % workflow['w_id'], shell=True)
                                time.sleep(3)
                          
                            time.sleep(int(waiting_project['Agent_Timer']))
                        elif waiting_project['Run_alife_Check'] != '0':
                            print "XCC Service: Start ping."
                            write_log('XCC Service: Ping to DFE')
                            alife_check(waiting_project['C_id'])
                                                       
                            print "XCC Service: End ping." 
                        elif waiting_project['Agent_log']!= '0':
                            write_log('XCC Service: Forward log data files to XCC support')
                            sent_log_to_XCC(waiting_project['Agent_log_days'],waiting_project['C_id'])
                        elif waiting_project['Stop_Agent'] != '0':
                            print "XCC Service: Force stop."
                            write_log('XCC Service: Force stop')
                            run=1
                        elif waiting_project['Restart_Nearline_Spectro'] != '0':
                            print "XCC Service: Try to Restart Nearline Spectro"
                            write_log('XCC Service: Try to Restart Nearline Spectro')
                            restart_program("XCC_Nearline_Spectro.exe","XCC Nearline Spectro")
                            time.sleep(int(waiting_project['Agent_Timer']))
                        elif waiting_project['Restart_Response_Service'] != '0':
                            print "XCC Service: Try to Restart Response Service"
                            write_log('XCC Service: Try to Restart Response Service')
                            restart_program("XCC_Response_Service.exe","XCC Response Service")
                            time.sleep(int(waiting_project['Agent_Timer']))
                        elif waiting_project['Restart_Hot_Folder'] != '0':
                            print "XCC Service: Try to Restart Hot Folder"
                            write_log('XCC Service: Try to Restart Hot Folder')
                            restart_program("XCC_Hot_Folder.exe","XCC Hot Folder") 
                            time.sleep(int(waiting_project['Agent_Timer']))
                        else:   
                            print 'XCC Service: Wait for next check, Agent Timer sec %s'%waiting_project['Agent_Timer']
			    write_log('XCC Service: Wait for next check, Agent Timer sec %s'%waiting_project['Agent_Timer'])
                            time.sleep(int(waiting_project['Agent_Timer']))
                
                    except:
                        print "XCC Service: Retrieved corrupt data"
                        write_log('XCC Service: Retrieved corrupt data')
                        time.sleep(30)
                except:
                    print "XCC Service: XCC web not visual"
                    write_log('XCC Service: XCC web not visual')
                    time.sleep(30)
        else:
            run=1 
            write_log('XCC Service: Stopped 2nd XCC Service')
    else: 
        run=1
        write_log('XCC Service: Stopped because XCC Agent not started')