
from array import array
import socket
from pylogix import PLC
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.80.3.86', 7000))

edc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
edc.connect(('10.80.3.86', 16000))

with PLC() as plc:
    plc.IPAddress = '10.80.3.240'
def buildSer(id):
    [by0, by1, by2, by3] = id.to_bytes(4, 'big', signed=True)
    array1 = [by0, by1, by2, by3]
    sendEDC(array1)
    
def printGO():
    try:
        Go = bytearray()
        Go.append(0x1B)
        Go.append(0x4E)
        Go.append(0x31)
        Go.append(0x04)
        s.send(Go)
        data1 = s.recv(4).hex()
        plc.Write('Print_Ack', True)
        print("PrintDone")   
        print(data1)
        print(s)
    except:
        print("Didnt Work")


def sendEDC(array1):
    try:
        serID = bytearray()#
        serID.append(0x02)
        serID.append(0x4f)
        serID.append(0x45) #Command
        serID.append(0x30) #Datalength
        serID.append(0x30) #Datalength
        serID.append(0x30) #Datalength
        serID.append(0x34) #Datalength
        for i in array1:    #for loop used to insert variable data into byte array
            serID.append(i)
        serID.append(0x03)
        print(serID)
        edc.send(serID)
        print("data sent")
        print(serID)
        print(edc)       
    except:
        print("idNotSent")
        print(edc)
        

def initPrint():
    init = bytearray()
    init.append(0x1b)          #start
    init.append(0x4f)          #command
    init.append(0x50)          #command
    init.append(0x46)          #startChar
    init.append(0x46)          #startChar
    init.append(0x30)          #externalDataEnc
    init.append(0x46)          #endChar
    init.append(0x46)          #endChar
    init.append(0x30)          #lengthOfExtData
    init.append(0x30)          #lengthOfExtData
    init.append(0x30)          #lengthOfExtData
    init.append(0x32)          #lengthOfExtData
    init.append(0x30)          #AckNak
    init.append(0x30)          #Log
    init.append(0x30)          #Dup
    init.append(0x30)          #Dup
    init.append(0x31)          #LogFullAct
    init.append(0x31)          #LogPer
    init.append(0x31)          #LabelChangeAct
    init.append(0x04)          #
    s.send(init)
    print("initializing")
    time.sleep(2)
initPrint()
while True:
    PrintGO = plc.Read('Print_Go')
    ret = plc.Read('SerialID')
    if PrintGO.Value == True:
        id = ret.Value
        buildSer(id)
        #sendEDC(edc)
        printGO()
    else: 
        continue
