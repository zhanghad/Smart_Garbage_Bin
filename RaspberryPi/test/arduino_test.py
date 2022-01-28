import serial
import traceback

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
num=0

try:
    while True:
        #ser.write('s'.encode('utf-8'))
        
        re = ser.readline()
        #print(re)
        
        num=num+1
        
        if (re == b''):
            print('null')
        else:
            
            print(num)
            
            re = re.decode('utf-8')[:-1]
            print(re)
        
        
except:
    print('close')
    traceback.print_exc()
    ser.close()
