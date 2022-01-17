try:
       # py2exe 0.6.4 introduced a replacement modulefinder.
       # This means we have to add package paths there, not to the built-in
       # one.  If this new modulefinder gets integrated into Python, then
       # we might be able to revert this some day.
       # if this doesn't work, try import modulefinder
       try:
              import py2exe.mf as modulefinder
       except ImportError:
              import modulefinder
       import win32com, sys
       for p in win32com.__path__[1:]:
              modulefinder.AddPackagePath("win32com", p)
       for extra in ["win32com.shell"]: #,"win32com.mapi"
              __import__(extra)
              m = sys.modules[extra]
              for p in m.__path__[1:]:
                     modulefinder.AddPackagePath(extra, p)
except ImportError:
       # no build path setup, no worries.
       pass
from distutils.core import setup
import py2exe

py2exe=dict(compressed=0,
             bundle_files=1)
options_dict={'py2exe':{
                       'bundle_files':   3, # 3 - Don't pack, 2 - Pack all but interpreter, 1 - pack all.
                       'unbuffered':     True,
                       'optimize':       2,
                       'compressed':     True,
                        
                       #'ascii': True,
                       "packages":["gzip"],
                       "excludes": ["PyQt4.uic.port_v3"],
                       "dll_excludes": ["MSVCP90.dll","mswsock.dll", "powrprof.dll",],#"QtCore4.dll","QtGui4.dll"],
                       
                        "includes":["sip"],
                        },
             
            }

prog1=dict(script="XCC_Service.py",
           icon_resources=[(1,"XCC.ico")],
           version="1.0.0"
           )

prog2=dict(script="XCC_Workflow_Agent_Service.py",
           icon_resources=[(1,"XCC.ico")],
           version="1.0.0"
           )
prog3=dict(script="XCC_Response_Server.py",
           icon_resources=[(1,"XCC.ico")],
           version="1.0.0"
           )
prog4=dict(script="XCC_Hot_Folder.py",
           icon_resources=[(1,"XCC.ico")],
           version="1.0.0"
           )
prog5=dict(script="XCC_Nearline_Spectro.py",
           icon_resources=[(1,"XCC.ico")],
           version="1.0.0"
           )
#prog4 = 
             

setup(data_files=[
                ('imageformats',[r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/QtCore4.dll',
    r'C:\\Python27/Lib/site-packages/PyQt4/QtGui4.dll',
    #r'C:\\Python27/Lib/site-packages/PyQt4/QtGui.pyd',
    #r'vcredist_x86.exe'
    r'C:\\Windows/System32/msvcp71.dll',
    #r'C:\\Program Files/Wing IDE 4.1/bin/msvcr71.dll'
    ]),('.',['XCC.ico'])
               ],
     
      options ={'py2exe':{
          'bundle_files':  3, # 3 - Don't pack, 2 - Pack all but interpreter, 1 - pack all.
          'unbuffered':     True,
          'optimize':       2,
          'compressed':     True,
                        
          #'ascii': True,
          "packages":["gzip"],
          "excludes": ["PyQt4.uic.port_v3"],
          "dll_excludes": ["MSVCP90.dll","mswsock.dll", "powrprof.dll",],#"QtCore4.dll","QtGui4.dll"],                       
          "includes":["sip"],
          },
             
                },
     console=[{"script": "no_logo.py",
                             "icon_resources": [(1,"XCC.ico")]},
              {"script": "XCC_Service.py",
                             "icon_resources": [(1,"XCC.ico")]},              
              {"script":"XCC_Workflow_Service.py",
                             "icon_resources": [(1,"XCC.ico")]},
              {"script":"XCC_Response_Service.py",
                             "icon_resources": [(1,"XCC.ico")]},                            
              {"script":"XCC_Hot_Folder.py",
                                           "icon_resources": [(1,"XCC.ico")]},
              {"script":"XCC_Nearline_Spectro.py",
               "icon_resources": [(1,"XCC.ico")]}],
     windows=[{"script":"XCC_Agent.py","icon_resources":[(1, "XCC.ico")]}],
      )
"""


#
cd C:\Users\W7Pro_32\Documents\Python\XCC_Agent_Gui
python setup.py py2exe
"XCC.ico"
XCC_Agent.py',
              'script':'XCC_Agent_Service.py',
              'script':'XCC_Workflow_Agent_Service.py',
              'script':'XCC_Response_Server.py',
              
              
              
              
              
              
pyuic4 -x XCC_Agent_Design.ui -o XCC_Agent_Design.py
"""