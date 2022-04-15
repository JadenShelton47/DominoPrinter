import queue
import threading
import socket
from pylogix import PLC
import time





with PLC() as plc:
    plc.IPAddress = '10.80.3.240'



def buildSer(id,q):
    [by0, by1, by2, by3] = id.to_bytes(4, 'big', signed=True)
    array1 = [by0, by1, by2, by3]
    q.put(array1)
    
    
def printGO():
    try:
        Go = bytearray()
        Go.append(0x1B)
        Go.append(0x4E)
        Go.append(0x31)
        Go.append(0x04)
        s.send(Go)
        data1 = s.recv(6).hex()
        plc.Write('Print_Ack', True)
        print("PrintDone")   
        print(data1)
        print(s)
    except:
        print("Didnt Work")
    
    try:
        bufQ = bytearray()
        bufQ.append(0x1b) #esc
        bufQ.append(0x7E) #cmd
        bufQ.append(0x50) #cmd
        bufQ.append(0x30) #comm method
        bufQ.append(0x3f) #q cmd
        bufQ.append(0x04) #eot
        s.send(bufQ)

        bufLEN = s.recv(12).hex()
        print("HEREHREHREHERHERHERHR")
        print(bufLEN)
        print("is the length")
    except:
        print("Buffer length not Recieved")

def sendEDC():
        array1 = q.get()
        serID = bytearray()#
        serID.append(0x1b)
        serID.append(0x4f)
        serID.append(0x45) #Command
        serID.append(0x30) #Datalength
        serID.append(0x30) #Datalength
        serID.append(0x30) #Datalength
        serID.append(0x34) #Datalength
        for i in array1:    #for loop used to insert variable data into byte array
            serID.append(i)
        serID.append(0x04)
        print(edc)
        edc.send(serID)
        time.sleep(.01)
        
        print("EDC stuff was sent")
        
        print(serID)   

def initPrint():
    init = bytearray()
    init.append(0x1b)          #start
    init.append(0x4f)          #command
    init.append(0x50)          #command
    init.append(0x30)          #startChar
    init.append(0x32)          #startChar
    init.append(0x30)          #externalDataEnc
    init.append(0x30)          #endChar
    init.append(0x33)          #endChar
    init.append(0x31)          #lengthOfExtData
    init.append(0x30)          #lengthOfExtData
    init.append(0x32)          #lengthOfExtData
    init.append(0x34)          #lengthOfExtData
    init.append(0x31)          #AckNak
    init.append(0x30)          #Log
    init.append(0x30)          #Dup
    init.append(0x30)          #Dup
    init.append(0x30)          #LogFullAct
    init.append(0x30)          #LogPer
    init.append(0x30)          #LabelChangeAct
    init.append(0x04)          #EOT
    s.send(init)
    print("initializing")
    ack = s.recv(1).hex()
    print(ack)
    
    time.sleep(2)

def MainDef():
    while True:
        PrintGO = plc.Read('Print_Go')
        ret = plc.Read('SerialID')
        if PrintGO.Value == True:
            id = ret.Value
            buildSer(id,q)
            printGO()
        else: 
            continue

q = queue.Queue()        
EDCThread = threading.Thread(target= sendEDC)
edc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
edc.connect(('10.80.3.86', 16000))
blocking = edc.getblocking()
print(blocking)

mainThread = threading.Thread(target= MainDef)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.80.3.86', 7000))


initPrint()

mainThread.start()
EDCThread.start()




