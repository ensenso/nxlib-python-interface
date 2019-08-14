# -*- coding: utf-8 -*-

from ctypes import *
import cv2
import numpy as np

import time
import os
import re

NxLibItemSeparator = '/'
NxLibIndexEscapeChar = '\\'
NxLibItemForbiddenChars = "/\\\\r\n\0"

NxLibItemTypeInvalid = 0
NxLibItemTypeNull    = 1
NxLibItemTypeNumber  = 2
NxLibItemTypeString  = 3
NxLibItemTypeBool    = 4
NxLibItemTypeArray   = 5
NxLibItemTypeObject  = 6


NxLibOperationSucceeded              = 0
NxLibCannotCreateItem                = 1
NxLibCouldNotInterpretJsonText       = 2
NxLibItemInexistent                  = 3
NxLibCouldNotOpenPort                = 6
NxLibInternalError                   = 7
NxLibTimeout                         = 8
NxLibNotConnected                    = 9
NxLibItemTypeNotCompatible           = 13
NxLibBufferTooSmall                  = 15
NxLibBufferNotDivisibleByElementSize = 16
NxLibExecutionFailed                 = 17
NxLibDebugMessageOverflow            = 18
NxLibNoDebugData                     = 5
NxLibInvalidBufferSize               = 14
NxLibMethodInvalid                   = 10
NxLibBadRequest                      = 11
NxLibConnectionNotCompatible         = 22
NxLibInitializationNotAllowed        = 23
NxLibNestingLimitReached             = 24
NxLibNoOpenProfileBlock              = 25

NxErrors = ["NxLibOperationSucceeded",
"NxLibCannotCreateItem",
"NxLibCouldNotInterpretJsonText",
"NxLibItemInexistent",
"",
"NxLibNoDebugData",
"NxLibCouldNotOpenPort",
"NxLibInternalError",
"NxLibTimeout",
"NxLibNotConnected",
"NxLibMethodInvalid",
"NxLibBadRequest",
"",
"NxLibItemTypeNotCompatible",
"NxLibInvalidBufferSize",
"NxLibBufferTooSmall",
"NxLibBufferNotDivisibleByElementSize",
"NxLibExecutionFailed",
"NxLibDebugMessageOverflow",
"",
"",
"",
"NxLibConnectionNotCompatible",
"NxLibInitializationNotAllowed",
"NxLibNestingLimitReached",
"NxLibNoOpenProfileBlock"]

#to generate automatically from c headers?
itmExecute = 'Execute' 
itmCommand = 'Command'
itmParameters = 'Parameters'
itmResult = 'Result'
itmErrorSymbol = 'ErrorSymbol'

nxLib = None
nxLibRemote = None
'''
This class encapsulates NxLib API errors. 
All overloaded functions of NxLibItem and NxLibCommand not taking a return code pointer will throw and NxLibException when the API return code indicates an error.
'''
class NxLibException(Exception):
    def __init__(self, message, path, errorCode):
        # super(NxLibException, self).__init__(message)
        # super().__init__(message)

        self.path = path
        self.errorCode = errorCode
        # self.errorText = nxLib.translateReturnCode(ErrorCode).decode()
        self.message = str(message) + str(' at ') + str(self.path) + str(' - ErrorCode ') + str(self.errorCode)

    def getErrorCode(self):
        return self.errorCode

    def getErrorText(self):
        return str(self.message) #self.errorText

    def getItemPath(self):
        return self.path

    def __str__(self):
        return str(self.message)


class NxLib(object):
    '''
    Schnittstelle zu einer NxLib Instanz über die NxLib.dll.
    '''    

    def __init__(self, PathToNxLibDll=None):
        '''
        Erwartet als Parameter den Pfad zur zu verwendenden NxLib.Dll.
        '''
        if PathToNxLibDll is not None:
            self.NxLibDll = CDLL(PathToNxLibDll) # or WinDLL(PathToNxLibDll)
        global nxLib
        nxLib  = self

    def fixStrEncoding(self,path):
        try:
            path = path.encode()
        except AttributeError:
            pass
        return path

    def checkReturnCode(self,errorCode):
        if errorCode != NxLibOperationSucceeded:
            raise NxLibException('NxLibException : ', self.path, errorCode)

    # setters

    def setNull(self,path):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibSetNull
        f.argtypes = [POINTER(c_int32),c_char_p]
        errorCode = c_int32(0)
        f(byref(errorCode),path)
        return errorCode.value

    '''
        generic setter setNx requires a function name and pointer
    '''
    def setNx(self,name,f,path,value):
        path = self.fixStrEncoding(path)
        errorCode = c_int32(0)
        f(byref(errorCode),path,value)
        return errorCode.value
       
    def setInt(self,path,value):
        f = self.NxLibDll.nxLibSetInt
        f.argtypes = [POINTER(c_int32),c_char_p, c_int32]
        return self.setNx("setInt",f,path,value)

    def setDouble(self,path,value):
        f = self.NxLibDll.nxLibSetDouble
        f.argtypes = [POINTER(c_int32),c_char_p, c_double]
        return self.setNx("setDouble",f,path,value)

    def setBool(self,path,value):
        f = self.NxLibDll.nxLibSetBool
        f.argtypes = [POINTER(c_int32),c_char_p, c_int32]
        return self.setNx("setBool",f,path,value)

    def setString(self,path,value):
        value = self.fixStrEncoding(value)
        f = self.NxLibDll.nxLibSetString
        f.argtypes = [POINTER(c_int32),c_char_p, c_char_p]
        return self.setNx("setString",f,path,value)
       
    #  void nxLibSetJson (NXLIBERR* result, NXLIBSTR itemPath, NXLIBSTR value, NXLIBBOOL onlyWriteableNodes);
    def setJson(self,path,value,onlyWriteableNodes=False):
        path = self.fixStrEncoding(path)
        value = self.fixStrEncoding(value)
        f = self.NxLibDll.nxLibSetJson
        f.argtypes = [POINTER(c_int32),c_char_p,c_char_p,c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,value,onlyWriteableNodes)
        return errorCode.value

    def setBinary(self,path,buffer,bufferSize):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibSetBinary
        f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_void_p), c_int32]
        buffer = cast(buffer, POINTER(c_void_p))
        errorCode = c_int32(0)
        f(byref(errorCode),path,buffer,bufferSize)
        return errorCode.value

    def setBinaryFormatted(self,path,buffer,width,height,channelCount,bytesPerElement,isFloat):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibSetBinaryFormatted
        f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_void_p), c_int32,  c_int32,  c_int32,  c_int32,  c_int32]
        buffer = cast(buffer, POINTER(c_void_p))
        errorCode = c_int32(0)
        f(byref(errorCode),path,buffer,width,height,channelCount,bytesPerElement,isFloat)
        return errorCode.value

    # getters

    # void nxLibGetBinary (NXLIBERR* result, NXLIBSTR itemPath, void* destinationBuffer, NXLIBINT bufferSize, NXLIBINT* bytesCopied, NXLIBDOUBLE* timestamp);
    def getBinary(self,path,destinationBuffer,bufferSize):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibGetBinary
        f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_void_p), c_int32, POINTER(c_int32),POINTER(c_double)]
        errorCode = c_int32(0)
        destinationBuffer = cast(destinationBuffer, POINTER(c_void_p))
        # destinationBuffer = c_void_p(bufferSize) #(c_ubyte * bufferSize)() 
        bytesCopied = c_int32(0)
        timestamp = c_double(0)

        result = f(byref(errorCode),path,destinationBuffer,bufferSize,byref(bytesCopied),byref(timestamp))

        return bytesCopied.value, timestamp.value, errorCode.value
        

    # void nxLibGetBinaryInfo (NXLIBERR* result, NXLIBSTR itemPath, NXLIBINT* width, NXLIBINT* height, NXLIBINT* channelCount, 
    #                          NXLIBINT* bytesPerElement, NXLIBBOOL* isFloat, NXLIBDOUBLE* timestamp);
    def getBinaryInfo(self,path):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibGetBinaryInfo
        f.argtypes = [POINTER(c_int32), c_char_p, POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_int32), POINTER(c_double)]

        errorCode = c_int32(0)
        width = c_int32(0)
        height = c_int32(0)
        channelCount = c_int32(0)
        bytesPerElement = c_int32(0)
        isFloat = c_int32(0)
        timestamp = c_double(0)

        f(byref(errorCode),path,byref(width),byref(height),byref(channelCount),byref(bytesPerElement),byref(isFloat),byref(timestamp))
       
        return width.value, height.value, channelCount.value, bytesPerElement.value, isFloat.value==1, timestamp.value, errorCode.value


    '''
        generic getter getNx requires a function name and pointer
    '''
    def getNx(self,name,f,path):
        path = self.fixStrEncoding(path)
        errorCode = c_int32(0)
        result = f(byref(errorCode),path)
        return result, errorCode.value


    # NXLIBINT nxLibGetType (NXLIBINT* result, NXLIBSTR itemPath);
    def getType(self,path):
        f = self.NxLibDll.nxLibGetType
        f.restype = c_int32
        f.argtypes = [POINTER(c_int32), c_char_p]
        return self.getNx("getType",f,path)

    def getInt(self,path):
        f = self.NxLibDll.nxLibGetInt
        f.restype = c_int32
        f.argtypes = [POINTER(c_int32), c_char_p]
        return self.getNx("getInt",f,path)

    def getBool(self,path):
        f = self.NxLibDll.nxLibGetBool
        f.restype = c_int32
        f.argtypes = [POINTER(c_int32), c_char_p]
        b, errorCode = self.getNx("getBool",f,path)
        return b == 1, errorCode

    def getCount(self,path):
        f = self.NxLibDll.nxLibGetCount
        f.restype = c_int32
        f.argtypes = [POINTER(c_int32), c_char_p]
        return self.getNx("getCount",f,path)

    def getDouble(self,path):
        f = self.NxLibDll.nxLibGetDouble
        f.restype = c_double
        f.argtypes = [POINTER(c_int32), c_char_p]
        return self.getNx("getDouble",f,path)

    def getString(self,path):
        f = self.NxLibDll.nxLibGetString
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32), c_char_p]
        s, errorCode = self.getNx("getString",f,path)
        if s is not None:
            s = s.decode()
        return s, errorCode

    def getName(self,path):
        f = self.NxLibDll.nxLibGetName
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32), c_char_p]
        s, errorCode = self.getNx("getName",f,path)
        if s is not None:
            s = s.decode()
        return s, errorCode
        
    # NXLIBSTR nxLibGetJson (NXLIBERR* result, NXLIBSTR itemPath, NXLIBBOOL prettyPrint, NXLIBINT numberPrecision, NXLIBBOOL scientificNumberFormat);
    def getJson(self,path,prettyPrint,numberPrecision,scientificNumberFormat):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibGetJson
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32, c_int32]
        errorCode = c_int32(0)
        result = f(byref(errorCode),path,prettyPrint,numberPrecision,scientificNumberFormat)       
        return result.decode(), errorCode.value

    # NXLIBSTR nxLibGetJsonMeta (NXLIBERR* result, NXLIBSTR itemPath, NXLIBINT numLevels, NXLIBBOOL prettyPrint, NXLIBINT numberPrecision, NXLIBBOOL scientificNumberFormat);
    def getJsonMeta(self,path,numLevels,prettyPrint,numberPrecision,scientificNumberFormat):
        path = self.fixStrEncoding(path)

        f = self.NxLibDll.nxLibGetJsonMeta
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32, c_int32, c_int32]
        errorCode = c_int32(0)
        result = f(byref(errorCode),path,numLevels,prettyPrint,numberPrecision,scientificNumberFormat)               
        return result.decode(), errorCode.value

    def erase(self,path):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibErase
        f.argtypes = [POINTER(c_int32), c_char_p]
        errorCode = c_int32(0)
        f(byref(errorCode),path)               
        return errorCode.value

    def waitForChange(self,path):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibWaitForChange
        f.argtypes = [POINTER(c_int32), c_char_p]
        errorCode = c_int32(0)
        f(byref(errorCode),path)               
        return errorCode.value

    def waitForType(self,path,awaitedType,waitForEqual):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibWaitForType
        f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,awaitedType,waitForEqual)               
        return errorCode.value

    def waitForIntValue(self,path,value,waitForEqual):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibWaitForIntValue
        f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,value,waitForEqual)               
        return errorCode.value
    
    def waitForStringValue(self,path,value,waitForEqual):
        path = self.fixStrEncoding(path)
        value = self.fixStrEncoding(value)
        f = self.NxLibDll.nxLibWaitForStringValue
        f.argtypes = [POINTER(c_int32), c_char_p, c_char_p, c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,value,waitForEqual)               
        return errorCode.value
    
    def waitForDoubleValue(self,path,value,waitForEqual):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibWaitForDoubleValue
        f.argtypes = [POINTER(c_int32), c_char_p, c_double, c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,value,waitForEqual)               
        return errorCode.value
    
    def waitForBoolValue(self,path,value,waitForEqual):
        path = self.fixStrEncoding(path)
        f = self.NxLibDll.nxLibWaitForBoolValue
        f.argtypes = [POINTER(c_int32), c_char_p, c_int32, c_int32]
        errorCode = c_int32(0)
        f(byref(errorCode),path,value,waitForEqual)               
        return errorCode.value

    def makeUniqueItem(self,path,itemName):
        path = self.fixStrEncoding(path)
        itemName = self.fixStrEncoding(itemName)
        f = self.NxLibDll.nxLibMakeUniqueItem
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32), c_char_p, c_char_p]
        errorCode = c_int32(0)
        newPath = f(byref(errorCode),path,value,waitForEqual)
        if newPath is not None:
            newPath = newPath.decode()               
        return newPath, errorCode.value

    def translateReturnCode(self,returnCode):
        if returnCode < 0 or returnCode > len(NxErrors) :
            return ''
        
        return NxErrors[returnCode]

    def getDebugMessages(self):
        f = self.NxLibDll.nxLibGetDebugMessages
        f.restype = c_char_p
        f.argtypes = [POINTER(c_int32)]
        result = f(byref(returnCode))
        checkReturnCode(returnCode)
        return result.decode()

    # TODO
    def getDebugBuffer(self):
        pass

    def initialize(self, waitForInitialCameraRefresh=True):
        f = self.NxLibDll.nxLibInitialize
        f.argtypes = [POINTER(c_int32),c_int32]
        f(byref(returnCode),waitForInitialCameraRefresh)
        checkReturnCode(returnCode)

    def finalize(self):
        f = self.NxLibDll.nxLibFinalize
        f.argtypes = [POINTER(c_int32)]
        f(byref(returnCode))
        checkReturnCode(returnCode)

    def openTcpPort(self,portNumber = 0, openedPort = 0):
        f = self.NxLibDll.nxLibOpenTcpPort
        f.argtypes = [POINTER(c_int32),c_int32,c_int32]
        f(byref(returnCode),portNumber,openedPort)
        checkReturnCode(returnCode)

    def closeTcpPort(self):
        f = self.NxLibDll.nxLibCloseTcpPort
        f.argtypes = [POINTER(c_int32)]
        f(byref(returnCode))
        checkReturnCode(returnCode)


class NxLibRemote(object):
    '''
    Schnittstelle zu einer NxLib Instanz über die NxLib.dll.
    '''    

    def __init__(self, PathToNxLibDll=None):
        '''
        Erwartet als Parameter den Pfad zur zu verwendenden NxLib.Dll.
        '''
        if PathToNxLibDll is not None:
            self.NxLibDll = CDLL(PathToNxLibDll) # or WinDLL(PathToNxLibDll)
        global nxLibRemote
        nxLibRemote  = self

    def fixStrEncoding(self,path):
        try:
            path = path.encode()
        except AttributeError:
            pass
        return path

    def checkReturnCode(self,errorCode):
        if errorCode != NxLibOperationSucceeded:
            raise NxLibException('NxLibException : ', self.path, errorCode)
        
    def connect(self,hostname,port):
        hostname = self.fixStrEncoding(hostname)
        f = self.NxLibDll.nxLibConnect
        f.argtypes = [POINTER(c_int32),c_char_p,c_int32]
        f(byref(returnCode),hostname,port)
        checkReturnCode(returnCode)

    def disconnect(self):
        hostname = self.fixStrEncoding(hostname)
        f = self.NxLibDll.nxLibDisconnect
        f.argtypes = [POINTER(c_int32)]
        f(byref(returnCode))
        checkReturnCode(returnCode)
    '''

    nxlib
    SetDebugThreadName
    nxLibWriteDebugMessage
    nxLibTranslateReturnCode

    NxLib:
    nxLibInitialize
    nxLibFinalize
    nxLibOpenTcpPort
    nxLibCloseTcpPort

    '''


'''
 
'''
class NxLibItem(object):

    def __init__(self,path=""):
        self.path = path
        pass

    def checkReturnCode(self,errorCode):
        if errorCode != NxLibOperationSucceeded:
            raise NxLibException('NxLibException : ', self.path, errorCode)

    def __getitem__(self, value):
        if type(value) is str: 
            return NxLibItem(self.path+NxLibItemSeparator+value)
        elif type(value) is int:
            t = self.path+NxLibItemSeparator+NxLibIndexEscapeChar+str(value)
            return NxLibItem(self.path+NxLibItemSeparator+NxLibIndexEscapeChar+str(value))
        else:
            raise NxLibException('NxLibException : ', self.path, NxLibBadRequest)

    def __setitem__(self, path, value):
        NxLibItem(self.path+NxLibItemSeparator+path).setT(value)

    def compare(self, value):
        itemValue = self.asT()
        if type(itemValue) == type(value):
            if itemValue == value:
                return 0
            elif itemValue < value:
                return -1
            else:
                return 1
        else:
            raise NxLibException('NxLibException : ', self.path, NxLibItemTypeNotCompatible)

    def __lt__(self, value):
        return self.compare(value) < 0
    def __le__(self, value):
        return self.compare(value) <= 0
    def __eq__(self, value):
        return self.compare(value) == 0
    def __ne__(self, value):
        return self.compare(value) != 0
    def __gt__(self, value):
        return self.compare(value) > 0
    def __ge__(self, value):
        return self.compare(value) >= 0

    def __lshift__(self, other):
        # call setJson on str, and setJson(itm.asJson()) on other
        if type(other) is str: 
            self.setJson(str,True)
        elif isinstance(other,NxLibItem):
            self.setJson(other.asJson(),True)
        else :
            raise NxLibException('NxLibException : ', self.path, NxLibItemTypeNotCompatible)

    def setT(self,value):
        if value is None:
            self.setNull()
        elif type(value) is int:
            if(value > 2147483647 or value < -2147483648): 
                self.setDouble(value)
            else:
                self.setInt(value)    
        elif type(value) is str:
            self.setString(value)
        elif type(value) is bool:
            self.setBool(value)   
        else:
            raise NxLibException('NxLibException : ', self.path, NxLibItemTypeNotCompatible)   
        # elif type(value) is :
        #    self.setInt(value)

    def setNull(self):
        errorCode = nxLib.setNull(self.path)
        self.checkReturnCode(errorCode)

    def setDouble(self,value):
        errorCode = nxLib.setDouble(self.path,value)
        self.checkReturnCode(errorCode)

    def setInt(self,value):
        errorCode = nxLib.setInt(self.path,value)
        self.checkReturnCode(errorCode)

    def setBool(self,value):
        errorCode = nxLib.setBool(self.path,value)
        self.checkReturnCode(errorCode)

    def setString(self,value):
        errorCode = nxLib.setString(self.path,value)
        self.checkReturnCode(errorCode)

    def setJson(self,value,onlyWriteableNodes=False):
        errorCode = nxLib.setJson(self.path,value,onlyWriteableNodes)
        self.checkReturnCode(errorCode)

    def setBinaryData(self,buffer,bufferSizeOrWidth=0,height=0,channelCount=0,bytesPerElement=0,isFloat=0):
        if bufferSizeOrWidth==0:
            # cvMat
            self.setBinaryDataFromCvMat(buffer)
        else:
            if(channelCount>0): # formatted
                width = bufferSizeOrWidth
                errorCode = nxLib.setBinaryFormatted(self.path,buffer,width,height,channelCount,bytesPerElement,isFloat)    
            else: # not formatted 
                bufferSize = bufferSizeOrWidth
                errorCode = nxLib.setBinary(self.path,buffer,bufferSize)
            self.checkReturnCode(errorCode)

    def setBinaryDataFromCvMat(self,mat):
        if type(mat).__name__ != 'ndarray':
            raise NxLibException('NxLibException : ', self.path, NxLibItemTypeNotCompatible)

        channelCount = mat.shape[2]
        isFloat = False
        if mat.dtype == 'uint8' or mat.dtype == 'int8':
            bpe = 1
        elif mat.dtype == 'uint16' or mat.dtype == 'int16':
            bpe = 2
        elif mat.dtype == 'int32':
            bpe = 4
        elif mat.dtype == 'float32':
            bpe = 4
            isFloat = True
        elif mat.dtype == 'float64':
            bpe = 8
            isFloat = True

        buffer = np.ctypeslib.as_ctypes(mat) # mat.ravel()
        errorCode = nxLib.setBinaryFormatted(self.path,buffer,mat.shape[1],mat.shape[0],channelCount,bpe,isFloat)    
        self.checkReturnCode(errorCode)

    def getBinaryData(self,bufferSize=0):    
        # initialize buffer ?  
        if bufferSize == 0 :
            buffer = self.createCvMatBuffer()
            bufferSize = buffer.shape[0] * buffer.shape[1] * buffer.shape[2]
            cbuffer = np.ctypeslib.as_ctypes(buffer)
        else:
            cbuffer = [] #?? to test # TODO
        bytesCopied, timestamp, errorCode = nxLib.getBinary(self.path,cbuffer,bufferSize)
        self.checkReturnCode(errorCode)
        return buffer
    
    def createCvMatBuffer(self):
        width, height, channelCount, bpe, isFloat, timestamp, errorCode = self.getBinaryDataInfo()        
        nptype = np.uint8
        if isFloat:
            if bpe == 4:
                nptype = np.float32 # 'float32'
            elif bpe == 8:
                nptype = np.float64 # 'float64'
        else:
            if bpe == 1:
                nptype = np.uint8 # 'uint8'
            elif bpe == 2:
                nptype = np.int16 # 'int16'
            elif bpe == 4:
                nptype = np.int32 # 'int32'

        image_buffer = np.zeros((height,width,channelCount), nptype, order='C')

        return image_buffer
        '''
        if isFloat:
            if channelCount == 1:
                if bpe == 4:
                    cvtype = cv2.CV_32FC1
                elif bpe == 8:
                    cvtype = cv2.CV_64FC1
            elif channelCount == 2:
                if bpe == 4:
                    cvtype = cv2.CV_32FC2
                elif bpe == 8:
                    cvtype = cv2.CV_64FC2
            elif channelCount == 3:
                if bpe == 4:
                    cvtype = cv2.CV_32FC3
                elif bpe == 8:
                    cvtype = cv2.CV_64FC3
            elif channelCount == 4:
                if bpe == 4:
                    cvtype = cv2.CV_32FC4
                elif bpe == 8:
                    cvtype = cv2.CV_64FC4
        else:
            if channelCount == 1:
                if bpe == 1:
                    cvtype = cv2.CV_32FC1
                elif bpe == 2:
                    cvtype = cv2.CV_64FC1
                elif bpe == 4:
                    cvtype = cv2.CV_64FC1
                elif bpe == 8:
                    cvtype = cv2.CV_64FC1
            elif channelCount == 2:
                if bpe == 4:
                    cvtype = cv2.CV_32FC2
                elif bpe == 8:
                    cvtype = cv2.CV_64FC2
            elif channelCount == 3:
                if bpe == 4:
                    cvtype = cv2.CV_32FC3
                elif bpe == 8:
                    cvtype = cv2.CV_64FC3
            elif channelCount == 4:
                if bpe == 4:
                    cvtype = cv2.CV_32FC4
                elif bpe == 8:
                    cvtype = cv2.CV_64FC4
        '''


    def getBinaryDataInfo(self):        
        width, height, channelCount, bpe, isFloat, timestamp, errorCode = nxLib.getBinaryInfo(self.path)
        self.checkReturnCode(errorCode)
        return width, height, channelCount, bpe, isFloat, timestamp, errorCode

    def asT(self):
        if self.isNull():
            return None
        elif self.isDouble():
            return self.asDouble()           
        elif self.isInt():
            return self.asInt()
        elif self.isString():
            return self.asString()
        elif self.isBool():
            return self.asBool()  
        else:
            raise NxLibException('NxLibException : ', self.path, NxLibItemTypeNotCompatible)   

    def asInt(self):        
        i, errorCode = nxLib.getInt(self.path)
        self.checkReturnCode(errorCode)
        return i
    
    def asBool(self):        
        b, errorCode = nxLib.getBool(self.path)
        self.checkReturnCode(errorCode)
        return b
    
    def asDouble(self):        
        d, errorCode = nxLib.getDouble(self.path)
        self.checkReturnCode(errorCode)
        return d

    def asString(self):        
        s, errorCode = nxLib.getString(self.path)
        self.checkReturnCode(errorCode)
        return s

    def count(self):        
        c, errorCode = nxLib.getCount(self.path)
        self.checkReturnCode(errorCode)
        return c

    def asJson(self,prettyPrint=1,numberPrecision=2,scientificNumberFormat=0):
        json, errorCode = nxLib.getJson(self.path,prettyPrint,numberPrecision,scientificNumberFormat)
        self.checkReturnCode(errorCode)
        return json

    def asJsonMeta(self,numLevels=1,prettyPrint=1,numberPrecision=2,scientificNumberFormat=0):
        jsonMeta, errorCode = nxLib.getJsonMeta(self.path,numLevels,prettyPrint,numberPrecision,scientificNumberFormat)
        self.checkReturnCode(errorCode)
        return jsonMeta

    def isNull(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeNull

    def isString(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeString

    def isNumber(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeNumber

    def isBool(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeBool

    def isArray(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeArray

    def isObject(self):
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t == NxLibItemTypeObject

    def type(self): # overrides python type keyword ... !
        t, errorCode = nxLib.getType(self.path)
        self.checkReturnCode(errorCode)
        return t

    def exists(self):
        t, errorCode = nxLib.getType(self.path)
        if errorCode == NxLibItemInexistent:
            return False
        elif errorCode == NxLibOperationSucceeded:
            return t != NxLibItemTypeInvalid
        else:
            self.checkReturnCode(errorCode)
            return False

    def name(self): 
        itemName, errorCode = nxLib.getName(self.path)
        self.checkReturnCode(errorCode)
        return itemName

    def erase(self):
        errorCode = nxLib.erase(self.path)
        if errorCode == NxLibItemInexistent:
                return
        self.checkReturnCode(errorCode)

    def waitForChange(self):
        errorCode = nxLib.waitForChange(self.path)
        self.checkReturnCode(errorCode)

    def waitForType(self,awaitedType,waitForEqual):
        errorCode = nxLib.waitForType(self.path,awaitedType,waitForEqual)
        self.checkReturnCode(errorCode)

    def waitForValue(self,value,waitForEqual):
        if type(value) is int:
            # double or int ?
            errorCode = nxLib.waitForIntValue(self.path,value,waitForEqual)
        elif type(value) is str:
            errorCode = nxLib.waitForStringValue(self.path,value,waitForEqual)
        elif type(value) is bool:
            errorCode = nxLib.waitForBoolValue(self.path,value,waitForEqual)    
        self.checkReturnCode(errorCode)

    def makeUniqueItem(self,itemName):
        newPath, errorCode = nxLib.makeUniqueItem(self.path,itemName)
        self.checkReturnCode(errorCode)
        if newPath:
            return NxLibItem(newPath)
        return NxLibItem()


'''


'''
class NxLibCommand(object):

    def __init__(self, commandName, nodeName=None):

        self.commandName = commandName
        self.removeSlotOnDestruction = False
        
        if not nodeName:
            self.commandItem = NxLibItem()[itmExecute]
        else:
            self.commandItem = NxLibItem()[itmExecute][nodeName]

    def __del__(self):
        try:
            if self.removeSlotOnDestruction:
                self.commandItem.erase()
        except NxLibException:
            pass 

    def createTemporarySlot(self,baseName):
        self.removeSlotOnDestruction = True
        execItem = NxLibItem()[itmExecute]
        self.commandItem = execItem.makeUniqueItem(baseName)

    def checkReturnCode(self,returnCode):
        if returnCode != NxLibOperationSucceeded:
                raise NxLibException('NxLibException : ', self.path, returnCode)
    
    def parameters(self):
        return self.commandItem[itmParameters]

    def result(self):
        return self.commandItem[itmResult]

    def successful(self):
        errorCode = NxLibOperationSucceeded
        try:
            hasError = self.result()[itmErrorSymbol].exists()
        except NxLibException as e:
            errorCode = e.getErrorCode()  
            hasError = True  
        return hasError == False, errorCode

    def execute(self,commandName=None,wait=True):
        functionItem = self.commandItem[itmCommand]
        if not commandName:
            commandName = self.commandName
        try:
            functionItem.setT(commandName)
        except NxLibException as e:
            return e.getErrorCode()

        if wait:
            try:
                functionItem.waitForType(NxLibItemTypeNull, True)
            except NxLibException as e:
                return e.getErrorCode()
            
            result, returnCode = self.successful()
            if result == NxLibOperationSucceeded:
                return NxLibOperationSucceeded
            else:
                return NxLibExecutionFailed

            # raise exception or return error code, to change

    def finished(self):
        if not self.commandItem[itmCommand].exists() or self.commandItem[itmCommand].type() == NxLibItemTypeNull:
            return True
        return False



