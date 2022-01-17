import ConfigParser
import os.path
import base64
from win32com.shell import shell, shellcon
XCC_Agent_Version="2.54"
APP_Dirname="XCC_Agent"
App_TEMP_FILES="Temp"
App_LOG_FILES="Log"
APP_Hotfolder="Hot_folder"
APP_Hotfolder_in="In"
APP_Hotfolder_processed="Processed"
APP_Hotfolder_error="Error"

APP_CONFIG_PATH = os.path.join(os.environ['APPDATA'],APP_Dirname)
APP_TEMP_PATH = os.path.join(APP_CONFIG_PATH,App_TEMP_FILES)
APP_LOG_PATH = os.path.join(APP_CONFIG_PATH,App_LOG_FILES)
APP_CONFIG_FILE=os.path.join(APP_CONFIG_PATH,"Agent_config.ini")

APP_MYDOC_PATH= os.path.join(shell.SHGetSpecialFolderPath(0, shellcon.CSIDL_PERSONAL))
APP_XCC_Agent_PATH= os.path.join(APP_MYDOC_PATH,APP_Dirname)
APP_HOTFOLDER_PATH= os.path.join(APP_XCC_Agent_PATH,APP_Hotfolder)
APP_HOTFOLDER_PATH_IN= os.path.join(APP_XCC_Agent_PATH,APP_Hotfolder,APP_Hotfolder_in)
APP_HOTFOLDER_PATH_PROCESSED= os.path.join(APP_XCC_Agent_PATH,APP_Hotfolder,APP_Hotfolder_processed)
APP_HOTFOLDER_PATH_ERROR= os.path.join(APP_XCC_Agent_PATH,APP_Hotfolder,APP_Hotfolder_error)


App_PROGRAMDATA=os.path.join(os.environ['ProgramData'])

def clear_Hot_folder(): 
        if not os.path.exists(APP_XCC_Agent_PATH):
                os.mkdir(APP_XCC_Agent_PATH)
        if not os.path.exists(APP_HOTFOLDER_PATH):
                os.mkdir(APP_HOTFOLDER_PATH)  
                
        if not os.path.exists(APP_HOTFOLDER_PATH_IN):
                os.mkdir(APP_HOTFOLDER_PATH_IN)
        if not os.path.exists(APP_HOTFOLDER_PATH_PROCESSED):
                os.mkdir(APP_HOTFOLDER_PATH_PROCESSED)  
        if not os.path.exists(APP_HOTFOLDER_PATH_ERROR):
                os.mkdir(APP_HOTFOLDER_PATH_ERROR)                  
                
        for the_file in os.listdir(APP_HOTFOLDER_PATH_IN):
                file_path = os.path.join(APP_HOTFOLDER_PATH_IN, the_file)
                try:
                        if os.path.isfile(file_path):
                                os.unlink(file_path)
                except Exception, e:
                        print e        
                try:
                        if os.path.isdir(file_path):
                                import shutil
                                shutil.rmtree(file_path)
                                os.rmdir(file_path)
                except Exception, e:
                        print e                     




def Configfile(): 
    
    if not os.path.exists(APP_CONFIG_PATH):
        os.mkdir(APP_CONFIG_PATH)
        
    if not os.path.exists(APP_TEMP_PATH):
        os.mkdir(APP_TEMP_PATH)
        
    if not os.path.exists(APP_LOG_PATH):
        os.mkdir(APP_LOG_PATH)    
    if not os.path.isfile(APP_CONFIG_FILE):
        
        config = ConfigParser.RawConfigParser()
        config.add_section('Agent_config')
        config.set('Agent_config', 'Use_proxy', 'False')
        config.set('Agent_config', 'Proxy', '')
        config.set('Agent_config', 'Proxy_port', '')
        config.set('Agent_config', 'Response_port', '8000')
        config.set('Agent_config', 'User', '')
        config.set('Agent_config', 'Pw', '')
        config.set('Agent_config', 'Config', '0')
        config.set('Agent_config', 'Log', '5')
        config.set('Agent_config', 'AutoStart', '0')
        config.set('Agent_config', 'CN', '0')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        EXE_name='XCC Agent'
        if os.path.isfile(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name)):
            os.remove(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name))
        
    config = ConfigParser.ConfigParser()
    config.read(APP_CONFIG_FILE)
    
    if not config.has_section('Agent_config'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.add_section('Agent_config')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)  
        
    if not config.has_option('Agent_config', 'Use_proxy'):    
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Use_proxy', 'False')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'Proxy'):    
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Proxy', '')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)     
    if not config.has_option('Agent_config', 'Proxy_port'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Proxy_port', '')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'Response_port'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Response_port', '8000')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'User'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'User', '')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)     
    if not config.has_option('Agent_config', 'Pw'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Pw', '')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'Config'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Config', '0')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'Log'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'Log', '5')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE) 
    if not config.has_option('Agent_config', 'CN'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'CN', '5')
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
                config.write(configfile) 
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)    
    if not config.has_option('Agent_config', 'AutoStart'):
        config = ConfigParser.RawConfigParser() 
        config.read(APP_CONFIG_FILE)
        config.set('Agent_config', 'AutoStart', '0')
        
        # Writing our configuration file to 'example.cfg'
        with open(APP_CONFIG_FILE, 'wb') as configfile:
            config.write(configfile)
        EXE_name='XCC Agent'
        if os.path.isfile(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name)):
            os.remove(os.path.join(os.environ['APPDATA'],"Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk" % EXE_name))
        
        config = ConfigParser.ConfigParser()
        config.read(APP_CONFIG_FILE)        
        
    
    
    # Set the third, optional argument of get to 1 if you wish to use raw mode.
    config_array=[]
    config_array=(config.get('Agent_config', 'Use_proxy'),
                  config.get('Agent_config', 'Proxy'),
                  config.get('Agent_config', 'Proxy_port'),
                  config.get('Agent_config', 'Response_port'),
                  config.get('Agent_config', 'User'),
                  base64.b64decode(config.get('Agent_config', 'Pw')),
                  config.get('Agent_config', 'Config'),
                  config.get('Agent_config', 'Log'),
                  config.get('Agent_config', 'AutoStart')) # -> "Python is fun!"
    #print config_array
    return config_array
#config_array=(config.get('agent_config', 'proxy')) # -> "%(bar)s is %(baz)s!"


def Write_confile(Use_proxy="DC",Proxy_url="DC",Porxy_Port="DC",Response_port="DC",User="DC",Password="DC",Config="DC",Log="DC",AutoStart="DC"):
    config = ConfigParser.ConfigParser()
    config.read(APP_CONFIG_FILE)  
    if not(Use_proxy=="DC"): 
        config.set('Agent_config', 'Use_proxy', Use_proxy)
    if not(Proxy_url=="DC"):
        if(Proxy_url=="eMPTY"):            
            config.set('Agent_config', 'Proxy', '')
        else:
            config.set('Agent_config', 'Proxy', Proxy_url)
    if not(Porxy_Port=="DC"):
        if(Porxy_Port=="eMPTY"):
            config.set('Agent_config', 'Proxy_port', '')
        else:
            config.set('Agent_config', 'Proxy_port', Porxy_Port)
    if not(Response_port=="DC"):
        config.set('Agent_config', 'Response_port', Response_port)
    if not(User=="DC"):
        config.set('Agent_config', 'User',User)
    if not(Password=="DC"):
        config.set('Agent_config', 'Pw', base64.b64encode(Password))
    if not(Config=="DC"):
        config.set('Agent_config', 'Config', Config)
    if not(Log=="DC"):
        config.set('Agent_config', 'Log', Log)
    if not(AutoStart=="DC"):
        config.set('Agent_config', 'AutoStart', AutoStart)
    with open(APP_CONFIG_FILE, 'wb') as configfile:
                config.write(configfile)     

Configfile()
config = ConfigParser.ConfigParser()
config.read(APP_CONFIG_FILE)
if (config.get('Agent_config', 'CN')=="100"):
        Use_URL="develop"
else:
        Use_URL="www"


Use_Domain="xeikoncolorcontrol.com"
