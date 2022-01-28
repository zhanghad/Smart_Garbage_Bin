import RPi.GPIO as GPIO
import time
from config import config
import logging

def buzzer_setup():
    logging.info('buzzer setup')
    global makerobo_BuzzerPin
    makerobo_BuzzerPin = config.buzzer
    GPIO.setmode(GPIO.BOARD)  # 采用实际的物理管脚给GPIO口
    GPIO.setwarnings(False)  # 关闭GPIO警告提示
    GPIO.setup(makerobo_BuzzerPin, GPIO.OUT)  # 设置蜂鸣器管脚为输出模式
    GPIO.output(makerobo_BuzzerPin, GPIO.LOW)  # 蜂鸣器设置为低电平，关闭状态


def buzzer_on():
    logging.info('buzzer on')
    GPIO.output(makerobo_BuzzerPin, GPIO.HIGH)  # 打开蜂鸣器


def buzzer_off():
    logging.info('buzzer off')
    GPIO.output(makerobo_BuzzerPin, GPIO.LOW)  # 关闭蜂鸣器


def buzzer_beep(x):
    logging.info('buzzer beep')
    buzzer_on()  # 打开蜂鸣器控制
    time.sleep(x)  # 延时时间
    buzzer_off()  # 关闭蜂鸣器控制
    time.sleep(x)  # 延时时间


def buzzer_loop(x):
    while True:
        buzzer_beep(x)  # 控制蜂鸣器鸣叫时间，延时时间为0.5秒


def buzzer_destroy():
    logging.info('buzzer destroy')
    GPIO.setmode(GPIO.BOARD)
    GPIO.output(makerobo_BuzzerPin, GPIO.LOW)  # 关闭蜂鸣器鸣叫
    GPIO.cleanup()  # 释放资源


if __name__ == '__main__':
    buzzer_setup()  # 设置GPIO管脚
    try:  # 检测异常
        buzzer_loop(0.5)  # 调用循环函数
    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序
        buzzer_destroy()  # 释放资源
