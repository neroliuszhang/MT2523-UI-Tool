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

####################################################
# Usgae print
####################################################
def usage():
	print('Usage: python UI Tool.py')
	

####################################################
# Usgae print
####################################################
class ByteUtil:	
	@staticmethod
	def writeToOutputStream(outputStream, byteArray):
		totalBytes = len(byteArray)
		headFlag = False
		outputStream.write('{\n')
		print totalBytes
		for byteIndex in range(totalBytes - 1, -1, -3):
			#print byteIndex
			hexStr = '0x%02X' % (byteArray[byteIndex-2])
			outputStream.write(hexStr)
			if(byteIndex != totalBytes):
				outputStream.write(', ')
			hexStr = '0x%02X' % (byteArray[byteIndex-1])
			outputStream.write(hexStr)
			if(byteIndex != totalBytes):
				outputStream.write(', ')
			hexStr = '0x%02X' % (byteArray[byteIndex])
			outputStream.write(hexStr)
			if(byteIndex != totalBytes):
				outputStream.write(', ')
			if(headFlag == False) and (byteIndex == 7):
                                outputStream.write('\n')
                                headFlag = True
                        elif((byteIndex - 8) % 16 == 15):
				outputStream.write('\n')
		outputStream.write('\n};')

	@staticmethod
	def readFile(fileName):
		print('Read data from ' + fileName)
		headData = array.array('B')
		restheadData = array.array('B')
		rawData = array.array('B')
		#original_size = os.path.getsize(fileName)
		inputStream = open(fileName,'rb')
		headData.fromfile(inputStream, 14)
		filelength = (headData[5]<<24) + (headData[4]<<16) + (headData[3]<<8) + headData[2]
		dataoffset = (headData[13]<<24) + (headData[12]<<16) + (headData[11]<<8) + headData[10]
		print("file lengh = %d" % filelength)
		print("file offset = %d" % dataoffset)
		restheadData.fromfile(inputStream, dataoffset - 14)
		rawData.fromfile(inputStream, filelength - dataoffset)
		print rawData[0:10]
		
		inputStream.close()
		return rawData

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
						inputData = ByteUtil.readFile(inputFile)
						outputData = open(outputFile, 'w')
						ByteUtil.writeToOutputStream(outputData,inputData)
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
