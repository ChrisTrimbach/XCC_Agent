import urllib2
import requests
import simplejson as json
import subprocess
import time
import ctypes
import socket
import struct
import sys,os
import Agent_Config

workflow_id=sys.argv[1]
#workflow_id=11740
Config_array=Agent_Config.Configfile()
from Agent_log import write_log
proxy=Config_array[0]
proxysetting=(Config_array[1],Config_array[2])
PORT=int(Config_array[3])

write_log('XCC Workflow Service: Start for workflow id %s'% workflow_id)
write_log('XCC Workflow Service: XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
def get_macaddress(host,workflow_id,PORT):
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
        raise WindowsError('Retrieval of mac address(%s) - failed' % host)
    
    # Convert binary data into a string.
    macaddr = ''
    for intval in struct.unpack('BBBBBB', buffer):
        if intval > 15:
            replacestr = '0x'
        else:
            replacestr = 'x'
        macaddr = '-'.join([macaddr, hex(intval).replace(replacestr, '')])
    
    
    
    macaddr=macaddr.split("-",7)
    
    
    
    return macaddr[1]+':'+macaddr[2]+':'+macaddr[3]+':'+macaddr[4]+':'+macaddr[5]+':'+macaddr[6],hostip,workflow_id,PORT

#if __name__ == '__main__':
#print 'Your mac address is %s %s %s %s' % get_macaddress('localhost',workflow_id,PORT)



if(proxy =="True"):
    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
else:
    proxy_handeler = urllib2.ProxyHandler({})
opener_proxy = urllib2.build_opener(proxy_handeler)
get_workflow_settings= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_settings.php?%s_%s_%s_%s" % get_macaddress('localhost',workflow_id,PORT))
        
read_workflow_settings = opener_proxy.open(get_workflow_settings)
workflow_settings = json.load(read_workflow_settings)
write_log('XCC Workflow Service: Get workflow settings of workflow %s'% workflow_id)



def check_workflow_status(workflow_id):
    
    run = 0
    while (run < 1):
        if(proxy =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)	
        get_workflow_status= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_status.php?%s" % workflow_id)
                       
        read_workflow_status = opener_proxy.open(get_workflow_status)
        workflow_status = json.load(read_workflow_status)         
	print 'XCC Workflow Service: Status Check %s, Workflow id %s'%(workflow_status['status'],workflow_id)
	write_log('XCC Workflow Service: Status Check %s, Workflow id %s'%(workflow_status['status'],workflow_id))	
        if workflow_status['status'] == '10':
            run = run +1
            write_log('XCC Workflow Service: End task workflow id %s'% workflow_id)
        else:
            if workflow_status['status'] == '0':
                res = subprocess.call(['ping', '-n', '1','-w','750', workflow_settings['Printer_ip']],stdout = subprocess.PIPE)
                print res
                if res == 0:                    
		    print "XCC Workflow Service: Ping Ok, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
		    write_log('XCC Workflow Service: Ping Ok, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))
		    
                    run_job(workflow_id)
                else:
		    print "XCC Workflow Service: Ping No communication, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
		    write_log('XCC Workflow Service: Ping No communication, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))                    
                    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_ping_error.php?_et=5&w_id=%s" % workflow_id)                    
                    response = opener_proxy.open(req).read().strip()
                    print "XCC Workflow Service: Response %s"%response
                                                         
                    
		    wait_ping_error = 0
		    print "XCC Workflow Service: Start waiting process, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
		    write_log('XCC Workflow Service: Start waiting process, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))        		    
		    while (wait_ping_error < 288):
			time.sleep(300)
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_ping_error.php?_et=5&w_id=%s" % workflow_id)                    
			response = opener_proxy.open(req).read().strip()
			print "XCC Workflow Service: Response %s"%response			
			res_first = subprocess.call(['ping', '-n', '1','-w','750', workflow_settings['Printer_ip']],stdout = subprocess.PIPE)
			if res_first == 0:
			    print "XCC Workflow Service: After 5 min ping ok response wait 30 min to let the device start up, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
			    write_log('XCC Workflow Service: After 5 min ping ok response wait 30 min to let the device start up, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))			    
			    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_ping_error.php?_et=30&w_id=%s" % workflow_id)                    
			    response = opener_proxy.open(req).read().strip()
			    print "XCC Workflow Service: Response %s"%response			    
			    time.sleep(1800)
			    res_second = subprocess.call(['ping', '-n', '1','-w','750', workflow_settings['Printer_ip']],stdout = subprocess.PIPE)
			    if res_second == 0:
				print "XCC Workflow Service: After 30 min ping ok response send job to device, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
				write_log('XCC Workflow Service: After 30 min ping ok response send job to device, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))			   				
				break
			    else:
				print "XCC Workflow Service: After 30 min no ping response try again, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
				write_log('XCC Workflow Service: After 30 min no ping response try again, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))				
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_ping_error.php?_et=5&w_id=%s" % workflow_id)                    
				response = opener_proxy.open(req).read().strip()
				print "XCC Workflow Service: Response %s"%response				
				wait_ping_error += 1
			else:
			    wait_ping_error += 1
			    print "XCC Workflow Service: After 5 min no ping response try again, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
			    write_log('XCC Workflow Service: After 5 min no ping response try again, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))			    
		    else:
			print "XCC Workflow Service: End waiting process, Workflow id %s(%s)"% (workflow_id,workflow_settings['Printer_ip'])
			write_log('XCC Workflow Service: End waiting process, Workflow id %s(%s)'% (workflow_id,workflow_settings['Printer_ip']))
            else:
		print 'XCC Workflow Service: Wait for next Status Check, Workflow id %s'% workflow_id
		write_log('XCC Workflow Service: Wait for next Status Check, Workflow id %s'% workflow_id)
                
                time.sleep(15)
                              
                              
                
        
        





def run_job(workflow_id):
    print 'XCC Workflow Service: Start task workflow id %s'% workflow_id
    write_log('XCC Workflow Service: Start task workflow id %s'% workflow_id)    
    if(proxy =="True"):
	proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
    else:
	proxy_handeler = urllib2.ProxyHandler({})
    opener_proxy = urllib2.build_opener(proxy_handeler)    
    get_job_data= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/KnownDevice.php?%s" % workflow_id,data="")
    
    print 'XCC Workflow Service: Get task workflow id %s'% workflow_id
    write_log('XCC Workflow Service: Get task workflow id %s'% workflow_id) 
    try:
	data=opener_proxy.open(get_job_data, timeout=60).read()
	data_array=data.split(" ",3)
    except urllib2.URLError as e:    
	print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
	write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
	time.sleep(5)
	print "XCC Workflow Service: Try again start get task from XCC"
	write_log('XCC Workflow Service: Try again start get task from XCC')  
	try:
	    data=opener_proxy.open(get_job_data, timeout=60).read()
	    data_array=data.split(" ",3)
	except urllib2.URLError as e:    
	    print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
	    write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
	    time.sleep(5)
	    print "XCC Workflow Service: Try again start get task from XCC"
	    write_log('XCC Workflow Service: Try again start get task from XCC')    
	    try:
		data=opener_proxy.open(get_job_data, timeout=60).read()
		data_array=data.split(" ",3)
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error'] 
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when get task from XCC"
		write_log('XCC Workflow Service: Timeout error when get task from XCC')		
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error']	    
	except socket.timeout:
	    print "XCC Workflow Service: Timeout error when get task from XCC"
	    write_log('XCC Workflow Service: Timeout error when get task from XCC')
	    time.sleep(5)
	    print "XCC Workflow Service: Try again start get task to XCC"
	    write_log('XCC Workflow Service: Try again start get task from XCC')   
	    try:
		data=opener_proxy.open(get_job_data, timeout=60).read()
		data_array=data.split(" ",3)
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error'] 
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when get task from XCC"
		write_log('XCC Workflow Service: Timeout error when get task from XCC')		
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error']	
    except socket.timeout:
	print "XCC Workflow Service: Timeout error when get task from XCC"
	write_log('XCC Workflow Service: Timeout error when get task from XCC')
	time.sleep(5)
	print "XCC Workflow Service: Try again start get task to XCC"
	write_log('XCC Workflow Service: Try again start get task from XCC')   
	try:
	    data=opener_proxy.open(get_job_data, timeout=60).read()
	    data_array=data.split(" ",3)
	except urllib2.URLError as e:    
	    print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
	    write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
	    time.sleep(5)
	    print "XCC Workflow Service: Try again start get task from XCC"
	    write_log('XCC Workflow Service: Try again start get task from XCC')    
	    try:
		data=opener_proxy.open(get_job_data, timeout=60).read()
		data_array=data.split(" ",3)
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error'] 
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when get task from XCC"
		write_log('XCC Workflow Service: Timeout error when get task from XCC')		
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error']	    
	except socket.timeout:
	    print "XCC Workflow Service: Timeout error when get task from XCC"
	    write_log('XCC Workflow Service: Timeout error when get task from XCC')
	    time.sleep(5)
	    print "XCC Workflow Service: Try again start get task to XCC"
	    write_log('XCC Workflow Service: Try again start get task from XCC')   
	    try:
		data=opener_proxy.open(get_job_data, timeout=60).read()
		data_array=data.split(" ",3)
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when get task from XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when get task from XCC (%s) ' % e.reason)
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error'] 
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when get task from XCC"
		write_log('XCC Workflow Service: Timeout error when get task from XCC')		
		print "XCC Workflow Service: Stop get task to XCC"
		write_log('XCC Workflow Service: Stop get task from XCC')
		data_array = ['error']
    
    data_array=data.split(" ",3)
    print "XCC Workflow Service: Type of Job %s"%data_array[0]
    print 'XCC Workflow Service: Retrieved next task workflow id %s task %s'% (workflow_id,data_array[1])
    write_log('XCC Workflow Service: Retrieved next task workflow id %s task %s'% (workflow_id,data_array[1]))   
    if(data_array[0] == 'JDF'):
        #print 'XCC Workflow Service: Task '+data_array[1]
        print "XCC Workflow Service: JDF"
        try:
            import base64
            #print data_array[2]
            res = requests.post(url='http://%s:%s'% (workflow_settings['Printer_ip'],workflow_settings['JMF_port']),
                                data=base64.b64decode(data_array[2]),
                                headers={'MIME-Version': '1.0','content-description': 'XCC JDF MIME Package','Content-Type': 'multipart/related'})
            #print res.text
            write_log('XCC Workflow Service: Send JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
            get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
	    read_Post_URL = opener_proxy.open(get_Post_URL)
	    Post_URL = json.load(read_Post_URL)
	    print Post_URL['Post_URL']	    
            import MultipartPostHandler
            #print res.text.encode('utf-8')
            params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
            opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
            urllib2.install_opener(opener)
            req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % workflow_id, params)
            if(proxy =="True"):
                req.set_proxy('%s:%s'% proxysetting, 'http')
            print "XCC Workflow Service: Start JDF result to XCC"
	    write_log('XCC Workflow Service: Start JDF result to XCC')	    
	    try:
		response = opener.open(req, timeout=30).read().strip()
		print "XCC Workflow Service: Response %s"%response
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		time.sleep(5)
		print "XCC Workflow Service: Try again start forward JDF result to XCC"
		write_log('XCC Workflow Service: Try again start forward JDF result to XCC')
		try:
		    response = opener.open(req, timeout=30).read().strip()
		    print "XCC Workflow Service: Response %s"%response
		except urllib2.URLError as e:    
		    print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward JDF result to XCC"
		    write_log('XCC Workflow Service: Try again start forward JDF result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		    
		except socket.timeout:
		    print "XCC Workflow Service: Timeout error when sent to XCC"
		    write_log('XCC Workflow Service: Timeout error when sent to XCC')
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward JDF result to XCC"
		    write_log('XCC Workflow Service: Try again start forward JDF result to XCC') 		
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when sent to XCC"
		write_log('XCC Workflow Service: Timeout error when sent to XCC')
		time.sleep(5)
		print "XCC Workflow Service: Try again start forward JDF result to XCC"
		write_log('XCC Workflow Service: Try again start forward JDF result to XCC')   
		try:
		    response = opener.open(req, timeout=30).read().strip()
		    print "XCC Workflow Service: Response %s"%response
		except urllib2.URLError as e:    
		    print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward JDF result to XCC"
		    write_log('XCC Workflow Service: Try again start forward JDF result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		    
		except socket.timeout:
		    print "XCC Workflow Service: Timeout error when sent to XCC"
		    write_log('XCC Workflow Service: Timeout error when sent to XCC')
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward JDF result to XCC"
		    write_log('XCC Workflow Service: Try again start forward JDF result to XCC') 		
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
            write_log('XCC Workflow Service: Completed JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
            write_log('XCC Workflow Service: Forward response JDF task %s to DFE %s of workflow id %s to XCC'% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
        except:
            print 'XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error JDF task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=JDF&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response
    elif(data_array[0] == 'DXML'):
        #print 'XCC Workflow Service: Task '+data_array[1]
        print "XCC Workflow Service: DXML"           
        try:
            import base64
            #print data_array[2]
            res = requests.post(url='http://%s:%s'% (workflow_settings['Printer_ip'],workflow_settings['JMF_port']),
                                data=base64.b64decode(data_array[2]),
                                headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
            #print res.text
            write_log('XCC Workflow Service: Send Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
	    get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
	    read_Post_URL = opener_proxy.open(get_Post_URL)
	    Post_URL = json.load(read_Post_URL)
	    print Post_URL['Post_URL']	    
            import MultipartPostHandler
            #print res.text.encode('utf-8')
            params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
            opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
            urllib2.install_opener(opener)
            req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % workflow_id, params)
            if(proxy =="True"):
                req.set_proxy('%s:%s'% proxysetting, 'http')
            print "XCC Workflow Service: Start Direct XML result to XCC"
	    write_log('XCC Workflow Service: Start Direct XML result to XCC')	    
	    try:
		response = opener.open(req, timeout=30).read().strip()
		print "XCC Workflow Service: Response %s"%response
	    except urllib2.URLError as e:    
		print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		time.sleep(5)
		print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC')
		try:
		    response = opener.open(req, timeout=30).read().strip()
		    print "XCC Workflow Service: Response %s"%response
		except urllib2.URLError as e:    
		    print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		    write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		    
		except socket.timeout:
		    print "XCC Workflow Service: Timeout error when sent to XCC"
		    write_log('XCC Workflow Service: Timeout error when sent to XCC')
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		    write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC') 		
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		
	    except socket.timeout:
		print "XCC Workflow Service: Timeout error when sent to XCC"
		write_log('XCC Workflow Service: Timeout error when sent to XCC')
		time.sleep(5)
		print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC')   
		try:
		    response = opener.open(req, timeout=30).read().strip()
		    print "XCC Workflow Service: Response %s"%response
		except urllib2.URLError as e:    
		    print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		    write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response		    
		except socket.timeout:
		    print "XCC Workflow Service: Timeout error when sent to XCC"
		    write_log('XCC Workflow Service: Timeout error when sent to XCC')
		    time.sleep(5)
		    print "XCC Workflow Service: Try again start forward Direct XML result to XCC"
		    write_log('XCC Workflow Service: Try again start forward Direct XML result to XCC') 		
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except urllib2.URLError as e:    
			print "XCC Workflow Service: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Workflow Service: Error when sent to XCC (%s) ' % e.reason)										    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
		    except socket.timeout:
			print "XCC Workflow Service: Timeout error when sent to XCC"
			write_log('XCC Workflow Service: Timeout error when sent to XCC')							    
			print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
			write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Direct XML&w_id=%s" % workflow_id)		    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Workflow Service: Response %s"%response
            write_log('XCC Workflow Service: Completed Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
            write_log('XCC Workflow Service: Forward response Direct XML task %s to DFE %s of workflow id %s to XCC'% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
                        
        except:
            print 'XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error Direct XML task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=DXML&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response     
    elif(data_array[0] == 'FTP'):
        import ftplib
        import base64
        print "XCC Workflow Service: FTP"        
        get_job_settings= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_job_settings.php?%s-%s-%s" % (workflow_id,data_array[0],data_array[1]))
                                                
	
        read_job_settings = opener_proxy.open(get_job_settings)
        job_settings = json.load(read_job_settings)   
                
                
        try:
            
            output = open("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),"wb")
                        
            output.write(base64.b64decode(data_array[2]))
            output.close()
            write_log('XCC Workflow Service: Send FTP task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
                
            ftp = ftplib.FTP()
            #print workflow_settings['FTP_port']
            ftp.connect(host="%s" % workflow_settings['Printer_ip'],port=int(workflow_settings['FTP_port']))
            ftp.login("%s"% (job_settings['User']),"%s" %(job_settings['Password']))# Connect
            fp = open("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),'rb') # file to send
            ftp.cwd("%s" % job_settings['Folder'])
            ftp.storbinary('STOR %s'% job_settings['Filename'], fp) # Send the file
                     
            fp.close() # Close file and FTP
            ftp.quit()  
            os.remove("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']))
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_completed.php?con=FTP&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response 
            write_log('XCC Workflow Service: Completed FTP task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
        except:
            print 'XCC Workflow Service: Error FTP task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error FTP task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
            
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=FTP&w_id=%s" % workflow_id)
           
            response = opener_proxy.open(req).read().strip()
            print response                         
                        
    elif(data_array[0] == 'SHARE'):
        print "XCC Workflow Service: Share"
                
        import shutil
        import base64
        get_job_settings= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_job_settings.php?%s-%s-%s" % (workflow_id,data_array[0],data_array[1]))
        
        read_job_settings = opener_proxy.open(get_job_settings)
        job_settings = json.load(read_job_settings)    
                                
        try:
            output = open("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),"wb")
            output.write(base64.b64decode(data_array[2]))
            output.close()
            write_log('XCC Workflow Service: Send Share task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
            shutil.copy2("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),'//%s/%s/%s'%(workflow_settings['Printer_ip'],job_settings['Folder'],job_settings['Filename']))
            os.remove("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']))
            #time.sleep(10)
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_completed.php?con=SHARE&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response
            write_log('XCC Workflow Service: Completed Share task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
        except:
            print 'XCC Workflow Service: Error Share task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error Share task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
            
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=SHARE&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response                         
    elif(data_array[0] == 'COLORPORT'):
        print "XCC Workflow Service: COLORPORT"
                        
        import shutil
        import base64
        get_job_settings= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_job_settings.php?%s-%s-%s" % (workflow_id,data_array[0],data_array[1]))
        
        read_job_settings = opener_proxy.open(get_job_settings)
        job_settings = json.load(read_job_settings)    
                                        
        try:
            output = open("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),"wb")
            output.write(base64.b64decode(data_array[2]))
            output.close()
            write_log('XCC Workflow Service: Send ColorPort task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
                    
            shutil.copy2("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),'%s/%s/%s'%(Agent_Config.APP_MYDOC_PATH,job_settings['Folder'],job_settings['Filename']))
            os.remove("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']))
            #time.sleep(10) 
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_completed.php?con=COLORPORT&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response 
            write_log('XCC Workflow Service: Completed ColorPort task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
        except:
            print 'XCC Workflow Service: Error ColorPort task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error ColorPort task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
                    
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=COLORPORT&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response    
    elif(data_array[0] == 'I1PROFILER'):
        print "XCC Workflow Service: I1PROFILER"
                                
        import shutil
        import base64
        get_job_settings= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/workflow_job_settings.php?%s-%s-%s" % (workflow_id,data_array[0],data_array[1]))
        
        read_job_settings = opener_proxy.open(get_job_settings)
        job_settings = json.load(read_job_settings)        
                                                
        try:
            output = open("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),"wb")
            output.write(base64.b64decode(data_array[2]))
            output.close()
            write_log('XCC Workflow Service: Send I1Profiler task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
                            
            shutil.copy2("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']),'%s/%s/%s'%(Agent_Config.App_PROGRAMDATA,job_settings['Folder'],job_settings['Filename']))
            os.remove("%s/%s" % (Agent_Config.APP_TEMP_PATH,job_settings['Filename_temp']))
            #time.sleep(10)
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_completed.php?con=I1PROFILER&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response
            write_log('XCC Workflow Service: Completed I1Profiler task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))           
            
        except:
            print 'XCC Workflow Service: Error I1Profiler task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
            write_log('XCC Workflow Service: Error I1Profiler task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
                            
            req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=I1PROFILER&w_id=%s" % workflow_id)
            
            response = opener_proxy.open(req).read().strip()
            print "XCC Workflow Service: Response %s"%response    
    else:
        print 'XCC Workflow Service: Error Unknown task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id)
        write_log('XCC Workflow Service: Error Unknown task %s to DFE %s of workflow id %s '% (data_array[1],workflow_settings['Printer_ip'],workflow_id))                       
        
        req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=undefined+job+type&w_id=%s" % workflow_id)
        
        response = opener_proxy.open(req).read().strip()
        print "XCC Workflow Service: Response %s"%response                 
 
        
check_workflow_status(workflow_id)

        



