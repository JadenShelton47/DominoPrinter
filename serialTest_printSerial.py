
import serial
from pylogix import PLC
import time

data1 = hex
ser = serial.Serial('COM4', 9600, timeout=.5)
with PLC() as plc:
    plc.IPAddress = '10.80.3.240'



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
ser.write(init)
whathappen = ser.readline(2).hex()
print(whathappen)

while True: 
    time.sleep(1) 
    PrintGO = plc.Read('Print_Go')
    print(PrintGO)
    if PrintGO.Value == False:
        continue 
    try:    
        SerialID = plc.Read('SerialID')
        #print(SerialID.Value)
        
    except:
        print("No Read")


    else:
        try:
            serID = bytearray()#
            serID.append(0x1B)
            serID.append(0x4f)
            serID.append(0x45) #Command
            serID.append(0x30) #Datalength
            serID.append(0x30) #Datalength
            serID.append(0x30) #Datalength
            serID.append(0x34) #Datalength
            serID.append(0xff)
            serID.append(0xff)
            serID.append(0xff)
            serID.append(0xff)
            serID.append(0x04)
            ser.write(serID)
            print("data sent")
            data2 = ser.readline(2).hex()
            print(data2, "data2")
            print("data Returned")
            
        except:
            print("idNotSent")
            break
        try:
            print(SerialID.Value)
            Go = bytearray()
            Go.append(0x1B)
            Go.append(0x4f)
            Go.append(0x31)
            Go.append(0x04)
            ser.write(Go)
            
            data1 = ser.readline().hex()
            
            plc.Write('Print_Ack', True)
            print("PrintDone")   
            time.sleep(.2)
        except:
            print("Didnt Work")
        continue
    
    


                    