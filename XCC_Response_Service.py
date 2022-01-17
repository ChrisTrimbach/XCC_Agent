import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import time
import base64
import Agent_Config
import os
import socket
Config_array=Agent_Config.Configfile()
proxy=Config_array[0]
proxysetting=(Config_array[1],Config_array[2])
PORT=int(Config_array[3])
from Agent_log import write_log

class ServerHandler(SimpleHTTPRequestHandler):    
    def do_POST(self):
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        print 'XCC Response Service: Received data'
        write_log('XCC Response Service: Received data')
        import urllib2
        import simplejson as json
	if(proxy =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)	
	get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")
						
	read_Post_URL = opener_proxy.open(get_Post_URL)
	Post_URL = json.load(read_Post_URL)
	print "XCC Response Service: Post URL %s"%Post_URL['Post_URL']	      
        import base64
        import MultipartPostHandler
        params = {'file_data':base64.b64encode(data)}
        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_measured.php", params)
        if(proxy =="True"):
            req.set_proxy('%s:%s'% proxysetting, 'http') 
	    
	
	print "XCC Response Service: Start forward result location to XCC"
	write_log('XCC Response Service: Start forward result location to XCC')	
	try:
	    response = opener.open(req, timeout=30)
	    print "XCC Response Service: Forward result location to XCC"
	    write_log('XCC Response Service: Forward result location to XCC')
	except urllib2.URLError as e:    
	    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
	    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
	    time.sleep(5)
	    print "XCC Response Service: Try again start forward result location to XCC"
	    write_log('XCC Response Service: Try again start forward result location to XCC')
	    try:
		response = opener.open(req, timeout=30)
		print "XCC Response Service: Forward result location to XCC"
		write_log('XCC Response Service: Forward result location to XCC')
	    except urllib2.URLError as e:    
		print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		time.sleep(5)
		print "XCC Response Service: Try again start forward result location to XCC"
		write_log('XCC Response Service: Try again start forward result location to XCC')
		try:
		    response = opener.open(req, timeout=30)
		    print "XCC Response Service: Forward result location to XCC"
		    write_log('XCC Response Service: Forward result location to XCC')
		except urllib2.URLError as e:    
		    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
		except socket.timeout:
		    print "XCC Response Service: Timeout error when sent to XCC"
		    write_log('XCC Response Service: Timeout error when sent to XCC')
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
	    except socket.timeout:
		print "XCC Response Service: Timeout error when sent to XCC"
		write_log('XCC Response Service: Timeout error when sent to XCC')
		time.sleep(5)
		print "XCC Response Service: Try again start forward result location to XCC"
		write_log('XCC Response Service: Try again start forward result location to XCC')
		try:
		    response = opener.open(req, timeout=30)
		    print "XCC Response Service: Forward result location to XCC"
		    write_log('XCC Response Service: Forward result location to XCC')
		except urllib2.URLError as e:    
		    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
		except socket.timeout:
		    print "XCC Response Service: Timeout error when sent to XCC"
		    write_log('XCC Response Service: Timeout error when sent to XCC')
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')	    
	except socket.timeout:
	    print "XCC Response Service: Timeout error when sent to XCC"
	    write_log('XCC Response Service: Timeout error when sent to XCC')
	    time.sleep(5)
	    print "XCC Response Service: Try again start forward result location to XCC"
	    write_log('XCC Response Service: Try again start forward result location to XCC')
	    try:
		response = opener.open(req, timeout=30)
		print "XCC Response Service: Forward result location to XCC"
		write_log('XCC Response Service: Forward result location to XCC')
	    except urllib2.URLError as e:    
		print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		time.sleep(5)
		print "XCC Response Service: Try again start forward result location to XCC"
		write_log('XCC Response Service: Try again start forward result location to XCC')
		try:
		    response = opener.open(req, timeout=30)
		    print "XCC Response Service: Forward result location to XCC"
		    write_log('XCC Response Service: Forward result location to XCC')
		except urllib2.URLError as e:    
		    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
		except socket.timeout:
		    print "XCC Response Service: Timeout error when sent to XCC"
		    write_log('XCC Response Service: Timeout error when sent to XCC')
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
	    except socket.timeout:
		print "XCC Response Service: Timeout error when sent to XCC"
		write_log('XCC Response Service: Timeout error when sent to XCC')
		time.sleep(5)
		print "XCC Response Service: Try again start forward result location to XCC"
		write_log('XCC Response Service: Try again start forward result location to XCC')
		try:
		    response = opener.open(req, timeout=30)
		    print "XCC Response Service: Forward result location to XCC"
		    write_log('XCC Response Service: Forward result location to XCC')
		except urllib2.URLError as e:    
		    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
		    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
		except socket.timeout:
		    print "XCC Response Service: Timeout error when sent to XCC"
		    write_log('XCC Response Service: Timeout error when sent to XCC')
		    print "XCC Response Service: Stopped  forward result location to XCC"
		    write_log('XCC Response Service: Stopped forward result location to XCC')
	
	
	
		
	try:
	    print 'XCC Response Service: Check XCC Cloud answer'
	    write_log('XCC Response Service: Check XCC Cloud answer')	    
	    Location_URL = json.load(response)
	    print 'XCC Response Service: Correct JSON answer of XCC Cloud'
	    write_log('XCC Response Service: Correct JSON answer of XCC Cloud')
	    
	    try:		
		print 'XCC Response Service: Get Cruise Control Status'		
		write_log('XCC Response Service: Get Cruise Control Status')		
		if 'Cruise_Control_Status_JMF' in Location_URL :
		    try:
			import base64
			import requests	
			res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
                                            data=base64.b64decode(Location_URL['Cruise_Control_Status_JMF']),
                                            headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
				
			write_log('XCC Response Service: Send Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")
			read_Post_URL = opener_proxy.open(get_Post_URL)
			Post_URL = json.load(read_Post_URL)
			print Post_URL['Post_URL']
			import MultipartPostHandler
				
			params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
			opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
			urllib2.install_opener(opener)
			req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
			if(proxy =="True"):
			    req.set_proxy('%s:%s'% proxysetting, 'http')
			print "XCC Response Service: Start forward result Cruise Control Status to XCC"
			write_log('XCC Response Service: Start forward result Cruise Control Status to XCC')				    
			try:			    
			    response = opener.open(req, timeout=30).read().strip()
			    print response
			    print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
			    write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			    print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
			    write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			except urllib2.URLError as e: 
			    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
			    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
			    write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')
			    try:
				response = opener.open(req, timeout=30).read().strip()
				print response
				print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			    except urllib2.URLError as e: 
				print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				time.sleep(5)
				print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
				write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response	
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response				
			    except socket.timeout:
				print "XCC Response Service: Timeout error when sent to XCC"
				write_log('XCC Response Service: Timeout error when sent to XCC')
				time.sleep(5)
				print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
				write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')			    
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response	
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response			    
		        except socket.timeout:
			    print "XCC Response Service: Timeout error when sent to XCC"
			    write_log('XCC Response Service: Timeout error when sent to XCC')
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
			    write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')			    try:
				response = opener.open(req, timeout=30).read().strip()
				print response
				print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			    except urllib2.URLError as e: 
				print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				time.sleep(5)
				print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
				write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response	
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response				
			    except socket.timeout:
				print "XCC Response Service: Timeout error when sent to XCC"
				write_log('XCC Response Service: Timeout error when sent to XCC')
				time.sleep(5)
				print "XCC Response Service: Try again start forward Cruise Control Status to XCC"
				write_log('XCC Response Service: Try again start forward Cruise Control Status to XCC')			    
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Cruise Control Status to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response	
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Stop forward result Cruise Control Status to XCC"
				    write_log('XCC Response Service: Stop forward result Cruise Control Status to XCC')			
				    print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response				    
			time.sleep(2)
		    except:
			print 'XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
			write_log('XCC Response Service: Error Direct XML task Cruise Control Status to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Cruise_Control_Status_DXML&w_id=%s" % Location_URL['workflow_id'])				    
			response = opener_proxy.open(req, timeout=30).read().strip()
			print "XCC Response Service: Response %s"%response
		else:
		    print 'XCC Response Service: No Cruise Control Status JMF Set'
		    write_log('XCC Response Service: No Cruise Control Status JMF Set')
	    except:
		print 'XCC Response Service: Error getting JMF Event Cruise Control Status'
		write_log('XCC Response Service: Error getting JMF Event Cruise Control Status')
	    print 'XCC Response Service: Check if measure data location is used'
	    write_log('XCC Response Service: Check if measure data location is used')
	    print "XCC Response Service: File location(%s) %s"%(Location_URL['Job_id'],Location_URL['cgats_url'])	    
	    print 'XCC Response Service: Check if file exists on share location?'
	    write_log('XCC Response Service: File location(%s) %s'%(Location_URL['Job_id'],Location_URL['cgats_url']))
	    write_log('XCC Response Service: Check if file exists on share location?')	    
	    if os.path.isfile(Location_URL['cgats_url']):
		print "XCC Response Service: File found on share(%s)"%Location_URL['Job_id']
		write_log('XCC Response Service: File found on share(%s)'%Location_URL['Job_id'])		
		try:
		    measurement_data_file = open(Location_URL['cgats_url'], 'r').read()	
		    print "XCC Response Service: Read file on share(%s)"%Location_URL['Job_id']
		    write_log('XCC Response Service: Read file on share(%s)'%Location_URL['Job_id'])		
		    import MultipartPostHandler
		    params = {'Job_id':Location_URL['Job_id'],'file_data':base64.b64encode(measurement_data_file)}		
		    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
		    urllib2.install_opener(opener)
		    req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_measured.php", params)
		    if(proxy =="True"):
			req.set_proxy('%s:%s'% proxysetting, 'http')
		    print "XCC Response Service: Start forward share measurement data to XCC"
		    write_log('XCC Response Service: Start forward share measurement data to XCC')		    
		    try:
			response = opener.open(req, timeout=60).read().strip()
			print "XCC Response Service: Response sent to XCC (%s) " % response
			print "XCC Response Service: Forward share measurement data to XCC"
			write_log('XCC Response Service: Forward share measurement data to XCC')
		    except urllib2.URLError as e:    
			print "XCC Response Service: Error when sent to XCC (%s) " % e.reason	
			write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
			time.sleep(5)
			print "XCC Response Service: Try again start forward share measurement data to XCC"
			write_log('XCC Response Service: Try again start forward share measurement data to XCC')
			try:
			    response = opener.open(req, timeout=60).read().strip()
			    print "XCC Response Service: Response sent to XCC (%s) " % response
			    print "XCC Response Service: Forward share measurement data to XCC"
			    write_log('XCC Response Service: Forward share measurement data to XCC')
			except urllib2.URLError as e:    
			    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason	
			    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)			    
			    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
			    response = opener_proxy.open(req, timeout=30).read().strip()			    
			except socket.timeout:			
			    print "XCC Response Service: Timeout error when sent to XCC"
			    write_log('XCC Response Service: Timeout error when sent to XCC')  				
			    print "XCC Response Service: Error sent file to XCC (%s)"%Location_URL['Job_id']	    
			    write_log('XCC Response Service: Error sent file to XCC (%s)'%Location_URL['Job_id'])
			    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
			    response = opener_proxy.open(req, timeout=30).read().strip()			
		    except socket.timeout:			
			print "XCC Response Service: Timeout error when sent to XCC"
			write_log('XCC Response Service: Timeout error when sent to XCC')  
			time.sleep(5)
			print "XCC Response Service: Try again start forward share measurement data to XCC"
			write_log('XCC Response Service: Try again start forward share measurement data to XCC')
			try:
			    response = opener.open(req, timeout=60).read().strip()
			    print "XCC Response Service: Response sent to XCC (%s) " % response
			    print "XCC Response Service: Forward share measurement data to XCC"
			    write_log('XCC Response Service: Forward share measurement data to XCC')
			except urllib2.URLError as e:    
			    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason	
			    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC"
				write_log('XCC Response Service: Forward share measurement data to XCC')
			    except urllib2.URLError as e:
				print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
		            except socket.timeout:
				print "XCC Response Service: Timeout error when sent to XCC"
				write_log('XCC Response Service: Timeout error when sent to XCC')
				print "XCC Response Service: Error sent file to XCC (%s)"%Location_URL['Job_id']
				write_log('XCC Response Service: Error sent file to XCC (%s)'%Location_URL['Job_id'])
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()				    
			except socket.timeout:			
			    print "XCC Response Service: Timeout error when sent to XCC"
			    write_log('XCC Response Service: Timeout error when sent to XCC')
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC"
				write_log('XCC Response Service: Forward share measurement data to XCC')
			    except urllib2.URLError as e:    
				print "XCC Response Service: Error when sent to XCC (%s) " % e.reason	
				write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				print "XCC Response Service: Error sent file to XCC (%s)"%Location_URL['Job_id']
				write_log('XCC Response Service: Error sent file to XCC (%s)'%Location_URL['Job_id'])
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])					    
				response = opener_proxy.open(req, timeout=30).read().strip()					
			    except socket.timeout:			
				print "XCC Response Service: Timeout error when sent to XCC"
				write_log('XCC Response Service: Timeout error when sent to XCC')
				print "XCC Response Service: Error sent file to XCC (%s)"%Location_URL['Job_id']
				write_log('XCC Response Service: Error sent file to XCC (%s)'%Location_URL['Job_id'])
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()		   
		    try:		
			print 'XCC Response Service: Remove JMF Event Persistent Channel'		
			write_log('XCC Response Service: Remove JMF Event Persistent Channel')		
			if 'Remove_JMF' in Location_URL :
			    try:
				import base64
				import requests	
				res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
				                    data=base64.b64decode(Location_URL['Remove_JMF']),
				                    headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
					
				write_log('XCC Response Service: Send Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))           
					
				get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
				read_Post_URL = opener_proxy.open(get_Post_URL)
				Post_URL = json.load(read_Post_URL)
				print Post_URL['Post_URL']	    
				import MultipartPostHandler
					
				params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
				opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
				urllib2.install_opener(opener)
				req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
				if(proxy =="True"):
				    req.set_proxy('%s:%s'% proxysetting, 'http')
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Try again start forward Remove JMF to XCC"
				    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					    
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					
				except socket.timeout:	
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Try again start forward Remove JMF to XCC"
				    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					    
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response		    
			    except:
				print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))                       
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    
				response = opener_proxy.open(req, timeout=30).read().strip()
				print "XCC Response Service: Response %s"%response   			
			else:
			    print 'XCC Response Service: No Remove JMF Set'		
			    write_log('XCC Response Service: No Remove JMF Set')		    
			      
		    except:
			print 'XCC Response Service: Error removing JMF Event Persistent Channel'		
			write_log('XCC Response Service: Error removing JMF Event Persistent Channel')			    
		except:
		    try:
			time.sleep(5)			
			print "XCC Response Service: Error forward share measurement data to XCC"
			write_log('XCC Response Service: Error forward share measurement data to XCC')
			measurement_data_file = open(Location_URL['cgats_url'], 'r').read()	
			print "XCC Response Service: Read file on share(%s)"%Location_URL['Job_id']
			write_log('XCC Response Service: Read file on share(%s)'%Location_URL['Job_id'])		
			import MultipartPostHandler
			params = {'Job_id':Location_URL['Job_id'],'file_data':base64.b64encode(measurement_data_file)}		
			opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
			urllib2.install_opener(opener)
			req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_measured.php", params)
			if(proxy =="True"):
			    req.set_proxy('%s:%s'% proxysetting, 'http')				
			print "XCC Response Service: Start forward share measurement data to XCC first try"
			write_log('XCC Response Service: Start forward share measurement data to XCC first try')
			try:
			    response = opener.open(req, timeout=60).read().strip()
			    print "XCC Response Service: Response sent to XCC first try (%s) " % response
			    print "XCC Response Service: Forward share measurement data to XC first tryC"
			    write_log('XCC Response Service: Forward share measurement data to XCC first try')
			except urllib2.URLError as e:    
			    print "XCC Response Service: Error when sent to XCC first try (%s) " % e.reason	
			    write_log('XCC Response Service: Error when sent to XCC first try (%s) ' % e.reason)
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC first try"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC first try')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC first try (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC first try"
				write_log('XCC Response Service: Forward share measurement data to XCC first try')
			    except urllib2.URLError as e:    
				print "XCC Response Service: Error when sent to XCC first try (%s) " % e.reason	
				write_log('XCC Response Service: Error when sent to XCC first try (%s) ' % e.reason)			    
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()			    
			    except socket.timeout:			
				print "XCC Response Service: Timeout error when sent to XCC first try"
				write_log('XCC Response Service: Timeout error when sent to XCC first try')  				
				print "XCC Response Service: Error sent file to XCC first try (%s)"%Location_URL['Job_id']	    
				write_log('XCC Response Service: Error sent file to XCC first try (%s)'%Location_URL['Job_id'])
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()			
			except socket.timeout:			
			    print "XCC Response Service: Timeout error when sent to XCC first try"
			    write_log('XCC Response Service: Timeout error when sent to XCC first try')  
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC first try"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC first try')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC first try"
				write_log('XCC Response Service: Forward share measurement data to XCC first try')
			    except urllib2.URLError as e:    
				print "XCC Response Service: Error when sent to XCC first try (%s) " % e.reason	
				write_log('XCC Response Service: Error when sent to XCC first try (%s) ' % e.reason)
				time.sleep(5)
				print "XCC Response Service: Try again start forward share measurement data to XCC first try"
				write_log('XCC Response Service: Try again start forward share measurement data to XCC first try')
				try:
				    response = opener.open(req, timeout=60).read().strip()
				    print "XCC Response Service: Response sent to XCC first try (%s) " % response
				    print "XCC Response Service: Forward share measurement data to XCC first try"
				    write_log('XCC Response Service: Forward share measurement data to XCC first try')
				except urllib2.URLError as e:
				    print "XCC Response Service: Error when sent to XCC first try (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC first try (%s) ' % e.reason)
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC first try"
				    write_log('XCC Response Service: Timeout error when sent to XCC first try')
				    print "XCC Response Service: Error sent file to XCC first try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC first try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				    response = opener_proxy.open(req, timeout=30).read().strip()				    
			    except socket.timeout:			
				print "XCC Response Service: Timeout error when sent to XCC first try"
				write_log('XCC Response Service: Timeout error when sent to XCC first try')
				time.sleep(5)
				print "XCC Response Service: Try again start forward share measurement data to XCC first try"
				write_log('XCC Response Service: Try again start forward share measurement data to XCC first try')
				try:
				    response = opener.open(req, timeout=60).read().strip()
				    print "XCC Response Service: Response sent to XCC first try (%s) " % response
				    print "XCC Response Service: Forward share measurement data to XCC first try"
				    write_log('XCC Response Service: Forward share measurement data to XCC first try')
				except urllib2.URLError as e:    
				    print "XCC Response Service: Error when sent to XCC first try (%s) " % e.reason	
				    write_log('XCC Response Service: Error when sent to XCC first try(%s) ' % e.reason)
				    print "XCC Response Service: Error sent file to XCC first try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC first try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])					    
				    response = opener_proxy.open(req, timeout=30).read().strip()					
				except socket.timeout:			
				    print "XCC Response Service: Timeout error when sent to XCC first try"
				    write_log('XCC Response Service: Timeout error when sent to XCC first try')
				    print "XCC Response Service: Error sent file to XCC first try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC first try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				    response = opener_proxy.open(req, timeout=30).read().strip()
			try:		
			    print 'XCC Response Service: Remove JMF Event Persistent Channel'		
			    write_log('XCC Response Service: Remove JMF Event Persistent Channel')		
			    if 'Remove_JMF' in Location_URL :
				try:
				    import base64
				    import requests	
				    res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
					                data=base64.b64decode(Location_URL['Remove_JMF']),
					                headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
					    
				    write_log('XCC Response Service: Send Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))           
					    
				    get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
				    read_Post_URL = opener_proxy.open(get_Post_URL)
				    Post_URL = json.load(read_Post_URL)
				    print Post_URL['Post_URL']	    
				    import MultipartPostHandler
					    
				    params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
				    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
				    urllib2.install_opener(opener)
				    req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
				    if(proxy =="True"):
					req.set_proxy('%s:%s'% proxysetting, 'http')			    
				    
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
				   
				   			
				except:
				    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response
			    else:
				print 'XCC Response Service: No Remove JMF Set'		
				write_log('XCC Response Service: No Remove JMF Set')		    
				  
			except:
			    print 'XCC Response Service: Error removing JMF Event Persistent Channel'		
			    write_log('XCC Response Service: Error removing JMF Event Persistent Channel')				
		    except:		    
			print "XCC Response Service: Error reading file on share(%s)"%Location_URL['Job_id']
			write_log('XCC Response Service: Error reading file on share(%s)'%Location_URL['Job_id'])
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=READSHAREFILE&w_id=%s" % Location_URL['workflow_id'])						
			response = opener_proxy.open(req, timeout=30).read().strip()		    
	    else:
		print "XCC Response Service: File Not found go to second try on share(%s)"%Location_URL['Job_id']	    
		write_log('XCC Response Service: File Not found go to second try on share(%s)'%Location_URL['Job_id'])	
		time.sleep(5)
		print "XCC Response Service: File location(%s) %s second try"%(Location_URL['Job_id'],Location_URL['cgats_url'])
		print 'XCC Response Service: Check if file exists on share location second try?'
		write_log('XCC Response Service: File location(%s) %s second try'%(Location_URL['Job_id'],Location_URL['cgats_url']))
		write_log('XCC Response Service: Check if file exists on share location? second try')	    		
		if os.path.isfile(Location_URL['cgats_url']):
		    print "XCC Response Service: File found on share(%s) second try"%Location_URL['Job_id']
		    write_log('XCC Response Service: File found on share(%s) second try'%Location_URL['Job_id'])		
		    try:
			measurement_data_file = open(Location_URL['cgats_url'], 'r').read()	
			print "XCC Response Service: Read file on share(%s) second try"%Location_URL['Job_id']
			write_log('XCC Response Service: Read file on share(%s) second try'%Location_URL['Job_id'])		
			import MultipartPostHandler
			params = {'Job_id':Location_URL['Job_id'],'file_data':base64.b64encode(measurement_data_file)}		
			opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
			urllib2.install_opener(opener)
			req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_measured.php", params)
			if(proxy =="True"):
			    req.set_proxy('%s:%s'% proxysetting, 'http')				
			print "XCC Response Service: Start forward share measurement data to XCC second try"
			write_log('XCC Response Service: Start forward share measurement data to XCC second try')
			try:
			    response = opener.open(req, timeout=60).read().strip()
			    print "XCC Response Service: Response sent to XCC second try (%s) " % response
			    print "XCC Response Service: Forward share measurement data to XCC second try "
			    write_log('XCC Response Service: Forward share measurement data to XCC second try ')
			except urllib2.URLError as e:    
			    print "XCC Response Service: Error when sent to XCC second try second try (%s) " % e.reason	
			    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC second try"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC second try (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC second try"
				write_log('XCC Response Service: Forward share measurement data to XCC second try')
			    except urllib2.URLError as e:    
				print "XCC Response Service: Error when sent to XCC second try (%s) " % e.reason	
				write_log('XCC Response Service: Error when sent to XCC second try (%s) ' % e.reason)			    
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()			    
			    except socket.timeout:			
				print "XCC Response Service: Timeout error when sent to XCC second try"
				write_log('XCC Response Service: Timeout error when sent to XCC second try')  				
				print "XCC Response Service: Error sent file to XCC second try (%s)"%Location_URL['Job_id']	    
				write_log('XCC Response Service: Error sent file to XCC second try (%s)'%Location_URL['Job_id'])
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				response = opener_proxy.open(req, timeout=30).read().strip()			
			except socket.timeout:			
			    print "XCC Response Service: Timeout error when sent to XCC second try"
			    write_log('XCC Response Service: Timeout error when sent to XCC second try')  
			    time.sleep(5)
			    print "XCC Response Service: Try again start forward share measurement data to XCC second try"
			    write_log('XCC Response Service: Try again start forward share measurement data to XCC second try')
			    try:
				response = opener.open(req, timeout=60).read().strip()
				print "XCC Response Service: Response sent to XCC (%s) " % response
				print "XCC Response Service: Forward share measurement data to XCC second try"
				write_log('XCC Response Service: Forward share measurement data to XCC second try')
			    except urllib2.URLError as e:    
				print "XCC Response Service: Error when sent to XCC second try (%s) " % e.reason	
				write_log('XCC Response Service: Error when sent to XCC second try (%s) ' % e.reason)
				time.sleep(5)
				print "XCC Response Service: Try again start forward share measurement data to XCC second try"
				write_log('XCC Response Service: Try again start forward share measurement data to XCC second try')
				try:
				    response = opener.open(req, timeout=60).read().strip()
				    print "XCC Response Service: Response sent to XCC second try (%s) " % response
				    print "XCC Response Service: Forward share measurement data to XCC second try"
				    write_log('XCC Response Service: Forward share measurement data to XCC second try')
				except urllib2.URLError as e:
				    print "XCC Response Service: Error when sent to XCC second try (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC second try (%s) ' % e.reason)
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				except socket.timeout:
				    print "XCC Response Service: Timeout error when sent to XCC second try"
				    write_log('XCC Response Service: Timeout error when sent to XCC second try')
				    print "XCC Response Service: Error sent file to XCC second try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC second try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				    response = opener_proxy.open(req, timeout=30).read().strip()				    
			    except socket.timeout:			
				print "XCC Response Service: Timeout error when sent to XCC second try"
				write_log('XCC Response Service: Timeout error when sent to XCC second try')
				time.sleep(5)
				print "XCC Response Service: Try again start forward share measurement data to XCC second try"
				write_log('XCC Response Service: Try again start forward share measurement data to XCC second try')
				try:
				    response = opener.open(req, timeout=60).read().strip()
				    print "XCC Response Service: Response sent to XCC second try (%s) " % response
				    print "XCC Response Service: Forward share measurement data to XCC second try"
				    write_log('XCC Response Service: Forward share measurement data to XCC second try')
				except urllib2.URLError as e:    
				    print "XCC Response Service: Error when sent to XCC second try (%s) " % e.reason	
				    write_log('XCC Response Service: Error when sent to XCC second try (%s) ' % e.reason)
				    print "XCC Response Service: Error sent file to XCC second try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC second try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])					    
				    response = opener_proxy.open(req, timeout=30).read().strip()					
				except socket.timeout:			
				    print "XCC Response Service: Timeout error when sent to XC second tryC"
				    write_log('XCC Response Service: Timeout error when sent to XCC second try')
				    print "XCC Response Service: Error sent file to XCC second try (%s)"%Location_URL['Job_id']
				    write_log('XCC Response Service: Error sent file to XCC second try (%s)'%Location_URL['Job_id'])
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=UPLOADISSUE&w_id=%s" % Location_URL['workflow_id'])
				    response = opener_proxy.open(req, timeout=30).read().strip()
			try:		
			    print 'XCC Response Service: Remove JMF Event Persistent Channel second try'		
			    write_log('XCC Response Service: Remove JMF Event Persistent Channel second try')		
			    if 'Remove_JMF' in Location_URL :
				try:
				    import base64
				    import requests	
				    res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
					                data=base64.b64decode(Location_URL['Remove_JMF']),
					                headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
					    
				    write_log('XCC Response Service: Send Direct XML task Remove Channel to DFE %s of workflow id %s second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))           
					    
				    get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
				    read_Post_URL = opener_proxy.open(get_Post_URL)
				    Post_URL = json.load(read_Post_URL)
				    print Post_URL['Post_URL']	    
				    import MultipartPostHandler
					    
				    params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
				    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
				    urllib2.install_opener(opener)
				    req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
				    if(proxy =="True"):
					req.set_proxy('%s:%s'% proxysetting, 'http')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
				except:
				    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))                       
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response   			
			    else:
				print 'XCC Response Service: No Remove JMF Set second try'		
				write_log('XCC Response Service: No Remove JMF Set second try')		    
				  
			except:
			    print 'XCC Response Service: Error removing JMF Event Persistent Channel second try'		
			    write_log('XCC Response Service: Error removing JMF Event Persistent Channel second try')				
		    except:
			print "XCC Response Service: Error reading file on share(%s) second try"%Location_URL['Job_id']
			write_log('XCC Response Service: Error reading file on share(%s) second try'%Location_URL['Job_id'])
			req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=READSHAREFILE&w_id=%s" % Location_URL['workflow_id'])						    
			response = opener_proxy.open(req, timeout=30).read().strip()
			try:		
			    print 'XCC Response Service: Remove JMF Event Persistent Channel second try'		
			    write_log('XCC Response Service: Remove JMF Event Persistent Channel second try')		
			    if 'Remove_JMF' in Location_URL :
				try:
				    import base64
				    import requests	
				    res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
					                data=base64.b64decode(Location_URL['Remove_JMF']),
					                headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
					    
				    write_log('XCC Response Service: Send Direct XML task Remove Channel to DFE %s of workflow id %s  second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))           
					    
				    get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
				    read_Post_URL = opener_proxy.open(get_Post_URL)
				    Post_URL = json.load(read_Post_URL)
				    print Post_URL['Post_URL']	    
				    import MultipartPostHandler
					    
				    params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
				    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
				    urllib2.install_opener(opener)
				    req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
				    if(proxy =="True"):
					req.set_proxy('%s:%s'% proxysetting, 'http')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response					    
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    time.sleep(5)
					    print "XCC Response Service: Try again start forward Remove JMF to XCC"
					    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					    try:
						response = opener.open(req, timeout=30).read().strip()
						print response
						print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
						write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    except urllib2.URLError as e: 
						print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
						write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response
					    except socket.timeout:	
						print "XCC Response Service: Timeout error when sent to XCC"
						write_log('XCC Response Service: Timeout error when sent to XCC')
						print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
						write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
						req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						response = opener_proxy.open(req, timeout=30).read().strip()
						print "XCC Response Service: Response %s"%response	
				except:
				    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s second try'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))                       
				    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
						
				    response = opener_proxy.open(req, timeout=30).read().strip()
				    print "XCC Response Service: Response %s"%response   			
			    else:
				print 'XCC Response Service: No Remove JMF Set second try'		
				write_log('XCC Response Service: No Remove JMF Set second try')		    
				  
			except:
			    print 'XCC Response Service: Error removing JMF Event Persistent Channel second try'		
			    write_log('XCC Response Service: Error removing JMF Event Persistent Channel second try')				
		else:	    		
		
		    print "XCC Response Service: File Not found second try on share(%s)"%Location_URL['Job_id']	    
		    write_log('XCC Response Service: File Not found second try on share(%s)'%Location_URL['Job_id'])
		    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=NOTFOUNDSHAREFILE&w_id=%s" % Location_URL['workflow_id'])
				
		    response = opener_proxy.open(req, timeout=30).read().strip()
		    try:		
			print 'XCC Response Service: Remove JMF Event Persistent Channel'		
			write_log('XCC Response Service: Remove JMF Event Persistent Channel')		
			if 'Remove_JMF' in Location_URL :
			    try:
				import base64
				import requests	
				res = requests.post(url='http://%s:%s'% (Location_URL['Printer_ip'],Location_URL['JMF_port']),
				                    data=base64.b64decode(Location_URL['Remove_JMF']),
				                    headers={'MIME-Version': '1.0','content-description': 'XCC DXML Package'})
					
				write_log('XCC Response Service: Send Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))           
					
				get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")			
				read_Post_URL = opener_proxy.open(get_Post_URL)
				Post_URL = json.load(read_Post_URL)
				print Post_URL['Post_URL']	    
				import MultipartPostHandler
					
				params = {'file_data':base64.b64encode(res.text.encode('utf-8'))}
				opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
				urllib2.install_opener(opener)
				req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_xml.php?w_id=%s" % Location_URL['workflow_id'], params)
				if(proxy =="True"):
				    req.set_proxy('%s:%s'% proxysetting, 'http')
				try:
				    response = opener.open(req, timeout=30).read().strip()
				    print response
				    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
				    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				except urllib2.URLError as e: 
				    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
				    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
				    time.sleep(5)
				    print "XCC Response Service: Try again start forward Remove JMF to XCC"
				    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					    
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					
				except socket.timeout:	
				    print "XCC Response Service: Timeout error when sent to XCC"
				    write_log('XCC Response Service: Timeout error when sent to XCC')
				    time.sleep(5)
				    print "XCC Response Service: Try again start forward Remove JMF to XCC"
				    write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
				    try:
					response = opener.open(req, timeout=30).read().strip()
					print response
					print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
				    except urllib2.URLError as e: 
					print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response					    
				    except socket.timeout:	
					print "XCC Response Service: Timeout error when sent to XCC"
					write_log('XCC Response Service: Timeout error when sent to XCC')
					time.sleep(5)
					print "XCC Response Service: Try again start forward Remove JMF to XCC"
					write_log('XCC Response Service: Try again start forward Remove JMF to XCC')
					try:
					    response = opener.open(req, timeout=30).read().strip()
					    print response
					    print "XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s "% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Completed Direct XML task Remove JMF to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    print "XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC"% (Location_URL['Printer_ip'],Location_URL['workflow_id']) 
					    write_log('XCC Response Service: Forward response Direct XML task Remove JMF to DFE %s of workflow id %s to XCC'% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					except urllib2.URLError as e: 
					    print "XCC Response Service: Error when sent to XCC (%s) " % e.reason
					    write_log('XCC Response Service: Error when sent to XCC (%s) ' % e.reason)
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response
					except socket.timeout:	
					    print "XCC Response Service: Timeout error when sent to XCC"
					    write_log('XCC Response Service: Timeout error when sent to XCC')
					    print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
					    write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))
					    req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    response = opener_proxy.open(req, timeout=30).read().strip()
					    print "XCC Response Service: Response %s"%response	    
			    except:
				print 'XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id'])
				write_log('XCC Response Service: Error Direct XML task Remove Channel to DFE %s of workflow id %s '% (Location_URL['Printer_ip'],Location_URL['workflow_id']))                       
				req = urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_sent_error.php?con=Remove_Channel_DXML&w_id=%s" % Location_URL['workflow_id'])
					    
				response = opener_proxy.open(req, timeout=30).read().strip()
				print "XCC Response Service: Response %s"%response   			
			else:
			    print 'XCC Response Service: No Remove JMF Set'		
			    write_log('XCC Response Service: No Remove JMF Set')		    
			      
		    except:
			print 'XCC Response Service: Error removing JMF Event Persistent Channel'		
			write_log('XCC Response Service: Error removing JMF Event Persistent Channel')		    
		
		
		
		
	except:
	    print "XCC Response Service: This option is not used"	
	print "XCC Response Service: Forward data to XCC"
        write_log('XCC Response Service: Forward data to XCC')
        self.send_response(200)
        
   
        
Handler = ServerHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print "XCC Response Service: Start XCC Agent Version %s" % Agent_Config.XCC_Agent_Version 
print "XCC Response Service: Connection with port", PORT
write_log('XCC Response Service: Start XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
write_log('XCC Response Service: Response Port %s'% PORT)
httpd.serve_forever()
