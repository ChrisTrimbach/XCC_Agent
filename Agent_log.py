import time
import datetime
import os
import Agent_Config
import base64
import simplejson as json
import socket


def write_log(log_text):
    
    Config_array=Agent_Config.Configfile()
    Log_file_name=datetime.datetime.now().strftime("%Y%m%d")+'.log'
    
    Log_file=os.path.join(Agent_Config.APP_LOG_PATH,Log_file_name)
    if not os.path.isfile(Log_file):                
        last_log=(datetime.date.today() - datetime.timedelta(int(Config_array[7]))).strftime("%Y%m%d")               
        import fnmatch        
        for file in os.listdir(Agent_Config.APP_LOG_PATH):
            if fnmatch.fnmatch(file,'*.log'):                
                if(last_log>=file[:-4]):
                    os.remove(os.path.join(Agent_Config.APP_LOG_PATH,file))   
  
    
    information=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+str(log_text)+'\n'
    f = open(Log_file, 'a')
    f.write(information)
    f.close()
        

def sent_log_to_XCC(Days="1",Company_id="geen"):
    Config_array=Agent_Config.Configfile()
    
    proxy=Config_array[0]
    proxysetting=(Config_array[1],Config_array[2])
    PORT=int(Config_array[3])    
    Log_file_name=datetime.datetime.now().strftime("%Y%m%d")+'.log'
        
    Log_file=os.path.join(Agent_Config.APP_LOG_PATH,Log_file_name)    
    last_log=(datetime.date.today() - datetime.timedelta(int(Days)-1)).strftime("%Y%m%d")               
    import fnmatch     
    for file in os.listdir(Agent_Config.APP_LOG_PATH):
        if fnmatch.fnmatch(file,'*.log'):                
            if(last_log<=file[:-4]):
                print file
                with open("%s/%s" % (Agent_Config.APP_LOG_PATH,file),'rb') as myfile:
                    File_data=myfile.read().replace('\n','<br>').replace('\r','')
                print "XCC Agent Log: Sent data"
                import urllib2
		
		if(proxy =="True"):
		    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
		else:
		    proxy_handeler = urllib2.ProxyHandler({})
		opener_proxy = urllib2.build_opener(proxy_handeler)			    
		get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")														
		read_Post_URL = opener_proxy.open(get_Post_URL)
		Post_URL = json.load(read_Post_URL)
		print "XCC Agent Log: Post URL %s"%Post_URL['Post_URL']	                
                import MultipartPostHandler
                params = {}
                params['file_data'] = base64.b64encode(File_data)
                params['file_name'] = file
                params['Company_id'] = Company_id
                opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
                urllib2.install_opener(opener)
                req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_agent_log.php", params)
                if(proxy =="True"):
                    req.set_proxy('%s:%s'% proxysetting, 'http')
		print 'XCC Agent Log: Start forward result to XCC'
		write_log('XCC Agent Log: Start forward result to XCC')
		try:
		    response = opener.open(req, timeout=30).read().strip()
		    print "XCC Agent Log: Forward result to XCC"
		    write_log('XCC Agent Log: Forward result to XCC')
		    print response
		except urllib2.URLError as e:
		    print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
		    time.sleep(5)
		    print "XCC Agent Log: Try again start forward result to XCC"
		    write_log('XCC Agent Log: Try again start forward result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Agent Log: Forward result to XCC"
			write_log('XCC Agent Log: Forward result to XCC')
			print response
		    except urllib2.URLError as e:
			print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			time.sleep(5)
			print "XCC Agent Log: Try again start forward result to XCC"
			write_log('XCC Agent Log: Try again start forward result to XCC')
			try:
			    response = opener.open(req, timeout=30).read().strip()
			    print "XCC Agent Log: Forward result to XCC"
			    write_log('XCC Agent Log: Forward result to XCC')
			    print response
			except urllib2.URLError as e:
			    print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			    write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			except socket.timeout:
			    print "XCC Agent Log: Timeout error when sent to XCC"
			    write_log('XCC Agent Log: Timeout error when sent to XCC')
		    except socket.timeout:
			print "XCC Agent Log: Timeout error when sent to XCC"
			write_log('XCC Agent Log: Timeout error when sent to XCC')
			time.sleep(5)
			print "XCC Agent Log: Try again start forward result to XCC"
			write_log('XCC Agent Log: Try again start forward result to XCC')
			try:
			    response = opener.open(req, timeout=30).read().strip()
			    print "XCC Agent Log: Forward result to XCC"
			    write_log('XCC Agent Log: Forward result to XCC')
			    print response
			except urllib2.URLError as e:
			    print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			    write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			except socket.timeout:
			    print "XCC Agent Log: Timeout error when sent to XCC"
			    write_log('XCC Agent Log: Timeout error when sent to XCC')		    
		except socket.timeout:
		    print "XCC Agent Log: Timeout error when sent to XCC"
		    write_log('XCC Agent Log: Timeout error when sent to XCC')
		    time.sleep(5)
		    print "XCC Agent Log: Try again start forward result to XCC"
		    write_log('XCC Agent Log: Try again start forward result to XCC')
		    try:
			response = opener.open(req, timeout=30).read().strip()
			print "XCC Agent Log: Forward result to XCC"
			write_log('XCC Agent Log: Forward result to XCC')
			print response
		    except urllib2.URLError as e:
			print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			time.sleep(5)
			print "XCC Agent Log: Try again start forward result to XCC"
			write_log('XCC Agent Log: Try again start forward result to XCC')
			try:
			    response = opener.open(req, timeout=30).read().strip()
			    print "XCC Agent Log: Forward result to XCC"
			    write_log('XCC Agent Log: Forward result to XCC')
			    print response
			except urllib2.URLError as e:
			    print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			    write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			except socket.timeout:
			    print "XCC Agent Log: Timeout error when sent to XCC"
			    write_log('XCC Agent Log: Timeout error when sent to XCC')
		    except socket.timeout:
			print "XCC Agent Log: Timeout error when sent to XCC"
			write_log('XCC Agent Log: Timeout error when sent to XCC')
			time.sleep(5)
			print "XCC Agent Log: Try again start forward result to XCC"
			write_log('XCC Agent Log: Try again start forward result to XCC')
			try:
			    response = opener.open(req, timeout=30).read().strip()
			    print "XCC Agent Log: Forward result to XCC"
			    write_log('XCC Agent Log: Forward result to XCC')
			    print response
			except urllib2.URLError as e:
			    print "XCC Agent Log: Error when sent to XCC (%s) " % e.reason
			    write_log('XCC Agent Log: Error when sent to XCC (%s) ' % e.reason)
			except socket.timeout:
			    print "XCC Agent Log: Timeout error when sent to XCC"
			    write_log('XCC Agent Log: Timeout error when sent to XCC')
			    