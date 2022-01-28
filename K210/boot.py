import sensor, lcd, utime,time
from Maix import GPIO
from fpioa_manager import fm
import KPU as kpu
import uos
import image
from machine import UART,Timer
import gc
fm.register(9, fm.fpioa.UART1_RX, force=True)
fm.register(10, fm.fpioa.UART1_TX, force=True)
uart = UART(UART.UART1, 115200, read_buf_len=4096)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
#sensor.set_hmirror(1)
sensor.skip_frames(30)
lcd.init()
class_labels=['apple','background','banana','battery','bottle','brick','can','carrot','cell','cigarette','orange','pepper','potato','tomato']
kmodel_path='/sd/trash.kmodel'
try:
	print('load model')
	model=kpu.load(kmodel_path)
	kpu.set_outputs(model,0,1,1,14)
	print('load success')
except:
	print('load error')
while True:
	img = sensor.snapshot()
	t = time.ticks_ms()
	fmap = kpu.forward(model, img)
	t = time.ticks_ms() - t
	plist = fmap[:]
	pmax = max(plist)
	max_index = plist.index(pmax)
	labelText = class_labels[max_index].strip()
	acc = ('{:.1f}%'.format(pmax * 100))
	lcd.display(img)
	lcd.draw_string(10, 10, labelText)
	lcd.draw_string(10, 30, acc)
	lcd.draw_string(10, 60, (str(t) + ' ms'))
	uart.write(labelText+' '+str(acc)+' '+str(t)+'\n')
