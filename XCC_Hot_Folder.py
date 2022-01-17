import urllib2
import requests
import simplejson as json
import subprocess
import time
import ctypes
import socket
import struct
import sys,os,collections
import Agent_Config
from PIL import Image
import glob
import re
from PyQt4.QtGui import *
from PyQt4.QtCore import *
Config_array=Agent_Config.Configfile()
from Agent_log import write_log
proxy=Config_array[0]
proxysetting=(Config_array[1],Config_array[2])
PORT=int(Config_array[3])
#Created Hot folder
Agent_Config.clear_Hot_folder()
seconds = 8

#start hotfolder while        
        
def Read_files_in_hotfolder(File_Collection):
	
        global file_path
	global the_file	
	
        for the_file in os.listdir(Agent_Config.APP_HOTFOLDER_PATH_IN):
                file_path = os.path.join(Agent_Config.APP_HOTFOLDER_PATH_IN, the_file)
		for the_file_COL in os.listdir(Agent_Config.APP_HOTFOLDER_PATH_IN):
			File_Collection[the_file_COL]=1			
                try:
                        if os.path.isfile(file_path):
                                print  'XCC Hot Folder: \nNew File ='+file_path
                                print os.stat(file_path)
                                fileName, fileExtension = os.path.splitext(file_path)
                                             
                                print fileExtension
                                if fileExtension =='.tifxxxxxxxxxxxxx':
                                        isImage = Image.open(file_path)
                                        print isImage.size
                                        _dX=isImage.size[0]/4
                                        _dY=isImage.size[1]/4
                                        dpi = isImage.info['dpi']  # (180, 180)
                                        isImage = isImage.resize((_dX, _dY), Image.BICUBIC)
                                        isImage.save(os.path.join(Agent_Config.APP_HOTFOLDER_PATH_IN,'test.tif'), format = 'TIFF')
                                        print "New Size ",isImage.size, "\n"
                                
                                else:
                                
                                        fp = open("%s" % (file_path),'r')#, encoding='utf-8'
                                        line_nr=1
                                        max_lines_nr=30
                                        read_all_line=fp.readlines()
                                        Correct_cgates=0
                                        while (line_nr<=max_lines_nr):
                                                line_nr_min=line_nr-1
                                                Read_lines=read_all_line[line_nr_min:line_nr]
                                               
                                                Read_line=Read_lines[0].rstrip()                                                
                                                Read_line_array=Read_line.split('\t')                                        
                                                
                                        
                                                if line_nr==1:
                                                        print "XCC Hot Folder: Read line 1 %s"%Read_line_array[0]
                                                        if re.match("CGATS|IS126422|LGOMCCHANNEL01|LGOROWLENGTH", Read_line_array[0].decode("ascii","ignore").encode('utf-8')):
                                                                print "XCC Hot Folder: Match yes"
                                                        else:
                                                                print "XCC Hot Folder: Match no"
                                        
                                        
                                        
                                        
                                        
                                        
                                                if Read_line_array[0]=="DESCRIPTOR":
                                                        try:                                                                                                              
                                                                Target_name=Read_line_array[1].split(':') 
                                                                print "XCC Hot Folder: DESCRIPTOR %s"%Target_name[1].strip().rstrip('"')
                                                       
                                                        except:
                                                                print "XCC Hot Folder: No DESCRIPTOR"
                                        
                                                if(Read_line_array[0] =='SampleID' and
                                                   Read_line_array[1] =='SAMPLE_NAME' and
                                                   Read_line_array[2] =='CMYK_C' and
                                                   Read_line_array[3] =='CMYK_M' and
                                                   Read_line_array[4] =='CMYK_Y' and
                                                   Read_line_array[5] =='CMYK_K' and
                                                   Read_line_array[6] =='LAB_L' and
                                                   Read_line_array[7] =='LAB_A' and
                                                   Read_line_array[8] =='LAB_B' and
                                                   Read_line_array[9] =='nm380' and
                                                   Read_line_array[10] =='nm390' and
                                                   Read_line_array[11] =='nm400' and
                                                   Read_line_array[12] =='nm410' and
                                                   Read_line_array[13] =='nm420' and
                                                   Read_line_array[14] =='nm430' and
                                                   Read_line_array[15] =='nm440' and
                                                   Read_line_array[16] =='nm450' and
                                                   Read_line_array[17] =='nm460' and
                                                   Read_line_array[18] =='nm470' and
                                                   Read_line_array[19] =='nm480' and
                                                   Read_line_array[20] =='nm490' and
                                                   Read_line_array[21] =='nm500' and
                                                   Read_line_array[22] =='nm510' and
                                                   Read_line_array[23] =='nm520' and
                                                   Read_line_array[24] =='nm530' and
                                                   Read_line_array[25] =='nm540' and
                                                   Read_line_array[26] =='nm550' and
                                                   Read_line_array[27] =='nm560' and
                                                   Read_line_array[28] =='nm570' and
                                                   Read_line_array[29] =='nm580' and
                                                   Read_line_array[30] =='nm590' and
                                                   Read_line_array[31] =='nm600' and
                                                   Read_line_array[32] =='nm610' and
                                                   Read_line_array[33] =='nm620' and
                                                   Read_line_array[34] =='nm630' and
                                                   Read_line_array[35] =='nm640' and
                                                   Read_line_array[36] =='nm650' and
                                                   Read_line_array[37] =='nm660' and
                                                   Read_line_array[38] =='nm670' and
                                                   Read_line_array[39] =='nm680' and
                                                   Read_line_array[40] =='nm690' and
                                                   Read_line_array[41] =='nm700' and
                                                   Read_line_array[42] =='nm710' and
                                                   Read_line_array[43] =='nm720'): 
                                                        print "XCC Hot Folder: File Type 203 - 380 - 730 - CMYK"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SampleID' and
                                                     Read_line_array[1] =='SAMPLE_NAME' and
                                                     Read_line_array[2] =='CMYK_C' and
                                                     Read_line_array[3] =='CMYK_M' and
                                                     Read_line_array[4] =='CMYK_Y' and
                                                     Read_line_array[5] =='CMYK_K' and
                                                     Read_line_array[6] =='LAB_L' and
                                                     Read_line_array[7] =='LAB_A' and
                                                     Read_line_array[8] =='LAB_B' and
                                                     Read_line_array[9] =='nm400' and
                                                     Read_line_array[10] =='nm410' and
                                                     Read_line_array[11] =='nm420' and
                                                     Read_line_array[12] =='nm430' and
                                                     Read_line_array[13] =='nm440' and
                                                     Read_line_array[14] =='nm450' and
                                                     Read_line_array[15] =='nm460' and
                                                     Read_line_array[16] =='nm470' and
                                                     Read_line_array[17] =='nm480' and
                                                     Read_line_array[18] =='nm490' and
                                                     Read_line_array[19] =='nm500' and
                                                     Read_line_array[20] =='nm510' and
                                                     Read_line_array[21] =='nm520' and
                                                     Read_line_array[22] =='nm530' and
                                                     Read_line_array[23] =='nm540' and
                                                     Read_line_array[24] =='nm550' and
                                                     Read_line_array[25] =='nm560' and
                                                     Read_line_array[26] =='nm570' and
                                                     Read_line_array[27] =='nm580' and
                                                     Read_line_array[28] =='nm590' and
                                                     Read_line_array[29] =='nm600' and
                                                     Read_line_array[30] =='nm610' and
                                                     Read_line_array[31] =='nm620' and
                                                     Read_line_array[32] =='nm630' and
                                                     Read_line_array[33] =='nm640' and
                                                     Read_line_array[34] =='nm650' and
                                                     Read_line_array[35] =='nm660' and
                                                     Read_line_array[36] =='nm670' and
                                                     Read_line_array[37] =='nm680' and
                                                     Read_line_array[38] =='nm690'):
                                                        print "XCC Hot Folder: File Type 203 - 400 - 700 - CMYK"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SAMPLE_ID' and
                                                     Read_line_array[1] =='CMYK_C' and
                                                     Read_line_array[2] =='CMYK_M' and
                                                     Read_line_array[3] =='CMYK_Y' and
                                                     Read_line_array[4] =='CMYK_K' and
                                                     Read_line_array[5] =='LAB_L' and
                                                     Read_line_array[6] =='LAB_A' and
                                                     Read_line_array[7] =='LAB_B' and
                                                     Read_line_array[8] =='SPECTRAL_380' and
                                                     Read_line_array[9] =='SPECTRAL_390' and
                                                     Read_line_array[10] =='SPECTRAL_400' and
                                                     Read_line_array[11] =='SPECTRAL_410' and
                                                     Read_line_array[12] =='SPECTRAL_420' and
                                                     Read_line_array[13] =='SPECTRAL_430' and
                                                     Read_line_array[14] =='SPECTRAL_440' and
                                                     Read_line_array[15] =='SPECTRAL_450' and
                                                     Read_line_array[16] =='SPECTRAL_460' and
                                                     Read_line_array[17] =='SPECTRAL_470' and
                                                     Read_line_array[18] =='SPECTRAL_480' and
                                                     Read_line_array[19] =='SPECTRAL_490' and
                                                     Read_line_array[20] =='SPECTRAL_500' and
                                                     Read_line_array[21] =='SPECTRAL_510' and
                                                     Read_line_array[22] =='SPECTRAL_520' and
                                                     Read_line_array[23] =='SPECTRAL_530' and
                                                     Read_line_array[24] =='SPECTRAL_540' and
                                                     Read_line_array[25] =='SPECTRAL_550' and
                                                     Read_line_array[26] =='SPECTRAL_560' and
                                                     Read_line_array[27] =='SPECTRAL_570' and
                                                     Read_line_array[28] =='SPECTRAL_580' and
                                                     Read_line_array[29] =='SPECTRAL_590' and
                                                     Read_line_array[30] =='SPECTRAL_600' and
                                                     Read_line_array[31] =='SPECTRAL_610' and
                                                     Read_line_array[32] =='SPECTRAL_620' and
                                                     Read_line_array[33] =='SPECTRAL_630' and
                                                     Read_line_array[34] =='SPECTRAL_640' and
                                                     Read_line_array[35] =='SPECTRAL_650' and
                                                     Read_line_array[36] =='SPECTRAL_660' and
                                                     Read_line_array[37] =='SPECTRAL_670' and
                                                     Read_line_array[38] =='SPECTRAL_680' and
                                                     Read_line_array[39] =='SPECTRAL_690' and
                                                     Read_line_array[40] =='SPECTRAL_700' and
                                                     Read_line_array[41] =='SPECTRAL_710' and
                                                     Read_line_array[42] =='SPECTRAL_720'):
                                                        print "XCC Hot Folder: File Type 154 - 380 - 730 - CMYK"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SAMPLE_ID' and
                                                     Read_line_array[1] =='CMYK_C' and
                                                     Read_line_array[2] =='CMYK_M' and
                                                     Read_line_array[3] =='CMYK_Y' and
                                                     Read_line_array[4] =='CMYK_K' and
                                                     Read_line_array[5] =='LAB_L' and
                                                     Read_line_array[6] =='LAB_A' and
                                                     Read_line_array[7] =='LAB_B' and
                                                     Read_line_array[8] =='SPECTRAL_400' and
                                                     Read_line_array[9] =='SPECTRAL_410' and
                                                     Read_line_array[10] =='SPECTRAL_420' and
                                                     Read_line_array[11] =='SPECTRAL_430' and
                                                     Read_line_array[12] =='SPECTRAL_440' and
                                                     Read_line_array[13] =='SPECTRAL_450' and
                                                     Read_line_array[14] =='SPECTRAL_460' and
                                                     Read_line_array[15] =='SPECTRAL_470' and
                                                     Read_line_array[16] =='SPECTRAL_480' and
                                                     Read_line_array[17] =='SPECTRAL_490' and
                                                     Read_line_array[18] =='SPECTRAL_500' and
                                                     Read_line_array[19] =='SPECTRAL_510' and
                                                     Read_line_array[20] =='SPECTRAL_520' and
                                                     Read_line_array[21] =='SPECTRAL_530' and
                                                     Read_line_array[22] =='SPECTRAL_540' and
                                                     Read_line_array[23] =='SPECTRAL_550' and
                                                     Read_line_array[24] =='SPECTRAL_560' and
                                                     Read_line_array[25] =='SPECTRAL_570' and
                                                     Read_line_array[26] =='SPECTRAL_580' and
                                                     Read_line_array[27] =='SPECTRAL_590' and
                                                     Read_line_array[28] =='SPECTRAL_600' and
                                                     Read_line_array[29] =='SPECTRAL_610' and
                                                     Read_line_array[30] =='SPECTRAL_620' and
                                                     Read_line_array[31] =='SPECTRAL_630' and
                                                     Read_line_array[32] =='SPECTRAL_640' and
                                                     Read_line_array[33] =='SPECTRAL_650' and
                                                     Read_line_array[34] =='SPECTRAL_660' and
                                                     Read_line_array[35] =='SPECTRAL_670' and
                                                     Read_line_array[36] =='SPECTRAL_680' and
                                                     Read_line_array[37] =='SPECTRAL_690'):
                                                        print "XCC Hot Folder: File Type 154 - 400 - 700 - CMYK"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SampleID' and
                                                     Read_line_array[1] =='SAMPLE_NAME' and
                                                     Read_line_array[2] =='RGB_R' and
                                                     Read_line_array[3] =='RGB_G' and
                                                     Read_line_array[4] =='RGB_B' and
                                                     Read_line_array[5] =='LAB_L' and
                                                     Read_line_array[6] =='LAB_A' and
                                                     Read_line_array[7] =='LAB_B' and
                                                     Read_line_array[8] =='nm380' and
                                                     Read_line_array[9] =='nm390' and
                                                     Read_line_array[10] =='nm400' and
                                                     Read_line_array[11] =='nm410' and
                                                     Read_line_array[12] =='nm420' and
                                                     Read_line_array[13] =='nm430' and
                                                     Read_line_array[14] =='nm440' and
                                                     Read_line_array[15] =='nm450' and
                                                     Read_line_array[16] =='nm460' and
                                                     Read_line_array[17] =='nm470' and
                                                     Read_line_array[18] =='nm480' and
                                                     Read_line_array[19] =='nm490' and
                                                     Read_line_array[20] =='nm500' and
                                                     Read_line_array[21] =='nm510' and
                                                     Read_line_array[22] =='nm520' and
                                                     Read_line_array[23] =='nm530' and
                                                     Read_line_array[24] =='nm540' and
                                                     Read_line_array[25] =='nm550' and
                                                     Read_line_array[26] =='nm560' and
                                                     Read_line_array[27] =='nm570' and
                                                     Read_line_array[28] =='nm580' and
                                                     Read_line_array[29] =='nm590' and
                                                     Read_line_array[30] =='nm600' and
                                                     Read_line_array[31] =='nm610' and
                                                     Read_line_array[32] =='nm620' and
                                                     Read_line_array[33] =='nm630' and
                                                     Read_line_array[34] =='nm640' and
                                                     Read_line_array[35] =='nm650' and
                                                     Read_line_array[36] =='nm660' and
                                                     Read_line_array[37] =='nm670' and
                                                     Read_line_array[38] =='nm680' and
                                                     Read_line_array[39] =='nm690' and
                                                     Read_line_array[40] =='nm700' and
                                                     Read_line_array[41] =='nm710' and
                                                     Read_line_array[42] =='nm720'):
                                                        print "XCC Hot Folder: File Type 203 - 380 - 730 - RGB"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SampleID' and
                                                     Read_line_array[1] =='SAMPLE_NAME' and
                                                     Read_line_array[2] =='RGB_R' and
                                                     Read_line_array[3] =='RGB_G' and
                                                     Read_line_array[4] =='RGB_B' and
                                                     Read_line_array[5] =='LAB_L' and
                                                     Read_line_array[6] =='LAB_A' and
                                                     Read_line_array[7] =='LAB_B' and
                                                     Read_line_array[8] =='nm400' and
                                                     Read_line_array[9] =='nm410' and
                                                     Read_line_array[10] =='nm420' and
                                                     Read_line_array[11] =='nm430' and
                                                     Read_line_array[12] =='nm440' and
                                                     Read_line_array[13] =='nm450' and
                                                     Read_line_array[14] =='nm460' and
                                                     Read_line_array[15] =='nm470' and
                                                     Read_line_array[16] =='nm480' and
                                                     Read_line_array[17] =='nm490' and
                                                     Read_line_array[18] =='nm500' and
                                                     Read_line_array[19] =='nm510' and
                                                     Read_line_array[20] =='nm520' and
                                                     Read_line_array[21] =='nm530' and
                                                     Read_line_array[22] =='nm540' and
                                                     Read_line_array[23] =='nm550' and
                                                     Read_line_array[24] =='nm560' and
                                                     Read_line_array[25] =='nm570' and
                                                     Read_line_array[26] =='nm580' and
                                                     Read_line_array[27] =='nm590' and
                                                     Read_line_array[28] =='nm600' and
                                                     Read_line_array[29] =='nm610' and
                                                     Read_line_array[30] =='nm620' and
                                                     Read_line_array[31] =='nm630' and
                                                     Read_line_array[32] =='nm640' and
                                                     Read_line_array[33] =='nm650' and
                                                     Read_line_array[34] =='nm660' and
                                                     Read_line_array[35] =='nm670' and
                                                     Read_line_array[36] =='nm680' and
                                                     Read_line_array[37] =='nm690'):
                                                        print "XCC Hot Folder: File Type 203 - 400 - 700 - RGB"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SAMPLE_ID' and
                                                     Read_line_array[1] =='RGB_R' and
                                                     Read_line_array[2] =='RGB_G' and
                                                     Read_line_array[3] =='RGB_B' and
                                                     Read_line_array[4] =='LAB_L' and
                                                     Read_line_array[5] =='LAB_A' and
                                                     Read_line_array[6] =='LAB_B' and
                                                     Read_line_array[7] =='SPECTRAL_400' and
                                                     Read_line_array[8] =='SPECTRAL_410' and
                                                     Read_line_array[9] =='SPECTRAL_420' and
                                                     Read_line_array[10] =='SPECTRAL_430' and
                                                     Read_line_array[11] =='SPECTRAL_440' and
                                                     Read_line_array[12] =='SPECTRAL_450' and
                                                     Read_line_array[13] =='SPECTRAL_460' and
                                                     Read_line_array[14] =='SPECTRAL_470' and
                                                     Read_line_array[15] =='SPECTRAL_480' and
                                                     Read_line_array[16] =='SPECTRAL_490' and
                                                     Read_line_array[17] =='SPECTRAL_500' and
                                                     Read_line_array[18] =='SPECTRAL_510' and
                                                     Read_line_array[19] =='SPECTRAL_520' and
                                                     Read_line_array[20] =='SPECTRAL_530' and
                                                     Read_line_array[21] =='SPECTRAL_540' and
                                                     Read_line_array[22] =='SPECTRAL_550' and
                                                     Read_line_array[23] =='SPECTRAL_560' and
                                                     Read_line_array[24] =='SPECTRAL_570' and
                                                     Read_line_array[25] =='SPECTRAL_580' and
                                                     Read_line_array[26] =='SPECTRAL_590' and
                                                     Read_line_array[27] =='SPECTRAL_600' and
                                                     Read_line_array[28] =='SPECTRAL_610' and
                                                     Read_line_array[29] =='SPECTRAL_620' and
                                                     Read_line_array[30] =='SPECTRAL_630' and
                                                     Read_line_array[31] =='SPECTRAL_640' and
                                                     Read_line_array[32] =='SPECTRAL_650' and
                                                     Read_line_array[33] =='SPECTRAL_660' and
                                                     Read_line_array[34] =='SPECTRAL_670' and
                                                     Read_line_array[35] =='SPECTRAL_680' and
                                                     Read_line_array[36] =='SPECTRAL_690'):
                                                        print "XCC Hot Folder: File Type 154 - 400 - 700 - RGB"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SAMPLE_ID' and
                                                     Read_line_array[1] =='RGB_R' and
                                                     Read_line_array[2] =='RGB_G' and
                                                     Read_line_array[3] =='RGB_B' and
                                                     Read_line_array[4] =='LAB_L' and
                                                     Read_line_array[5] =='LAB_A' and
                                                     Read_line_array[6] =='LAB_B' and
                                                     Read_line_array[7] =='SPECTRAL_380' and
                                                     Read_line_array[8] =='SPECTRAL_390' and
                                                     Read_line_array[9] =='SPECTRAL_400' and
                                                     Read_line_array[10] =='SPECTRAL_410' and
                                                     Read_line_array[11] =='SPECTRAL_420' and
                                                     Read_line_array[12] =='SPECTRAL_430' and
                                                     Read_line_array[13] =='SPECTRAL_440' and
                                                     Read_line_array[14] =='SPECTRAL_450' and
                                                     Read_line_array[15] =='SPECTRAL_460' and
                                                     Read_line_array[16] =='SPECTRAL_470' and
                                                     Read_line_array[17] =='SPECTRAL_480' and
                                                     Read_line_array[18] =='SPECTRAL_490' and
                                                     Read_line_array[19] =='SPECTRAL_500' and
                                                     Read_line_array[20] =='SPECTRAL_510' and
                                                     Read_line_array[21] =='SPECTRAL_520' and
                                                     Read_line_array[22] =='SPECTRAL_530' and
                                                     Read_line_array[23] =='SPECTRAL_540' and
                                                     Read_line_array[24] =='SPECTRAL_550' and
                                                     Read_line_array[25] =='SPECTRAL_560' and
                                                     Read_line_array[26] =='SPECTRAL_570' and
                                                     Read_line_array[27] =='SPECTRAL_580' and
                                                     Read_line_array[28] =='SPECTRAL_590' and
                                                     Read_line_array[29] =='SPECTRAL_600' and
                                                     Read_line_array[30] =='SPECTRAL_610' and
                                                     Read_line_array[31] =='SPECTRAL_620' and
                                                     Read_line_array[32] =='SPECTRAL_630' and
                                                     Read_line_array[33] =='SPECTRAL_640' and
                                                     Read_line_array[34] =='SPECTRAL_650' and
                                                     Read_line_array[35] =='SPECTRAL_660' and
                                                     Read_line_array[36] =='SPECTRAL_670' and
                                                     Read_line_array[37] =='SPECTRAL_680' and
                                                     Read_line_array[38] =='SPECTRAL_690' and
                                                     Read_line_array[39] =='SPECTRAL_700' and
                                                     Read_line_array[40] =='SPECTRAL_710' and
                                                     Read_line_array[41] =='SPECTRAL_720'):
                                                        print "XCC Hot Folder: File Type 154 - 380 - 730 - RGB"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
                                                elif(Read_line_array[0] =='SampleID' and
                                                     Read_line_array[1] =='SAMPLE_NAME' and
                                                     Read_line_array[2] =='CMYK_C' and
                                                     Read_line_array[3] =='CMYK_M' and
                                                     Read_line_array[4] =='CMYK_Y' and
                                                     Read_line_array[5] =='CMYK_K' and
                                                     Read_line_array[6] =='nm380' and
                                                     Read_line_array[7] =='nm390' and
                                                     Read_line_array[8] =='nm400' and
                                                     Read_line_array[9] =='nm410' and
                                                     Read_line_array[10] =='nm420' and
                                                     Read_line_array[11] =='nm430' and
                                                     Read_line_array[12] =='nm440' and
                                                     Read_line_array[13] =='nm450' and
                                                     Read_line_array[14] =='nm460' and
                                                     Read_line_array[15] =='nm470' and
                                                     Read_line_array[16] =='nm480' and
                                                     Read_line_array[17] =='nm490' and
                                                     Read_line_array[18] =='nm500' and
                                                     Read_line_array[19] =='nm510' and
                                                     Read_line_array[20] =='nm520' and
                                                     Read_line_array[21] =='nm530' and
                                                     Read_line_array[22] =='nm540' and
                                                     Read_line_array[23] =='nm550' and
                                                     Read_line_array[24] =='nm560' and
                                                     Read_line_array[25] =='nm570' and
                                                     Read_line_array[26] =='nm580' and
                                                     Read_line_array[27] =='nm590' and
                                                     Read_line_array[28] =='nm600' and
                                                     Read_line_array[29] =='nm610' and
                                                     Read_line_array[30] =='nm620' and
                                                     Read_line_array[31] =='nm630' and
                                                     Read_line_array[32] =='nm640' and
                                                     Read_line_array[33] =='nm650' and
                                                     Read_line_array[34] =='nm660' and
                                                     Read_line_array[35] =='nm670' and
                                                     Read_line_array[36] =='nm680' and
                                                     Read_line_array[37] =='nm690' and
                                                     Read_line_array[38] =='nm700' and
                                                     Read_line_array[39] =='nm710' and
                                                     Read_line_array[40] =='nm720' and
                                                     Read_line_array[41] =='nm730'):
                                                        print "XCC Hot Folder: File Type I1Profiler - 380 - 730 - CMYK"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
						elif(Read_line_array[0] =='SampleID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='5CLR_1' and
						     Read_line_array[3] =='5CLR_2' and
						     Read_line_array[4] =='5CLR_3' and
						     Read_line_array[5] =='5CLR_4' and
						     Read_line_array[6] =='5CLR_5' and
						     Read_line_array[7] =='nm380' and
						     Read_line_array[8] =='nm390' and
						     Read_line_array[9] =='nm400' and
						     Read_line_array[10] =='nm410' and
						     Read_line_array[11] =='nm420' and
						     Read_line_array[12] =='nm430' and
						     Read_line_array[13] =='nm440' and
						     Read_line_array[14] =='nm450' and
						     Read_line_array[15] =='nm460' and
						     Read_line_array[16] =='nm470' and
						     Read_line_array[17] =='nm480' and
						     Read_line_array[18] =='nm490' and
						     Read_line_array[19] =='nm500' and
						     Read_line_array[20] =='nm510' and
						     Read_line_array[21] =='nm520' and
						     Read_line_array[22] =='nm530' and
						     Read_line_array[23] =='nm540' and
						     Read_line_array[24] =='nm550' and
						     Read_line_array[25] =='nm560' and
						     Read_line_array[26] =='nm570' and
						     Read_line_array[27] =='nm580' and
						     Read_line_array[28] =='nm590' and
						     Read_line_array[29] =='nm600' and
						     Read_line_array[30] =='nm610' and
						     Read_line_array[31] =='nm620' and
						     Read_line_array[32] =='nm630' and
						     Read_line_array[33] =='nm640' and
						     Read_line_array[34] =='nm650' and
						     Read_line_array[35] =='nm660' and
						     Read_line_array[36] =='nm670' and
						     Read_line_array[37] =='nm680' and
						     Read_line_array[38] =='nm690' and
						     Read_line_array[39] =='nm700' and
						     Read_line_array[40] =='nm710' and
						     Read_line_array[41] =='nm720' and
						     Read_line_array[42] =='nm730'):
							print "XCC Hot Folder: File Type I1Profiler - 380 - 730 - 5Color"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr						
						elif(Read_line_array[0] =='SAMPLE_ID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='CMYK_C' and
						     Read_line_array[3] =='CMYK_M' and
						     Read_line_array[4] =='CMYK_Y' and
						     Read_line_array[5] =='CMYK_K' and
						     Read_line_array[6] =='SPECTRAL_NM380' and
						     Read_line_array[7] =='SPECTRAL_NM390' and
						     Read_line_array[8] =='SPECTRAL_NM400' and
						     Read_line_array[9] =='SPECTRAL_NM410' and
						     Read_line_array[10] =='SPECTRAL_NM420' and
						     Read_line_array[11] =='SPECTRAL_NM430' and
						     Read_line_array[12] =='SPECTRAL_NM440' and
						     Read_line_array[13] =='SPECTRAL_NM450' and
						     Read_line_array[14] =='SPECTRAL_NM460' and
						     Read_line_array[15] =='SPECTRAL_NM470' and
						     Read_line_array[16] =='SPECTRAL_NM480' and
						     Read_line_array[17] =='SPECTRAL_NM490' and
						     Read_line_array[18] =='SPECTRAL_NM500' and
						     Read_line_array[19] =='SPECTRAL_NM510' and
						     Read_line_array[20] =='SPECTRAL_NM520' and
						     Read_line_array[21] =='SPECTRAL_NM530' and
						     Read_line_array[22] =='SPECTRAL_NM540' and
						     Read_line_array[23] =='SPECTRAL_NM550' and
						     Read_line_array[24] =='SPECTRAL_NM560' and
						     Read_line_array[25] =='SPECTRAL_NM570' and
						     Read_line_array[26] =='SPECTRAL_NM580' and
						     Read_line_array[27] =='SPECTRAL_NM590' and
						     Read_line_array[28] =='SPECTRAL_NM600' and
						     Read_line_array[29] =='SPECTRAL_NM610' and
						     Read_line_array[30] =='SPECTRAL_NM620' and
						     Read_line_array[31] =='SPECTRAL_NM630' and
						     Read_line_array[32] =='SPECTRAL_NM640' and
						     Read_line_array[33] =='SPECTRAL_NM650' and
						     Read_line_array[34] =='SPECTRAL_NM660' and
						     Read_line_array[35] =='SPECTRAL_NM670' and
						     Read_line_array[36] =='SPECTRAL_NM680' and
						     Read_line_array[37] =='SPECTRAL_NM690' and
						     Read_line_array[38] =='SPECTRAL_NM700' and
						     Read_line_array[39] =='SPECTRAL_NM710' and
						     Read_line_array[40] =='SPECTRAL_NM720' and
						     Read_line_array[41] =='SPECTRAL_NM730'):
							print "XCC Hot Folder: File Type I1Profiler new - 380 - 730 - CMYK"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr  
						elif(Read_line_array[0] =='SAMPLE_ID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='5CLR_1' and
						     Read_line_array[3] =='5CLR_2' and
						     Read_line_array[4] =='5CLR_3' and
						     Read_line_array[5] =='5CLR_4' and
						     Read_line_array[6] =='5CLR_5' and
						     Read_line_array[7] =='SPECTRAL_NM380' and
						     Read_line_array[8] =='SPECTRAL_NM390' and
						     Read_line_array[9] =='SPECTRAL_NM400' and
						     Read_line_array[10] =='SPECTRAL_NM410' and
						     Read_line_array[11] =='SPECTRAL_NM420' and
						     Read_line_array[12] =='SPECTRAL_NM430' and
						     Read_line_array[13] =='SPECTRAL_NM440' and
						     Read_line_array[14] =='SPECTRAL_NM450' and
						     Read_line_array[15] =='SPECTRAL_NM460' and
						     Read_line_array[16] =='SPECTRAL_NM470' and
						     Read_line_array[17] =='SPECTRAL_NM480' and
						     Read_line_array[18] =='SPECTRAL_NM490' and
						     Read_line_array[19] =='SPECTRAL_NM500' and
						     Read_line_array[20] =='SPECTRAL_NM510' and
						     Read_line_array[21] =='SPECTRAL_NM520' and
						     Read_line_array[22] =='SPECTRAL_NM530' and
						     Read_line_array[23] =='SPECTRAL_NM540' and
						     Read_line_array[24] =='SPECTRAL_NM550' and
						     Read_line_array[25] =='SPECTRAL_NM560' and
						     Read_line_array[26] =='SPECTRAL_NM570' and
						     Read_line_array[27] =='SPECTRAL_NM580' and
						     Read_line_array[28] =='SPECTRAL_NM590' and
						     Read_line_array[29] =='SPECTRAL_NM600' and
						     Read_line_array[30] =='SPECTRAL_NM610' and
						     Read_line_array[31] =='SPECTRAL_NM620' and
						     Read_line_array[32] =='SPECTRAL_NM630' and
						     Read_line_array[33] =='SPECTRAL_NM640' and
						     Read_line_array[34] =='SPECTRAL_NM650' and
						     Read_line_array[35] =='SPECTRAL_NM660' and
						     Read_line_array[36] =='SPECTRAL_NM670' and
						     Read_line_array[37] =='SPECTRAL_NM680' and
						     Read_line_array[38] =='SPECTRAL_NM690' and
						     Read_line_array[39] =='SPECTRAL_NM700' and
						     Read_line_array[40] =='SPECTRAL_NM710' and
						     Read_line_array[41] =='SPECTRAL_NM720' and
						     Read_line_array[42] =='SPECTRAL_NM730'):
							print "XCC Hot Folder: File Type I1Profiler new - 380 - 730 - 5 Color"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr
						elif(Read_line_array[0] =='SAMPLE_ID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='6CLR_1' and
						     Read_line_array[3] =='6CLR_2' and
						     Read_line_array[4] =='6CLR_3' and
						     Read_line_array[5] =='6CLR_4' and
						     Read_line_array[6] =='6CLR_5' and
						     Read_line_array[7] =='6CLR_6' and
						     Read_line_array[8] =='SPECTRAL_NM380' and
						     Read_line_array[9] =='SPECTRAL_NM390' and
						     Read_line_array[10] =='SPECTRAL_NM400' and
						     Read_line_array[11] =='SPECTRAL_NM410' and
						     Read_line_array[12] =='SPECTRAL_NM420' and
						     Read_line_array[13] =='SPECTRAL_NM430' and
						     Read_line_array[14] =='SPECTRAL_NM440' and
						     Read_line_array[15] =='SPECTRAL_NM450' and
						     Read_line_array[16] =='SPECTRAL_NM460' and
						     Read_line_array[17] =='SPECTRAL_NM470' and
						     Read_line_array[18] =='SPECTRAL_NM480' and
						     Read_line_array[19] =='SPECTRAL_NM490' and
						     Read_line_array[20] =='SPECTRAL_NM500' and
						     Read_line_array[21] =='SPECTRAL_NM510' and
						     Read_line_array[22] =='SPECTRAL_NM520' and
						     Read_line_array[23] =='SPECTRAL_NM530' and
						     Read_line_array[24] =='SPECTRAL_NM540' and
						     Read_line_array[25] =='SPECTRAL_NM550' and
						     Read_line_array[26] =='SPECTRAL_NM560' and
						     Read_line_array[27] =='SPECTRAL_NM570' and
						     Read_line_array[28] =='SPECTRAL_NM580' and
						     Read_line_array[29] =='SPECTRAL_NM590' and
						     Read_line_array[30] =='SPECTRAL_NM600' and
						     Read_line_array[31] =='SPECTRAL_NM610' and
						     Read_line_array[32] =='SPECTRAL_NM620' and
						     Read_line_array[33] =='SPECTRAL_NM630' and
						     Read_line_array[34] =='SPECTRAL_NM640' and
						     Read_line_array[35] =='SPECTRAL_NM650' and
						     Read_line_array[36] =='SPECTRAL_NM660' and
						     Read_line_array[37] =='SPECTRAL_NM670' and
						     Read_line_array[38] =='SPECTRAL_NM680' and
						     Read_line_array[39] =='SPECTRAL_NM690' and
						     Read_line_array[40] =='SPECTRAL_NM700' and
						     Read_line_array[41] =='SPECTRAL_NM710' and
						     Read_line_array[42] =='SPECTRAL_NM720' and
						     Read_line_array[43] =='SPECTRAL_NM730'):
							print "XCC Hot Folder: File Type I1Profiler new - 380 - 730 - 6 Color"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr
						elif(Read_line_array[0] =='SAMPLE_ID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='7CLR_1' and
						     Read_line_array[3] =='7CLR_2' and
						     Read_line_array[4] =='7CLR_3' and
						     Read_line_array[5] =='7CLR_4' and
						     Read_line_array[6] =='7CLR_5' and
						     Read_line_array[7] =='7CLR_6' and
						     Read_line_array[8] =='7CLR_7' and
						     Read_line_array[9] =='SPECTRAL_NM380' and
						     Read_line_array[10] =='SPECTRAL_NM390' and
						     Read_line_array[11] =='SPECTRAL_NM400' and
						     Read_line_array[12] =='SPECTRAL_NM410' and
						     Read_line_array[13] =='SPECTRAL_NM420' and
						     Read_line_array[14] =='SPECTRAL_NM430' and
						     Read_line_array[15] =='SPECTRAL_NM440' and
						     Read_line_array[16] =='SPECTRAL_NM450' and
						     Read_line_array[17] =='SPECTRAL_NM460' and
						     Read_line_array[18] =='SPECTRAL_NM470' and
						     Read_line_array[19] =='SPECTRAL_NM480' and
						     Read_line_array[20] =='SPECTRAL_NM490' and
						     Read_line_array[21] =='SPECTRAL_NM500' and
						     Read_line_array[22] =='SPECTRAL_NM510' and
						     Read_line_array[23] =='SPECTRAL_NM520' and
						     Read_line_array[24] =='SPECTRAL_NM530' and
						     Read_line_array[25] =='SPECTRAL_NM540' and
						     Read_line_array[26] =='SPECTRAL_NM550' and
						     Read_line_array[27] =='SPECTRAL_NM560' and
						     Read_line_array[28] =='SPECTRAL_NM570' and
						     Read_line_array[29] =='SPECTRAL_NM580' and
						     Read_line_array[30] =='SPECTRAL_NM590' and
						     Read_line_array[31] =='SPECTRAL_NM600' and
						     Read_line_array[32] =='SPECTRAL_NM610' and
						     Read_line_array[33] =='SPECTRAL_NM620' and
						     Read_line_array[34] =='SPECTRAL_NM630' and
						     Read_line_array[35] =='SPECTRAL_NM640' and
						     Read_line_array[36] =='SPECTRAL_NM650' and
						     Read_line_array[37] =='SPECTRAL_NM660' and
						     Read_line_array[38] =='SPECTRAL_NM670' and
						     Read_line_array[39] =='SPECTRAL_NM680' and
						     Read_line_array[40] =='SPECTRAL_NM690' and
						     Read_line_array[41] =='SPECTRAL_NM700' and
						     Read_line_array[42] =='SPECTRAL_NM710' and
						     Read_line_array[43] =='SPECTRAL_NM720' and
						     Read_line_array[44] =='SPECTRAL_NM730'):
							print "XCC Hot Folder: File Type I1Profiler new - 380 - 730 - 7 Color"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr						
						elif(Read_line_array[0] =='SampleID' and
                                                     Read_line_array[1] =='SAMPLE_NAME' and
                                                     Read_line_array[2] =='RGB_R' and
                                                     Read_line_array[3] =='RGB_G' and
                                                     Read_line_array[4] =='RGB_B' and
                                                     Read_line_array[5] =='nm380' and
                                                     Read_line_array[6] =='nm390' and
                                                     Read_line_array[7] =='nm400' and
                                                     Read_line_array[8] =='nm410' and
                                                     Read_line_array[9] =='nm420' and
                                                     Read_line_array[10] =='nm430' and
                                                     Read_line_array[11] =='nm440' and
                                                     Read_line_array[12] =='nm450' and
                                                     Read_line_array[13] =='nm460' and
                                                     Read_line_array[14] =='nm470' and
                                                     Read_line_array[15] =='nm480' and
                                                     Read_line_array[16] =='nm490' and
                                                     Read_line_array[17] =='nm500' and
                                                     Read_line_array[18] =='nm510' and
                                                     Read_line_array[19] =='nm520' and
                                                     Read_line_array[20] =='nm530' and
                                                     Read_line_array[21] =='nm540' and
                                                     Read_line_array[22] =='nm550' and
                                                     Read_line_array[23] =='nm560' and
                                                     Read_line_array[24] =='nm570' and
                                                     Read_line_array[25] =='nm580' and
                                                     Read_line_array[26] =='nm590' and
                                                     Read_line_array[27] =='nm600' and
                                                     Read_line_array[28] =='nm610' and
                                                     Read_line_array[29] =='nm620' and
                                                     Read_line_array[30] =='nm630' and
                                                     Read_line_array[31] =='nm640' and
                                                     Read_line_array[32] =='nm650' and
                                                     Read_line_array[33] =='nm660' and
                                                     Read_line_array[34] =='nm670' and
                                                     Read_line_array[35] =='nm680' and
                                                     Read_line_array[36] =='nm690' and
                                                     Read_line_array[37] =='nm700' and
                                                     Read_line_array[38] =='nm710' and
                                                     Read_line_array[39] =='nm720' and
                                                     Read_line_array[40] =='nm730'):
                                                        print "XCC Hot Folder: File Type I1Profiler - 380 - 730 - RGB"
                                                        Correct_cgates=1
                                                        line_nr=line_nr+max_lines_nr
						elif(Read_line_array[0] =='SAMPLE_ID' and
						     Read_line_array[1] =='SAMPLE_NAME' and
						     Read_line_array[2] =='RGB_R' and
						     Read_line_array[3] =='RGB_G' and
						     Read_line_array[4] =='RGB_B' and
						     Read_line_array[5] =='SPECTRAL_NM380' and
						     Read_line_array[6] =='SPECTRAL_NM390' and
						     Read_line_array[7] =='SPECTRAL_NM400' and
						     Read_line_array[8] =='SPECTRAL_NM410' and
						     Read_line_array[9] =='SPECTRAL_NM420' and
						     Read_line_array[10] =='SPECTRAL_NM430' and
						     Read_line_array[11] =='SPECTRAL_NM440' and
						     Read_line_array[12] =='SPECTRAL_NM450' and
						     Read_line_array[13] =='SPECTRAL_NM460' and
						     Read_line_array[14] =='SPECTRAL_NM470' and
						     Read_line_array[15] =='SPECTRAL_NM480' and
						     Read_line_array[16] =='SPECTRAL_NM490' and
						     Read_line_array[17] =='SPECTRAL_NM500' and
						     Read_line_array[18] =='SPECTRAL_NM510' and
						     Read_line_array[19] =='SPECTRAL_NM520' and
						     Read_line_array[20] =='SPECTRAL_NM530' and
						     Read_line_array[21] =='SPECTRAL_NM540' and
						     Read_line_array[22] =='SPECTRAL_NM550' and
						     Read_line_array[23] =='SPECTRAL_NM560' and
						     Read_line_array[24] =='SPECTRAL_NM570' and
						     Read_line_array[25] =='SPECTRAL_NM580' and
						     Read_line_array[26] =='SPECTRAL_NM590' and
						     Read_line_array[27] =='SPECTRAL_NM600' and
						     Read_line_array[28] =='SPECTRAL_NM610' and
						     Read_line_array[29] =='SPECTRAL_NM620' and
						     Read_line_array[30] =='SPECTRAL_NM630' and
						     Read_line_array[31] =='SPECTRAL_NM640' and
						     Read_line_array[32] =='SPECTRAL_NM650' and
						     Read_line_array[33] =='SPECTRAL_NM660' and
						     Read_line_array[34] =='SPECTRAL_NM670' and
						     Read_line_array[35] =='SPECTRAL_NM680' and
						     Read_line_array[36] =='SPECTRAL_NM690' and
						     Read_line_array[37] =='SPECTRAL_NM700' and
						     Read_line_array[38] =='SPECTRAL_NM710' and
						     Read_line_array[39] =='SPECTRAL_NM720' and
						     Read_line_array[40] =='SPECTRAL_NM730'):
							print "XCC Hot Folder: File Type I1Profiler new - 380 - 730 - RGB"
							Correct_cgates=1
							line_nr=line_nr+max_lines_nr							
                                                line_nr=line_nr+1
                        
                                        if line_nr>=max_lines_nr:
                                                fp.close()
                                                if Correct_cgates==1:
                                                        Upload_Cgats(file_path,the_file)
                                                else:
                                                        Error_Wrong_File(file_path,the_file)
                                
                                                        
                        
                        
                        
                except:
			
			fp.close()
			print "XCC Hot Folder: File Path %s"%file_path
			print "XCC Hot Folder: File %s"%the_file			
                        Error_Wrong_File(file_path,the_file)    
                
                
def Upload_Cgats(file_path,the_file):
	
        print "XCC Hot Folder: Upload Cgats"
        print "XCC Hot Folder: File Path= %s"%file_path
	global seconds
	if(proxy =="True"):
		proxy_handeler = urllib2.ProxyHandler({'http':'%s:%s'% proxysetting})
	else:
		proxy_handeler = urllib2.ProxyHandler({})
	opener_proxy = urllib2.build_opener(proxy_handeler)	
	get_Post_URL= urllib2.Request("http://"+Agent_Config.Use_URL+"."+Agent_Config.Use_Domain+"/autoflow/Agent_Post_url.php")
			
	read_Post_URL = opener_proxy.open(get_Post_URL)
	Post_URL = json.load(read_Post_URL)
	print Post_URL['Post_URL']	
	
        import MultipartPostHandler
        import base64
        write_log('XCC Hot Folder: Upload Cgats '+the_file)
               
        with open("%s" % (file_path), "r") as Cgats_file:
                Cgats_data=Cgats_file.read()
                
        encoded_string = base64.b64encode(Cgats_data)
       
       
        Filter ='NA'
	File_amount = 0
	if the_file.endswith('_M0.txt') or the_file.endswith('_M1.txt') or the_file.endswith('_M2.txt'):
		if the_file.endswith('_M0.txt'):
			Filter='M0'
		elif the_file.endswith('_M1.txt'):
			Filter='M1'
		else:
			Filter='M2'
			
		File_amount+=File_Collection[the_file[0:-7]+'_M0.txt']
		File_amount+=File_Collection[the_file[0:-7]+'_M1.txt']
		File_amount+=File_Collection[the_file[0:-7]+'_M2.txt']
       
       
       
        params = {'file_data':encoded_string,
	          'Measure_Filter': Filter,
	          'File_amount':File_amount}
        
        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request("http://"+Post_URL['Post_URL']+"."+Agent_Config.Use_Domain+"/autoflow/autoflow_upload_Cgats.php", params)
        if(proxy =="True"):
		req.set_proxy('%s:%s'% proxysetting, 'http')
        print "XCC Hot Folder: Start File result to XCC"
	write_log('XCC Hot Folder: Start File result to XCC')	    
	try:
		response = opener.open(req, timeout=90).read().strip()
		Result_upload = json.loads(response)
	except urllib2.URLError as e:    
		print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
		write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)
		time.sleep(5)
		print "XCC Hot Folder: Try again start forward File result to XCC"
		write_log('XCC Hot Folder: Try again start forward File result to XCC')
		try:
			response = opener.open(req, timeout=90).read().strip()
			Result_upload = json.loads(response)
		except urllib2.URLError as e:    
			print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)
			time.sleep(5)
			print "XCC Hot Folder: Try again start forward File result to XCC"
			write_log('XCC Hot Folder: Try again start forward File result to XCC')
			try:
				response = opener.open(req, timeout=90).read().strip()
				Result_upload = json.loads(response)
			except urllib2.URLError as e:    
				print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)										    			
				Result_upload = {'Result':'Error sent to XCC'}
			except socket.timeout:
				print "XCC Hot Folder: Timeout error when sent to XCC"
				write_log('XCC Hot Folder: Timeout error when sent to XCC')							    				    
				Result_upload = {'Result':'Error sent to XCC'}
		except socket.timeout:		
			print "XCC Hot Folder: Timeout error when sent to XCC"
			write_log('XCC Hot Folder: Timeout error when sent to XCC')
			time.sleep(5)
			print "XCC Hot Folder: Try again start forward File result to XCC"
			write_log('XCC Hot Folder: Try again start forward File result to XCC') 		
			try:
				response = opener.open(req, timeout=90).read().strip()
				Result_upload = json.loads(response)
			except urllib2.URLError as e:    
				print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)										    			
				Result_upload = {'Result':'Error sent to XCC'}
			except socket.timeout:
				print "XCC Hot Folder: Timeout error when sent to XCC"
				write_log('XCC Hot Folder: Timeout error when sent to XCC')
				Result_upload = {'Result':'Error sent to XCC'}
	except socket.timeout:
		print "XCC Hot Folder: Timeout error when sent to XCC"
		write_log('XCC Hot Folder: Timeout error when sent to XCC')
		time.sleep(5)
		print "XCC Hot Folder: Try again start forward File result to XCC"
		write_log('XCC Hot Folder: Try again start forward File result to XCC')   
		try:
			response = opener.open(req, timeout=90).read().strip()
			Result_upload = json.loads(response)
		except urllib2.URLError as e:    
			print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
			write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)
			time.sleep(5)
			print "XCC Hot Folder: Try again start forward File result to XCC"
			write_log('XCC Hot Folder: Try again start forward File result to XCC')
			try:
				response = opener.open(req, timeout=90).read().strip()
				Result_upload = json.loads(response)
			except urllib2.URLError as e:    
				print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)
				Result_upload = {'Result':'Error sent to XCC'}
			except socket.timeout:
				print "XCC Hot Folder: Timeout error when sent to XCC"
				write_log('XCC Hot Folder: Timeout error when sent to XCC')				    
				Result_upload = {'Result':'Error sent to XCC'}
		except socket.timeout:
			print "XCC Hot Folder: Timeout error when sent to XCC"
			write_log('XCC Hot Folder: Timeout error when sent to XCC')
			time.sleep(5)
			print "XCC Hot Folder: Try again start forward File result to XCC"
			write_log('XCC Hot Folder: Try again start forward File result to XCC') 		
			try:
				response = opener.open(req, timeout=90).read().strip()
				Result_upload = json.loads(response)
			except urllib2.URLError as e:    
				print "XCC Hot Folder: Error when sent to XCC (%s) " % e.reason
				write_log('XCC Hot Folder: Error when sent to XCC (%s) ' % e.reason)										    			
				Result_upload = {'Result':'Error sent to XCC'}
			except socket.timeout:
				print "XCC Hot Folder: Timeout error when sent to XCC"
				write_log('XCC Hot Folder: Timeout error when sent to XCC')							    			
				Result_upload = {'Result':'Error sent to XCC'}	
        
	import shutil
	the_file2=time.strftime("%d%b%Y_%H-%M-%S")+'_'+the_file	
	print "XCC Hot Folder: %s"%Result_upload['Result']
	if(Result_upload['Result']==1):# oke
		
		print "XCC Hot Folder: File %s"%the_file   
		write_log('XCC Hot Folder: Correct Cgats '+the_file)
		shutil.move(file_path,os.path.join(Agent_Config.APP_HOTFOLDER_PATH_PROCESSED,the_file2))
		
		seconds = 8		
		Show_msg(Result_upload['Result_msg'])		
	elif(Result_upload['Result']==5):# not correct filter 
		print "XCC Hot Folder: Not Correct Filter Cgats %s"%the_file   
		write_log('XCC Hot Folder: Not Correct Filter Cgats '+the_file)
		shutil.move(file_path,os.path.join(Agent_Config.APP_HOTFOLDER_PATH_ERROR,the_file2))
	
	else:
		write_log('XCC Hot Folder: Upload Cgats Error '+the_file)
		the_file_error=time.strftime("%d%b%Y_%H-%M-%S")+'_Error_'+the_file+'.txt'
		output = open("%s/%s" % (Agent_Config.APP_HOTFOLDER_PATH_ERROR,the_file_error),"wb")
		output.write(Result_upload['Result_msg'])
		output.close()		
		
		
		shutil.move(file_path,os.path.join(Agent_Config.APP_HOTFOLDER_PATH_ERROR,the_file2))
		
		seconds = 1800
		Show_msg(Result_upload['Result_msg'])		
        
def Error_Wrong_File(file_path,the_file):                 
        write_log('XCC Hot Folder: Not supported file '+the_file)
        import shutil
        the_file=time.strftime("%d%b%Y_%H-%M-%S")+'_'+the_file
        print "XCC Hot Folder: Not supported file %s"%the_file
	shutil.move(file_path,os.path.join(Agent_Config.APP_HOTFOLDER_PATH_ERROR,the_file))
	
	global seconds
	seconds = 1800
        Show_msg('<font color="red"><b>Not supported file!</b></font>')
        
        
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
        
write_log('XCC Hot Folder: Start XCC Agent Version %s' % Agent_Config.XCC_Agent_Version)
print "XCC Hot Folder: Start XCC Agent Version %s" % Agent_Config.XCC_Agent_Version
global File_Collection 
File_Collection= collections.Counter()
run=0
run_max=100
while (run < run_max):
        if not os.path.exists(Agent_Config.APP_XCC_Agent_PATH):
		os.mkdir(Agent_Config.APP_XCC_Agent_PATH)
        if not os.path.exists(Agent_Config.APP_HOTFOLDER_PATH):
                os.mkdir(Agent_Config.APP_HOTFOLDER_PATH)  
                        
        if not os.path.exists(Agent_Config.APP_HOTFOLDER_PATH_IN):
                os.mkdir(Agent_Config.APP_HOTFOLDER_PATH_IN)
        if not os.path.exists(Agent_Config.APP_HOTFOLDER_PATH_PROCESSED):
                os.mkdir(Agent_Config.APP_HOTFOLDER_PATH_PROCESSED)  
        if not os.path.exists(Agent_Config.APP_HOTFOLDER_PATH_ERROR):
                os.mkdir(Agent_Config.APP_HOTFOLDER_PATH_ERROR)   
                
        if os.listdir(Agent_Config.APP_HOTFOLDER_PATH_IN) != []:
                print os.listdir(Agent_Config.APP_HOTFOLDER_PATH_IN)
                Read_files_in_hotfolder(File_Collection)               
        else:
                time.sleep(5)		
		File_Collection= collections.Counter()	
        print "XCC Hot Folder: Running"
	