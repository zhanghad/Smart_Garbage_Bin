import RPi.GPIO as GPIO
import time
import threading
from config import config
import logging
import traceback

# 规定GPIO引脚
IN1 = config.motor_1_1  # 接PUL-
IN2 = config.motor_1_2  # 接PUL+
IN3 = config.motor_1_3  # 接DIR-
IN4 = config.motor_1_4  # 接DIR+

IN5 = config.motor_2_1  # 接PUL-
IN6 = config.motor_2_2  # 接PUL+
IN7 = config.motor_2_3  # 接DIR-
IN8 = config.motor_2_4  # 接DIR+


def setStep1(w1, w2, w3, w4):  # 步进电机1,下
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)


def setStep2(u1, u2, u3, u4):  # 步进电机2,上
    GPIO.output(IN5, u1)
    GPIO.output(IN6, u2)
    GPIO.output(IN7, u3)
    GPIO.output(IN8, u4)


def stop1(n):
    logging.info('stop1')
    setStep1(0, 0, 0, 0)
    time.sleep(n)


def stop2(n):
    logging.info('stop2')
    setStep2(0, 0, 0, 0)
    time.sleep(n)


def forward1(delay, steps):
    logging.info('forward1:' + str(steps))
    for i in range(0, steps):
        setStep1(1, 0, 1, 0)
        time.sleep(delay)
        setStep1(0, 1, 1, 0)
        time.sleep(delay)
        setStep1(0, 1, 0, 1)
        time.sleep(delay)
        setStep1(1, 0, 0, 1)
        time.sleep(delay)


def forward2(delay, steps):
    logging.info('forward2:' + str(steps))
    for i in range(0, steps):
        setStep2(1, 0, 1, 0)
        time.sleep(delay)
        setStep2(0, 1, 1, 0)
        time.sleep(delay)
        setStep2(0, 1, 0, 1)
        time.sleep(delay)
        setStep2(1, 0, 0, 1)
        time.sleep(delay)


def backward1(delay, steps):
    logging.info('backward1:' + str(steps))
    for i in range(0, steps):
        setStep1(1, 0, 0, 1)
        time.sleep(delay)
        setStep1(0, 1, 0, 1)
        time.sleep(delay)
        setStep1(0, 1, 1, 0)
        time.sleep(delay)
        setStep1(1, 0, 1, 0)
        time.sleep(delay)


def backward2(delay, steps):
    logging.info('backward2:' + str(steps))
    for i in range(0, steps):
        setStep2(1, 0, 0, 1)
        time.sleep(delay)
        setStep2(0, 1, 0, 1)
        time.sleep(delay)
        setStep2(0, 1, 1, 0)
        time.sleep(delay)
        setStep2(1, 0, 1, 0)
        time.sleep(delay)


def motor_setup():
    logging.info('motor setup')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(IN1, GPIO.OUT)  # Set pin's mode is output
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(IN5, GPIO.OUT)
    GPIO.setup(IN6, GPIO.OUT)
    GPIO.setup(IN7, GPIO.OUT)
    GPIO.setup(IN8, GPIO.OUT)


# map
# 3 2
# 0 1

def both_forward(n):
    arg1 = config.motor_move_delay
    arg2 = n
    logging.info('both motors forward:' + str(n))

    t1 = threading.Thread(target=forward1, args=(arg1, arg2,))
    t2 = threading.Thread(target=forward2, args=(arg1, arg2,))
    try:
        t1.start()
        t2.start()
    except:
        logging.error('both_forward thread error')
        logging.error(traceback.format_exc())
    t1.join()
    t2.join()


def both_stop(n):
    logging.info('both motors stop')
    t1 = threading.Thread(target=stop1, args=(n,))
    t2 = threading.Thread(target=stop2, args=(n,))

    try:
        t1.start()
        t2.start()
    except:
        logging.error('both_stop thread error')
        logging.error(traceback.format_exc())

    t1.join()
    t2.join()


def both_backward(n):
    arg1 = config.motor_move_delay
    arg2 = n

    logging.info('both motors forward:' + str(n))

    t1 = threading.Thread(target=backward1, args=(arg1, arg2,))
    t2 = threading.Thread(target=backward2, args=(arg1, arg2,))
    try:
        t1.start()
        t2.start()
    except:
        logging.error('both_backward thread error')
        logging.error(traceback.format_exc())
    t1.join()
    t2.join()


def moveto(n):  # n=0,1,2,3
    logging.info('move to bin [%d]' % n)
    arg1 = config.motor_move_delay
    arg2s = [0, 2800//2, 5600//2, 8400//2]
    #arg2s = [0, 2800//1, 5600//1, 8400//1]
    stop_delay=config.motor_stop_delay

    if n == 0:
        forward1(arg1, arg2s[1])
        stop1(stop_delay)
        backward1(arg1, arg2s[1])
        stop1(stop_delay)
    elif n == 1:
        forward2(arg1, arg2s[1])
        stop2(stop_delay)
        backward2(arg1, arg2s[1])
        stop2(stop_delay)
    elif n == 3:
        backward2(arg1, arg2s[1])
        stop2(stop_delay)
        forward2(arg1, arg2s[1])
        stop2(stop_delay)
    elif n == 2:
        # move to 2
        both_forward(arg2s[1])
        both_stop(stop_delay)

        # clear trash
        forward2(arg1, arg2s[1])
        stop2(stop_delay)
        backward2(arg1, arg2s[1])
        stop2(stop_delay)

        # back to 0
        both_backward(arg2s[1])
        both_stop(stop_delay)

    else:
        logging.error('index error')

    logging.info('moveto finish')
    return


def motor_destroy():
    logging.info('motor destroy')
    GPIO.cleanup()  # 释放数据


if __name__ == '__main__':  # Program start from here
    motor_setup()

    try:
        moveto(2)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
        motor_destroy()
