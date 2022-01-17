import sys
import urllib2
import os
#import psutil
import time
import netifaces as nif
import subprocess
from wmi import WMI
import simplejson as json
import base64
from PyQt4 import QtGui,QtCore
from XCC_Agent_Design import Ui_Dialog
import Agent_Config
from Agent_log import write_log
write_log('XCC Agent: Start XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
#XCC_Response_Server=None
try:
    auto_start_check=sys.argv[1]
    if(auto_start_check== 'min'):
        auto_start=2
    else:
        auto_start=0    
except:
    auto_start=0
    
global XCC_Service
global XCC_Response_Service 
global XCC_Hot_Folder
global XCC_Nearline_Spectro
Config_array=Agent_Config.Configfile()
class XCC_Agent_Design(QtGui.QDialog):
    def __init__(self):
        
        QtGui.QDialog.__init__(self,None,QtCore.Qt.WindowCloseButtonHint)        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.SetupSignals()
        self.loadini()
        self.createActions()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()        
        self.service_check()
        
    
    
    
        
    
    def Quit(self): 
        PROCNAME_XCC_service = "XCC_Service.exe" 
        PROCNAME_XCC_Response_Service = "XCC_Response_Service.exe"
        PROCNAME_XCC_Hot_Folder = "XCC_Hot_Folder.exe"
        PROCNAME_XCC_Nearline_Spectro = "XCC_Nearline_Spectro.exe"
        Start_XCC_service=0
        Start_XCC_Response_Service=0    
        Start_XCC_Hot_Folder=0
        Start_XCC_Nearline_Spectro=0
        """import wmi
                
        check = WMI ()
                    
        for process in check.Win32_Process ():
            if process.Name ==PROCNAME_XCC_service:          
                Start_XCC_service=1 
            if process.Name ==PROCNAME_XCC_Response_Service:          
                Start_XCC_Response_Service=1
            if process.Name ==PROCNAME_XCC_Hot_Folder:          
                Start_XCC_Hot_Folder=1 
            if process.Name ==PROCNAME_XCC_Nearline_Spectro:          
                Start_XCC_Nearline_Spectro=1             
        """ 
	task_manager_lines = os.popen("tasklist").readlines()
	for line in task_manager_lines:
	    if str(line[0:28]) == PROCNAME_XCC_service + (28 - len(PROCNAME_XCC_service) )* ' ':
		Start_XCC_service=1
	    if str(line[0:28]) == PROCNAME_XCC_Response_Service + (28 - len(PROCNAME_XCC_Response_Service) )* ' ':
		Start_XCC_Response_Service=1	    	    
	    if str(line[0:28]) == PROCNAME_XCC_Hot_Folder + (28 - len(PROCNAME_XCC_Hot_Folder) )* ' ':
		Start_XCC_Hot_Folder=1
	    if str(line[0:28]) == PROCNAME_XCC_Nearline_Spectro + (28 - len(PROCNAME_XCC_Nearline_Spectro) )* ' ':
		Start_XCC_Nearline_Spectro=1  
		
        if Start_XCC_service == 1: 
            global XCC_Service
            subprocess.Popen("taskkill /F /T /PID %i"%XCC_Service.pid ,shell=True)
            
        if Start_XCC_Response_Service == 1:    
            global XCC_Response_Service
            subprocess.Popen("taskkill /F /T /PID %i"%XCC_Response_Service.pid ,shell=True)
        if Start_XCC_Hot_Folder == 1:    
            global XCC_Hot_Folder
            subprocess.Popen("taskkill /F /T /PID %i"%XCC_Hot_Folder.pid ,shell=True)
        if Start_XCC_Nearline_Spectro == 1:    
            global XCC_Nearline_Spectro
            subprocess.Popen("taskkill /F /T /PID %i"%XCC_Nearline_Spectro.pid ,shell=True)        
        
        write_log('XCC Agent: Stop')
        write_log('XCC Agent: Stop XCC Service')
        write_log('XCC Agent: Stop Response Service')
        write_log('XCC Agent: Stop Hot Folder') 
        write_log('XCC Agent: Stop Nearline Spectro') 
        QtGui.qApp.quit() 
        
    def User_Connect(self):
        write_log('XCC Agent: Connect User to XCC')
        if(self.ui.lineEditEmail.text()!='' and self.ui.lineEditPassword.text()!=''):
            Config_array=Agent_Config.Configfile()
	    if(Config_array[0] =="True"):
		proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% (Config_array[1],Config_array[2])})
	    else:
		proxy_handeler = urllib2.ProxyHandler({})
	    opener_proxy = urllib2.build_opener(proxy_handeler)            
	    get_waiting_project= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_setup.php?user_email=%s&user_password=%s&system_mac=%s&system_ip=%s&system_rport=%s&agent_version=%s&ip_and_mac=%s" % get_macaddress(host='localhost',email=self.ui.lineEditEmail.text(),password=self.ui.lineEditPassword.text(),rport=Config_array[3],AV=Agent_Config.XCC_Agent_Version))
			
	    try:
		read_waiting_project = opener_proxy.open(get_waiting_project)            
                waiting_project = json.load(read_waiting_project)
        
                if(waiting_project['Status']=='1'):
                    Agent_Config.Write_confile(User=waiting_project['Email'],Password=waiting_project['Password'],Config=1)
                    self.ui.pushButtonUser_Connect.setEnabled(0)
                    self.ui.pushButtonUser_Reset.setEnabled(1) 
                    write_log('XCC Agent: Passed to connect')
                    restart_XCC_Service()
                    restart_XCC_Response_Service()
                    restart_XCC_Hot_Folder()
                    restart_XCC_Nearline_Spectro()
                else:
                    write_log('XCC Agent: '+waiting_project['Status_msg'])
                    
                self.ui.label_Status.setText(waiting_project['Status_msg'])
            except:
                if(Config_array[0] =="True"):
                    self.ui.label_Status.setText('Can not connect to XCC please check your proxy / firewall settings.')
                    write_log('XCC Agent: Failed to connect Not correct proxy settings')
                    
                else:
                    self.ui.label_Status.setText('Can not connect to XCC.<br>When you are using a proxy server goto the tab proxy.')
                    write_log('XCC Agent: Failed to connect No proxy settings')
        else:
            self.ui.label_Status.setText('Please fill in your Email address and Password.')
            write_log('XCC Agent: Failed to connect No Email address or Password')
        
        
    def User_Reset(self):
        write_log('XCC Agent: Reset User')
        self.ui.lineEditEmail.setText('')
        self.ui.lineEditPassword.setText('')        
        Agent_Config.Write_confile(User='',Password='',Config=0)
        self.ui.pushButtonUser_Connect.setEnabled(1) 
        self.ui.pushButtonUser_Reset.setEnabled(0)
        self.ui.label_Status.setText('')
        quit_XCC_service()
            
    def Proxy_Enable(self):
        if self.ui.checkBoxProxy.isChecked(): 
            #Agent_Config.Write_confile(Use_proxy=self.ui.checkBoxProxy.isChecked())
            self.ui.lineEditProxy_Address.setEnabled(1)
            self.ui.lineEditProxy_Port.setEnabled(1)
            self.ui.pushButtonProxy_Save.setEnabled(1)
            self.ui.pushButtonProxy_Reset.setEnabled(0)
            quit_XCC_service()
        else:
            Agent_Config.Write_confile(Use_proxy=self.ui.checkBoxProxy.isChecked())
            self.ui.lineEditProxy_Address.setEnabled(0)
            self.ui.lineEditProxy_Port.setEnabled(0)
            self.ui.pushButtonProxy_Save.setEnabled(0)
            self.ui.pushButtonProxy_Reset.setEnabled(0)
            self.ui.labelProxySetupError.setText('')
            Config_array=Agent_Config.Configfile()
            if(Config_array[4]!=''):                
                restart_XCC_Hot_Folder()
                restart_XCC_Response_Service()
                restart_XCC_Service()
                restart_XCC_Nearline_Spectro()
            
    def Proxy_Save(self):
        write_log('XCC Agent: Save proxy')
        if(self.ui.lineEditProxy_Address.text().trimmed().isEmpty()):
            self.ui.labelProxySetupError.setText('Fill in Proxy address.')
            write_log('XCC Agent: Failed No proxy address')
        elif(self.ui.lineEditProxy_Port.text().trimmed().isEmpty()):
            self.ui.labelProxySetupError.setText('Fill in Proxy Port number.')
            write_log('XCC Agent: Failed No proxy port number')
        elif(self.ui.lineEditProxy_Port.text().toInt()[0]== 0):
            
            self.ui.labelProxySetupError.setText('Not a correct Proxy Port number.')
            write_log('XCC Agent: Failed No correct proxy port number')
        
        else: 
            self.ui.labelProxySetupError.setText('')
            Agent_Config.Write_confile(Use_proxy=self.ui.checkBoxProxy.isChecked(),Proxy_url=self.ui.lineEditProxy_Address.text(),Porxy_Port=self.ui.lineEditProxy_Port.text())
            self.ui.pushButtonProxy_Save.setEnabled(0)
            self.ui.pushButtonProxy_Reset.setEnabled(1)             
            write_log('XCC Agent: Proxy save correct')
            restart_XCC_Service()
            restart_XCC_Response_Service()
            restart_XCC_Hot_Folder()
            restart_XCC_Nearline_Spectro()
            #XCC_Response_Server=subprocess.Popen("XCC_Response_Server.exe", shell=True)
            
    def Proxy_Reset(self):
        write_log('XCC Agent: Reset proxy')
        self.ui.checkBoxProxy.setChecked(0) 
        self.ui.lineEditProxy_Address.setText('')
        self.ui.lineEditProxy_Port.setText('') 
        Agent_Config.Write_confile(Use_proxy='False',Proxy_url='eMPTY',Porxy_Port='eMPTY')
        self.ui.pushButtonProxy_Save.setEnabled(0)
        self.ui.pushButtonProxy_Reset.setEnabled(0)
        self.ui.lineEditProxy_Address.setEnabled(0)
        self.ui.lineEditProxy_Port.setEnabled(0)        
        #restart_XCC_Response_Service()
        Config_array=Agent_Config.Configfile()
        if(Config_array[4]!=''):                
            restart_XCC_Service()
            restart_XCC_Response_Service()
            restart_XCC_Hot_Folder()
            restart_XCC_Nearline_Spectro()
        else:
            quit_XCC_service()
        #XCC_Response_Server=subprocess.Popen("XCC_Response_Server.exe", shell=True)
    def rPortDefault(self):
        write_log('XCC Agent: Set response port back to default')
        self.ui.lineEditPort.setText('8000')
        self.ui.labelrPortError.setText('')
        Agent_Config.Write_confile(Response_port='8000')
        Config_array=Agent_Config.Configfile()
        if Config_array[6]=='0':
            quit_XCC_service()           
        else:
            restart_XCC_Response_Service()
            restart_XCC_Hot_Folder()  
            restart_XCC_Nearline_Spectro()
            
    def Download_updates(self):
        
        import webbrowser #XCC_Agent_Updates.php?v="+Agent_Config.XCC_Agent_Version
        webbrowser.open("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Download_Update.php")
    def rPort_Save(self):
        write_log('XCC Agent: Save response port')
        if(self.ui.lineEditPort.text().trimmed().isEmpty()):
            self.ui.labelrPortError.setText('Please fill in the incomming connection port.(Default 8000)')
            write_log('XCC Agent: Failed No response port')
        elif(self.ui.lineEditPort.text().toInt()[0]== 0):
            self.ui.labelrPortError.setText('Not a correct incomming connection port')        
            write_log('XCC Agent: Failed No correct response port')
        elif((self.ui.lineEditPort.text().toInt()[0]<= 0) or (self.ui.lineEditPort.text().toInt()[0]>= 65536)):
            self.ui.labelrPortError.setText('Between 1 - 65535')
            write_log('XCC Agent: Failed No correct response port')
        else:
            self.ui.labelrPortError.setText('')
            write_log('XCC Agent: Save response port')
            Agent_Config.Write_confile(Response_port=self.ui.lineEditPort.text())  
            restart_XCC_Response_Service()
            restart_XCC_Hot_Folder()
            restart_XCC_Nearline_Spectro()
    def changes_logdays(self): 
        #print self.ui.spinBox_LogDays.value()
        Agent_Config.Write_confile(Log=self.ui.spinBox_LogDays.value())  
            
            
            
    def SetupSignals(self):       
        self.ui.pushButtonUser_Connect.clicked.connect(self.User_Connect) 
        self.ui.pushButtonUser_Reset.clicked.connect(self.User_Reset) 
        self.ui.checkBoxProxy.clicked.connect(self.Proxy_Enable)
        self.ui.pushButtonProxy_Reset.clicked.connect(self.Proxy_Reset)
        self.ui.pushButtonProxy_Save.clicked.connect(self.Proxy_Save)
        self.ui.pushButtonPort_Default.clicked.connect(self.rPortDefault)
        self.ui.pushButtonPort_Save.clicked.connect(self.rPort_Save)
        self.ui.pushButton_Refresh.clicked.connect(self.service_check)
        self.ui.tabWidget.currentChanged.connect(self.tabToStatusTab)
        self.ui.checkBox_RunBootUp.clicked.connect(self.set_BootUp)
        self.ui.spinBox_LogDays.valueChanged.connect(self.changes_logdays)
        self.ui.pushButton_DownloadUpdate.clicked.connect(self.Download_updates)
        
    def tabToStatusTab(self,arg=None):        
        if arg==0:            
            self.service_check()
     
    def setup_button(self):        
        self.ui.tabWidget.setCurrentIndex(0)
        self.showNormal()
        self.service_check()
     
     
       
    def createActions(self):     
       
       
        self.setupAction = QtGui.QAction("Setup", self,
                       triggered=self.setup_button)
              
        self.quitAction = QtGui.QAction("&Quit", self,
                                   triggered=self.Quit)  
        
    def onTrayiconActivated(self,reason):
        if reason== QtGui.QSystemTrayIcon.DoubleClick:
            self.setup_button()
        
        
    def service_check(self):
        write_log('XCC Agent: Start status Check')
        Start_SaasColorManagement=0
        Config_array=Agent_Config.Configfile()
	if(Config_array[0] =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% (Config_array[1],Config_array[2])})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)                    
	get_waiting_project= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_status.php?user_email=%s&user_password=%s&system_mac=%s&system_ip=%s&system_rport=%s&agent_version=%s&ip_and_mac=%s" % get_macaddress(host='localhost',email=Config_array[4],password=Config_array[5],rport=Config_array[3],AV=Agent_Config.XCC_Agent_Version))        
	try:             
	    read_waiting_project = opener_proxy.open(get_waiting_project)                
            waiting_project = json.load(read_waiting_project)
                
            Start_SaasColorManagement=waiting_project['Status']
        except: 
            Start_SaasColorManagement=0
        
        if Start_SaasColorManagement == 2:
            self.ui.status_web.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_web.setText("Connected")
            write_log('XCC Agent: XCC web Connected ok')
        elif Start_SaasColorManagement == 1:
            self.ui.status_web.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_web.setText("Visual but not connected") 
            write_log('XCC Agent: XCC web Not correct user')
            
        elif Start_SaasColorManagement == 13:
            self.ui.status_web.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_web.setText("The IP address of this computer is changed. Use a static IP address.") 
            write_log('XCC Agent: Error: The IP address of this computer is changed.')
            XCC_Agent_Design.User_Reset(self)
        elif Start_SaasColorManagement == 12:
            self.ui.status_web.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_web.setText("Your account is licensed to another computer!") 
            write_log('XCC Agent: Your account is licensed to another computer!')
            XCC_Agent_Design.User_Reset(self)
            
        elif Start_SaasColorManagement == 11:
            self.ui.status_web.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_web.setText("Login error: reconnect XCC Agent!") 
            write_log('XCC Agent: Login error: reconnect XCC Agent!')
            XCC_Agent_Design.User_Reset(self)
            
        elif Start_SaasColorManagement == 10:
            self.ui.status_web.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_web.setText("Wrong login details!") 
            write_log('XCC Agent: Wrong login details!')
            XCC_Agent_Design.User_Reset(self)
            
        else:
            self.ui.status_web.setText("<span style='font-size:18pt; color:red;'>·</span>")
            self.ui.label_status_web.setText("No web access possible! Please check proxy / firewall settings.")
            write_log('XCC Agent: XCC web NOT Visual')        
        
        
        
        PROCNAME_XCC_service = "XCC_Service.exe" 
        PROCNAME_XCC_Response_Service = "XCC_Response_Service.exe"
        PROCNAME_XCC_workflow_service = "XCC_Workflow_Service.exe" 
        PROCNAME_XCC_hot_folder = "XCC_Hot_Folder.exe"
        PROCNAME_XCC_nearline_spectro = "XCC_Nearline_Spectro.exe"
        Start_XCC_service=0
        Start_XCC_Response_Service=0    
        Start_XCC_workflow_service=0 
        Start_XCC_hot_folder=0 
        Start_XCC_nearline_spectro=0 
        """import wmi
        
        check = WMI ()
            
        for process in check.Win32_Process ():
            if process.Name ==PROCNAME_XCC_service:          
                Start_XCC_service=1 
            if process.Name ==PROCNAME_XCC_Response_Service:          
                Start_XCC_Response_Service=1                  
            if process.Name ==PROCNAME_XCC_workflow_service:          
                Start_XCC_workflow_service=1                   
            if process.Name ==PROCNAME_XCC_hot_folder:          
                Start_XCC_hot_folder=1            
            if process.Name ==PROCNAME_XCC_nearline_spectro:          
                Start_XCC_nearline_spectro=1        
        """     
	task_manager_lines = os.popen("tasklist").readlines()
	for line in task_manager_lines:
	    if str(line[0:28]) == PROCNAME_XCC_service + (28 - len(PROCNAME_XCC_service) )* ' ':
		Start_XCC_service=1
	    if str(line[0:28]) == PROCNAME_XCC_Response_Service + (28 - len(PROCNAME_XCC_Response_Service) )* ' ':
		Start_XCC_Response_Service=1
	    if str(line[0:28]) == PROCNAME_XCC_workflow_service + (28 - len(PROCNAME_XCC_workflow_service) )* ' ':
		Start_XCC_workflow_service=1	    
	    if str(line[0:28]) == PROCNAME_XCC_hot_folder + (28 - len(PROCNAME_XCC_hot_folder) )* ' ':
		Start_XCC_hot_folder=1
	    if str(line[0:28]) == PROCNAME_XCC_nearline_spectro + (28 - len(PROCNAME_XCC_nearline_spectro) )* ' ':
		Start_XCC_nearline_spectro=1        
                  
        if Start_XCC_service == 1:
            self.ui.status_XCCService.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_XCCService.setText("Running")
            write_log('XCC Agent: Running XCC Service')
        else:
            self.ui.status_XCCService.setText("<span style='font-size:18pt; color:red;'>·</span>")
            self.ui.label_status_XCCService.setText("Stopped") 
            write_log('XCC Agent: Not started XCC Service')
        
        if Start_XCC_Response_Service == 1:
            self.ui.status_XCCResponseService.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_XCCResponseService.setText("Running")
            write_log('XCC Agent: Running XCC Response Service')
        else:
            self.ui.status_XCCResponseService.setText("<span style='font-size:18pt; color:red;'>·</span>")
            self.ui.label_status_XCCResponseService.setText("Stopped")
            write_log('XCC Agent: Not started XCC Response Service')
            
        if Start_XCC_hot_folder == 1:
            self.ui.status_XCCHotFolder.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_XCCHotFolder.setText("Running")
            write_log('XCC Agent: Running XCC Hot Folder')
        else:
            self.ui.status_XCCHotFolder.setText("<span style='font-size:18pt; color:red;'>·</span>")
            self.ui.label_status_XCCHotFolder.setText("Stopped")
            write_log('XCC Agent: Not started XCC Hot Folder') 
        
        if Start_XCC_nearline_spectro == 1:
            self.ui.status_XCCNearline_Spectro.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_XCCNearline_Spectro.setText("Running")
            write_log('XCC Agent: Running XCC Nearline Spectro')
        else:
            self.ui.status_XCCNearline_Spectro.setText("<span style='font-size:18pt; color:red;'>·</span>")
            self.ui.label_status_XCCNearline_Spectro.setText("Stopped")
            write_log('XCC Agent: Not started XCC Nearline Spectro') 
            
        if Start_XCC_workflow_service == 1:
            self.ui.status_XCCWorkflowService.setText("<span style='font-size:18pt; color:green;'>·</span>")
            self.ui.label_status_XCCWorkflowService.setText("Running")
            write_log('XCC Agent: Running XCC Workflow Service')
        else:
            self.ui.status_XCCWorkflowService.setText("<span style='font-size:18pt; color:orange;'>·</span>")
            self.ui.label_status_XCCWorkflowService.setText("Standby")
            write_log('XCC Agent: Standby XCC Workflow Service')
	
	if(Config_array[0] =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% (Config_array[1],Config_array[2])})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)        
	get_waiting_Updates= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Updates.php?v=%s" % Agent_Config.XCC_Agent_Version)
		    
	try:  			
	    read_waiting_Updates = opener_proxy.open(get_waiting_Updates)        
            waiting_Updates = json.load(read_waiting_Updates)
                            
            if(waiting_Updates['Updates']== 'yes'):
                self.ui.pushButton_DownloadUpdate.setEnabled(1)
                self.ui.pushButton_DownloadUpdate.setText('New updates')
            else:
                self.ui.pushButton_DownloadUpdate.setEnabled(0)
                self.ui.pushButton_DownloadUpdate.setText('No updates')                
            
        except: 
            self.ui.pushButton_DownloadUpdate.setEnabled(0)
            self.ui.pushButton_DownloadUpdate.setText('No updates')                         
                  
    def setIcon(self):
        
        icon = QtGui.QIcon('XCC.ico')
        self.trayIcon.setIcon(icon)
        #self.setWindowIcon(icon)
        self.trayIcon.setToolTip('XCC Agent') 
        
    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.setupAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        
        
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.activated.connect(self.onTrayiconActivated)
        self.trayIcon.setContextMenu(self.trayIconMenu) 
        
        
    def set_BootUp(self):
        from win32com.client import Dispatch
        
        EXE_name='XCC Agent'
        
        if self.ui.checkBox_RunBootUp.isChecked():
            try:
                path = os.path.join(os.path.join(os.environ['APPDATA'],'Microsoft\Windows\Start Menu\Programs\Startup'), "%s.lnk" % EXE_name)
                target = os.path.abspath(sys.executable)
                wDir = os.path.dirname(os.path.abspath(sys.executable))
                icon = os.path.join(os.path.dirname(os.path.abspath(sys.executable)),"XCC.ico")

                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.Arguments = ' min'
                shortcut.WorkingDirectory = wDir
                shortcut.IconLocation = icon
                shortcut.save()
                Agent_Config.Write_confile(AutoStart='1') 
            except:
                Agent_Config.Write_confile(AutoStart='0') 
        else:
            try:
                os.remove(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name))
                Agent_Config.Write_confile(AutoStart='0') 
            except:
                Agent_Config.Write_confile(AutoStart='0')            
            
    
    def loadini(self):
        self.ui.Label_Version_Number.setText(Agent_Config.XCC_Agent_Version)
        Config_array=Agent_Config.Configfile()
        if(Config_array[0]=='True'):
          self.ui.checkBoxProxy.setChecked(1)
          if(Config_array[1]!=''):              
              self.ui.lineEditProxy_Address.setText(Config_array[1])
              self.ui.lineEditProxy_Port.setText(Config_array[2])               
              self.ui.pushButtonProxy_Save.setEnabled(0)
              self.ui.pushButtonProxy_Reset.setEnabled(1)
          else:
              self.ui.pushButtonProxy_Save.setEnabled(1)
              self.ui.pushButtonProxy_Reset.setEnabled(0)              
                
          self.ui.lineEditProxy_Address.setEnabled(1)
          self.ui.lineEditProxy_Port.setEnabled(1)                
          
          #self.ui.pushButtonProxy_Save.setEnabled(1)
          #self.ui.pushButtonProxy_Reset.setEnabled(1)          
        else:
          self.ui.checkBoxProxy.setChecked(0)  
        self.ui.label_Status.setText('')         
        self.ui.lineEditPort.setText(Config_array[3]) 
        if(Config_array[4]!=''):            
            self.ui.lineEditEmail.setText(Config_array[4])
            self.ui.lineEditPassword.setText(Config_array[5])
            self.ui.pushButtonUser_Connect.setEnabled(0)
            self.ui.pushButtonUser_Reset.setEnabled(1)  
        else:
            self.ui.pushButtonUser_Reset.setEnabled(0)
            self.ui.lineEditPassword.setText('')
        if(Config_array[8]=='1'):
            self.ui.checkBox_RunBootUp.setChecked(1)
        else:
            self.ui.checkBox_RunBootUp.setChecked(0)
        self.ui.spinBox_LogDays.setValue(int(Config_array[7]))   
#def start_XCC_Response_Server():
   # XCC_Response_Server=subprocess.Popen("XCC_Response_Server.exe", shell=True)
   # global XCC_Response_Server
def quit_XCC_service():
    global XCC_Service
    global XCC_Response_Service
    global XCC_Hot_Folder
    global XCC_Nearline_Spectro
    try:
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Service.pid ,shell=True)
        
    except:
        Agent_Config.Write_confile(Config='0')
    try:
        
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Response_Service.pid ,shell=True) 
    except:
        Agent_Config.Write_confile(Config='0') 
    try:
                
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Hot_Folder.pid ,shell=True) 
    except:
        Agent_Config.Write_confile(Config='0')
    try:
                        
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Nearline_Spectro.pid ,shell=True) 
    except:
        Agent_Config.Write_confile(Config='0')    
        
    write_log('XCC Agent: Stop XCC Service')
    write_log('XCC Agent: Stop XCC Response Service') 
    write_log('XCC Agent: Stop XCC Hot Folder')
    write_log('XCC Agent: Stop XCC Nearline Spectro')
    
def restart_XCC_Response_Service():
    write_log('XCC Agent: Stop XCC Response Service')
    global XCC_Response_Service
    try:
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Response_Service.pid ,shell=True)     
        XCC_Response_Service.kill
        XCC_Response_Service=subprocess.Popen("XCC_Response_Service.exe", shell=True)
    except:        
        XCC_Response_Service=subprocess.Popen("XCC_Response_Service.exe", shell=True)
    write_log('XCC Agent: Start XCC Response Service') 
   
def restart_XCC_Hot_Folder():
    write_log('XCC Agent: Stop XCC Hot Folder')
    global XCC_Hot_Folder
    try:
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Hot_Folder.pid ,shell=True)     
        XCC_Hot_Folder.kill
        XCC_Hot_Folder=subprocess.Popen("XCC_Hot_Folder.exe", shell=True)
    except:        
        XCC_Hot_Folder=subprocess.Popen("XCC_Hot_Folder.exe", shell=True)
    write_log('XCC Agent: Start XCC Hot Folder') 
   
def restart_XCC_Nearline_Spectro():
    write_log('XCC Agent: Stop XCC Nearline Spectro')
    global XCC_Nearline_Spectro
    try:
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Nearline_Spectro.pid ,shell=True)     
        XCC_Nearline_Spectro.kill
        XCC_Nearline_Spectro=subprocess.Popen("XCC_Nearline_Spectro.exe", shell=True)
    except:        
        XCC_Nearline_Spectro=subprocess.Popen("XCC_Nearline_Spectro.exe", shell=True)
    write_log('XCC Agent: Start XCC Nearline Spectro') 
        
    
def restart_XCC_Service():
    write_log('XCC Agent: Stop XCC Service')
    global XCC_Service
    try:
        subprocess.Popen("taskkill /F /T /PID %i"%XCC_Service.pid ,shell=True)     
        XCC_Service.kill
        XCC_Service=subprocess.Popen("XCC_Service.exe", shell=True) 
    except:
        XCC_Service=subprocess.Popen("XCC_Service.exe", shell=True) 
    write_log('XCC Agent: Start XCC Service')
def get_all_mac_and_ip():
    all_mac_and_ip = []    
    'Returns a list of MACs for interfaces that have given IP, returns None if not found'
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)        
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
            if(if_mac and if_ip):                
                mac_and_ip = [if_ip,if_mac]
                all_mac_and_ip.append(mac_and_ip)        
        except : #ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None     
    return all_mac_and_ip 


def get_macaddress(host,email="None",password="None",rport="None",AV="None"):
    """ Returns the MAC address of a network host, requires >= WIN2K. """
    import ctypes
    import socket
    import struct    
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
    
    
    email_b64 =base64.b64encode(email)
    pw_b64 =base64.b64encode(password)
    return email,password,macaddr[1]+':'+macaddr[2]+':'+macaddr[3]+':'+macaddr[4]+':'+macaddr[5]+':'+macaddr[6],hostip,rport,AV,base64.b64encode(json.dumps(get_all_mac_and_ip()))

if __name__ == "__main__":
    
    
    PROCNAME = "XCC_Agent.exe"  
    Start_app=0
    
    #import wmi
    """c = WMI ()
    
    for process in c.Win32_Process ():
        if process.Name ==PROCNAME:          
            Start_app+=1  
     """
    task_manager_lines = os.popen("tasklist").readlines()
    for line in task_manager_lines:
	if str(line[0:28]) == PROCNAME + (28 - len(PROCNAME) )* ' ':
	    Start_app+=1                 
            #print Start_app            
    if(Start_app<=1):
        Start_SaasColorManagement=0
        Config_array=Agent_Config.Configfile()
                            
        if(Config_array[0] =="True"):
	    proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% (Config_array[1],Config_array[2])})
	else:
	    proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)                              
        get_waiting_project= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_status.php?user_email=%s&user_password=%s&system_mac=%s&system_ip=%s&system_rport=%s&agent_version=%s&ip_and_mac=%s" % get_macaddress(host='localhost',email=Config_array[4],password=Config_array[5],rport=Config_array[3],AV=Agent_Config.XCC_Agent_Version))        
        
        try:      
            
            read_waiting_project = opener_proxy.open(get_waiting_project)
            waiting_project = json.load(read_waiting_project)
                        
            Start_SaasColorManagement=waiting_project['Status']
        except: 
            Start_SaasColorManagement=0 
            
        global XCC_Service
        global XCC_Response_Service
        global XCC_Hot_Folder
        global XCC_Nearline_Spectro
        
        if(Start_SaasColorManagement==10 or Start_SaasColorManagement==11 or Start_SaasColorManagement==12 or Start_SaasColorManagement==13 ):
            EXE_name='XCC Agent'
            try:
                os.remove(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name))
                Agent_Config.Write_confile(User='',Password='',Config='0',AutoStart='0') 
            except:                
                Agent_Config.Write_confile(User='',Password='',Config='0',AutoStart='0')            
            #from PyQt4 import QtCore, QtGui
            _fromUtf8 = QtCore.QString.fromUtf8
                    
            _encoding = QtGui.QApplication.UnicodeUTF8
            def _translate(context, text, disambig):
                return QtGui.QApplication.translate(context, text, disambig, _encoding)        
                    
            app2 = QtGui.QApplication(sys.argv)
            icon2 = QtGui.QIcon()
                                        
            icon2.addPixmap(QtGui.QPixmap(_fromUtf8("XCC.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)           
                    
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowIcon(QtGui.QIcon(icon2))
                           
            msgBox.setWindowTitle(_translate("Dialog", "XCC Automated Settings", None))
            if(Start_SaasColorManagement==13):
                msgBox.setText("Error: The IP address of this computer is changed. Use a static IP address to continue.")
                write_log('XCC Agent: Error: The IP address of this computer is changed.')
            elif(Start_SaasColorManagement==12):
                msgBox.setText("Your account is licensed to another computer!")
                write_log('XCC Agent: Your account is licensed to another computer')
            elif(Start_SaasColorManagement==11):
                msgBox.setText("Login error: reconnect XCC Agent")
                write_log('XCC Agent: Login error: reconnect XCC Agent')                
            else:
                msgBox.setText("Wrong login details!")
                write_log('XCC Agent: Wrong login details')
            #msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtGui.QMessageBox.Close)
            msgBox.setDefaultButton(QtGui.QMessageBox.Close)
                     
            ret = msgBox.exec_()  
            
            
            
        elif(Start_SaasColorManagement==2):
            XCC_Service = subprocess.Popen("XCC_Service.exe", shell=True)      
            XCC_Response_Service=subprocess.Popen("XCC_Response_Service.exe", shell=True)
            XCC_Hot_Folder=subprocess.Popen("XCC_Hot_Folder.exe", shell=True)
            XCC_Nearline_Spectro=subprocess.Popen("XCC_Nearline_Spectro.exe", shell=True)
            write_log('XCC Agent: XCC web Connected ok')
            write_log('XCC Agent: Start XCC Service')
            write_log('XCC Agent: Start XCC Response Service')
            write_log('XCC Agent: Start Hot Folder')
            write_log('XCC Agent: Start Nearline Spectro')
        elif(Start_SaasColorManagement==1):
            write_log('XCC Agent: XCC web Not correct user')
            write_log('XCC Agent: NOT started XCC Service')
            write_log('XCC Agent: NOT started Response Service')
            write_log('XCC Agent: NOT started Hot Folder')
            write_log('XCC Agent: NOT started Nearline Spectro')
        else:
            write_log('XCC Agent: XCC web NOT Visual')
            write_log('XCC Agent: NOT started XCC Service')
            write_log('XCC Agent: NOT started Response Service')   
            write_log('XCC Agent: NOT started Hot Folder')
            write_log('XCC Agent: NOT started Nearline Spectro')
            
        #if(Start_SaasColorManagement!=10):
        app = QtGui.QApplication(sys.argv)    
        QtGui.QApplication.setQuitOnLastWindowClosed(False)
        window = XCC_Agent_Design()
        #window.windowFlags(QtCore.Qt.WindowTitleHint)
        if(Start_SaasColorManagement!=2):
            window.show()             
        elif(auto_start!=2):                   
            window.show()            
        
            
        sys.exit(app.exec_())
       
    else:
        #from PyQt4 import QtCore, QtGui
        _fromUtf8 = QtCore.QString.fromUtf8
        
        _encoding = QtGui.QApplication.UnicodeUTF8
        def _translate(context, text, disambig):
            return QtGui.QApplication.translate(context, text, disambig, _encoding)        

        app = QtGui.QApplication(sys.argv)
        icon = QtGui.QIcon()
                            
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("XCC.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)           
        
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon(icon))
               
        msgBox.setWindowTitle(_translate("Dialog", "XCC Automated Settings", None))
        msgBox.setText("Software already running.")
        #msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Close)
        msgBox.setDefaultButton(QtGui.QMessageBox.Close)
        write_log('XCC Agent: 2nd XCC Agent')         
        ret = msgBox.exec_()         
        
       