import sys
#sys.path.append("E:\Python27\Lib")
import os
import StringIO
import traceback
import time
import struct
import re
import shutil
import difflib
import datetime
import csv
import getopt
import array
import math

#just for bpp such as 16 and 24 those which can be divided by 8

####################################################
# Usgae print
####################################################
def usage():
	print('Usage: python replace_image_data.py')
	

####################################################
# Usgae print
####################################################
class ByteUtil:	
	@staticmethod
	def writeToOutputStream(outputStream, byteArray, width, height, depth):
	
		totalBytes = len(byteArray)
		
		headFlag = False
		
		outputStream.write('{\n')
		
		print totalBytes
		print "width, height, depth: %d, %d, %d" % (width, height, depth)

		
		dummynumber = 4 - width*depth%4
		print "dummy number: %d" % dummynumber
		
		byteinline = width*depth+dummynumber
		print "bytes in line: %d" % byteinline
		
		byteIndex = 0
		
		for lineindex in range(height-1, -1, -1):
			for byteindex in range(0, byteinline):
				byteIndex += 1
				if byteindex < width*depth:
					hexStr = '0x%02X' % (byteArray[lineindex*byteinline+byteindex])
					outputStream.write(hexStr)
					
					if(byteIndex != totalBytes):
						outputStream.write(', ')
						
				if(headFlag == False) and (byteIndex == 7):
					outputStream.write('\n')
					headFlag = True
				elif((byteIndex - 8) % 16 == 15):
					outputStream.write('\n')
		
		#for byteIndex in range(totalBytes - 1, -1, -3):
			#print byteIndex
			#hexStr = '0x%02X' % (byteArray[byteIndex-2])
			#outputStream.write(hexStr)
			#if(byteIndex != totalBytes):
				#outputStream.write(', ')
			#hexStr = '0x%02X' % (byteArray[byteIndex-1])
			#outputStream.write(hexStr)
			#if(byteIndex != totalBytes):
				#outputStream.write(', ')
			#hexStr = '0x%02X' % (byteArray[byteIndex])
			#outputStream.write(hexStr)
			#if(byteIndex != totalBytes):
				#outputStream.write(', ')
		#for byteIndex in range(0,totalBytes):
			#hexStr = '0x%02X' % (byteArray[byteIndex])
			#outputStream.write(hexStr)
			#if(byteIndex != totalBytes):
				#outputStream.write(', ')
			#if(headFlag == False) and (byteIndex == 7):
                                #outputStream.write('\n')
                                #headFlag = True
                        #elif((byteIndex - 8) % 16 == 15):
				#outputStream.write('\n')
		outputStream.write('\n};')

	@staticmethod
	def readFile(fileName):
	
		print('Read data from ' + fileName)
		
		headData = array.array('B')
		rawData = array.array('B')

		inputStream = open(fileName,'rb')
		
		headData.fromfile(inputStream, 54)
		
		filelength = (headData[5]<<24) + (headData[4]<<16) + (headData[3]<<8) + headData[2]
		dataoffset = (headData[13]<<24) + (headData[12]<<16) + (headData[11]<<8) + headData[10]
		width = (headData[21]<<24) + (headData[20]<<16) + (headData[19]<<8) + headData[18]
		height = (headData[25]<<24) + (headData[24]<<16) + (headData[23]<<8) + headData[22]
		depth = ((headData[29]<<8) + headData[28])/8
		print("file lengh = %d" % filelength)
		print("file offset = %d" % dataoffset)
		print("width = %d" % width)
		print("height = %d" % height)
		print("depth = %d" % depth)

		rawData.fromfile(inputStream, filelength - dataoffset)
		
		inputStream.close()
		return rawData, width, height, depth

####################################################
# Module Entry
####################################################
# Check if the file is being run as a top-level program file before 
# invoke main method
if __name__ == '__main__':
	result = 0
	paddingSize = 0
	inputFile = ''
	inputData = ''
	outputFile = ''
	outputData = 'd'

	if(len(sys.argv)<1):
		usage()
		result = 1
	try:
		#Parse command line parameter
		opts, args = getopt.getopt(sys.argv[1:], 'i:')
		
		for o, a in opts:
			if o == '-i':
				path = a
				print path
				
				list = os.listdir(path)
				print list
				
				for inputFile in list:
					_,filetype = os.path.splitext(inputFile) 
					if filetype == ".bmp":
						inputFile = os.path.join(path,inputFile)
						print inputFile
						
						outputFile = inputFile + ".txt"
						print outputFile
						
						inputData, width, height, depth = ByteUtil.readFile(inputFile)
						outputData = open(outputFile, 'w')
						
						ByteUtil.writeToOutputStream(outputData,inputData, width, height, depth)
						
						outputData.close()
		result = 0
		
	except getopt.GetoptError, err:
		usage()
		result = 1	
	except:
		result = 1
		print '\n', '-'*20, "python exception start", '-'*20
		traceback.print_exc(file=sys.stdout)
		print '-'*20, "python exception  end ", '-'*20
		raise
	finally:
		sys.exit(result)
####################################################
