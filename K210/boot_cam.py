'''
实验名称：照相机
版本：v1.0
日期：2019.12
作者：01Studio 【www.01Studio.org】
说明：通过按键拍照并在LCD上显示（本实验需要SD卡）。
'''
import sensor, lcd, utime,os
from Maix import GPIO
from fpioa_manager import fm
fm.register(16, fm.fpioa.GPIOHS0, force=True)
KEY=GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.skip_frames(30)
lcd.init()
key_node = 0
name_num = 0
def fun(KEY):
	global key_node
	utime.sleep_ms(10)
	if KEY.value()==0:
		key_node = 1
KEY.irq(fun, GPIO.IRQ_FALLING)
images_num=len(os.listdir("/sd/images"))
while True:
	lcd.display(sensor.snapshot())
	if key_node==1:
		key_node = 0
		img=sensor.snapshot()
		lcd.display(img.save("/sd/images/"+str(images_num+1)+".jpg"))
		lcd.draw_string(10, 10, str(images_num))
		images_num=images_num+1
