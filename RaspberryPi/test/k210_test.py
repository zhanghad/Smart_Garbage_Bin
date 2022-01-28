import serial
import traceback

ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)

try:
    while True:
        #ser.write('s')
        re = ser.readline()
        #print(re)
        
        if (re == b''):
            print('null')
        else:
            re = re.decode('utf-8')[:-1]
            relist=re.split(' ',-1);
            print(re)
            #print(relist)
        
except:
    print('close')
    traceback.print_exc()
    ser.close()

