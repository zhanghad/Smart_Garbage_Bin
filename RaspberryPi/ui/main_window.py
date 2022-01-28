import cv2
import threading
import time
import serial
import logging
import traceback

import PyQt5.QtCore as PQC
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QProgressBar, QApplication

from config import config, constant
from motor.motor import moveto, motor_setup, motor_destroy
from sensor.buzzer import buzzer_loop, buzzer_setup, buzzer_destroy,buzzer_off,buzzer_on

"""
    author:zhanghad
    qq:1310200276
"""


class MainForm(QMainWindow):

    def __init__(self):
        super(MainForm, self).__init__()

        # desktop = QApplication.desktop()
        # print("屏幕宽:" + str(desktop.width()))
        # print("屏幕高:" + str(desktop.height()))

        # set up GPIO
        buzzer_setup()
        motor_setup()

        # global variables
        # self.is_predicting = False
        self.is_moving = False
        self.is_buzzer_on = False
        self.object_exist = False
        self.buzzer_full_count = 0
        self.global_enable = True
        self.motor_enable = config.motor_enable
        self.bin_count = [0, 0, 0, 0]
        self.trash_count = 0
        self.last_class = ''
        self.smart_detect = config.smart_detect

        # thread locks
        # self.is_predicting_lock = threading.Lock()
        self.is_moving_lock = threading.Lock()
        self.object_exist_lock = threading.Lock()
        self.global_enable_lock = threading.Lock()
        self.motor_enable_lock = threading.Lock()
        self.bin_count_lock = threading.Lock()
        self.trash_count_lock = threading.Lock()
        self.last_class_lock = threading.Lock()
        self.arduino_commu_lock = threading.Lock()
        self.buzzer_state = threading.Lock()
        

        # init threads
        self.threadArduino = ThreadArduino()
        self.threadK210 = ThreadK210()
        self.threadMove = ''
        self.threadBuzzer = ''

        self.threadArduino.mainThread.connect(self.main_controller)
        self.threadK210.mainThread.connect(self.main_controller)

        self.threadK210.start()
        self.threadArduino.start()

        # init ui and create components
        self.resize(1024, 600)
        # self.showFullScreen()
        self.move(0, 0)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.class_label = QLabel(self)
        self.result_label = QLabel(self)
        self.status_label = QLabel(self)

        self.capacity_label = []
        self.bin_label = []
        self.count_label = []
        for i in range(0, 4):
            self.capacity_label.append(QLabel(self))
            self.bin_label.append(QLabel(self))
            self.count_label.append(QLabel(self))

        # init result label
        self.result_label.setGeometry(0, 0, 1024, 200)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("QLabel{background:rgb(172,218,224,250);}"
                                        "QLabel{color:rgb(0,0,0,250);font-size:70px;font-weight:bold;font-family:Roman times;}")
        self.result_label.setText(constant.INIT_RESULT_LABEL)
        self.result_label.setVisible(True)

        # init status label
        self.status_label.setGeometry(576, 600 - 76, 448, 76)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("QLabel{background:rgb(196,219,102,250);}"
                                        "QLabel{color:rgb(0,0,0,250);font-size:30px;font-weight:bold;font-family:Roman times;}")
        self.status_label.setText(constant.STATUS_LABEL_FREE)
        self.status_label.setVisible(True)

        # init classification label
        self.class_label.setParent(self)
        self.class_label.setVisible(True)
        self.class_label.setGeometry(576, 448, 448, 76)
        self.class_label.setStyleSheet("QLabel{background:rgb(21,184,215,250);}"
                                       "QLabel{color:rgb(255,255,255,250);font-size:30px;font-weight:bold;font-family:Roman times;}")
        self.class_label.setText("wait trash")
        self.class_label.setAutoFillBackground(True)
        self.class_label.setAlignment(Qt.AlignCenter)

        # init capacity bars && bin label && count label
        for i in range(0, 4):
            self.capacity_label[i].setGeometry(i * 144, 300, 144, 200)
            self.capacity_label[i].setAlignment(Qt.AlignCenter)
            self.capacity_label[i].setWordWrap(True)
            self.capacity_label[i].setText(constant.UN_FULL)
            self.capacity_label[i].setStyleSheet("QLabel{background:rgb(255,255,255,250);}"
                                                 "QLabel{color:rgb(0,0,0,250);font-size:30px;font-weight:bold;font-family:Roman times;}")
            self.capacity_label[i].setVisible(True)

            self.bin_label[i].setGeometry(i * 144, 500, 144, 100)
            self.bin_label[i].setWordWrap(True)
            self.bin_label[i].setAlignment(Qt.AlignCenter)
            self.bin_label[config.bin_map[i][0]].setText(config.bin_map[i][2])
            self.bin_label[i].setStyleSheet("QLabel{background:rgb(255,255,255,250);}"
                                            "QLabel{color:rgb(0,0,0,250);font-size:30px;font-weight:bold;font-family:Roman times;}")
            self.bin_label[i].setVisible(True)

            self.count_label[i].setGeometry(i * 144, 200, 144, 100)
            self.count_label[i].setWordWrap(True)
            self.count_label[i].setAlignment(Qt.AlignCenter)
            self.count_label[i].setText(str(self.bin_count[i]))
            self.count_label[i].setStyleSheet("QLabel{background:rgb(255,255,255,250);}"
                                              "QLabel{color:rgb(0,0,0,250);font-size:30px;font-weight:bold;font-family:Roman times;}")
            self.count_label[i].setVisible(True)
        
        buzzer_off()
        logging.info('main ui init success!')

    def __del__(self):
        # clean up GPIO
        motor_destroy()
        buzzer_off()
        buzzer_destroy()

    # to receive all thread's message and controller
    def main_controller(self, info):
        sender = info['sender']

        if sender == 'ThreadMove':
            if info[constant.STATUS] == constant.FAIL:
                logging.error('ThreadMove ' + info[constant.STATUS])
            else:
                # move finish
                self.is_moving_lock.acquire()
                self.is_moving = False
                self.is_moving_lock.release()
                self.object_exist_lock.acquire()
                self.object_exist = False
                self.object_exist_lock.release()
                self.trash_count_lock.acquire()
                self.trash_count += 1
                self.trash_count_lock.release()
                self.update_count_label()
                self.status_label.setText(constant.STATUS_LABEL_FREE)
                temp=0
                for i in range(0,4):
                    if config.bin_map[i][2]==self.last_class:
                        temp=config.bin_map[i][0]
                '''
                for b in config.binmap:
                    if b[2]==self.last_class:
                        temp=b[0]
                '''
                self.result_label.setText(str(self.trash_count) + '-' + self.last_class + '-'+str(self.bin_count[temp])+'-OK')
                self.class_label.setText(self.last_class)

        elif sender == 'ThreadK210':
            if info[constant.STATUS] == constant.FAIL:
                logging.error('ThreadK210 ' + info[constant.STATUS])
            else:
                dlist = info['K210'].split(' ', -1)
                if self.smart_detect == False:
                    self.class_label.setText(dlist[0] + " " + dlist[1] + ' (' + dlist[2] + 'ms)')
                
                # self.status_label.setText(constant.STATUS_LABEL_CLASS_SUCCESS)
                if not self.motor_enable:
                    logging.debug('motor is not enable')
                elif self.is_moving:
                    logging.debug('motor is moving, need to wait')
                elif not self.object_exist:
                    logging.debug('not exist')
                elif self.smart_detect == False:
                    # map trash to a bin
                    index = 0
                    temp_name = ''
                    for m in config.bin_map:
                        if (dlist[0] in m[1]):
                            index = m[0]
                            temp_name = m[2]
                    # increase count
                    self.bin_count_lock.acquire()
                    self.bin_count[index] += 1
                    self.bin_count_lock.release()
                    self.last_class_lock.acquire()
                    self.last_class = temp_name
                    self.last_class_lock.release()

                    # move trash to specific bin
                    self.is_moving_lock.acquire()
                    self.is_moving = True
                    self.is_moving_lock.release()
                    self.status_label.setText(constant.STATUS_LABEL_MOVING)
                    self.threadMove = ThreadMove(index=index)
                    self.threadMove.mainThread.connect(self.main_controller)
                    self.threadMove.start()
                else:
                    pass

        elif sender == 'ThreadArduino':
            if info[constant.STATUS] == constant.FAIL:
                logging.error('ThreadArduino ' + info[constant.STATUS])
            else:
                # activate buzzer if bin is full
                self.activate_buzzer(info['bin_full'])

                # use predict if detected object
                if not self.motor_enable:
                    logging.debug('motor is not enable')
                elif self.is_moving:
                    logging.debug('motor is moving, need to wait')
                # if machine is not free, detect object
                elif self.object_exist:
                    logging.debug('object is exist, need to wait')

                # machine is free to detect new object
                else:
                    if info['object'][0:6] != b'111111':
                        if self.smart_detect==True:
                            # smart detect is on, classify object from sensor
                            self.arduino_commu_lock.acquire()
                            logging.info('arduino detect:' + str(info['object']))

                            self.object_exist_lock.acquire()
                            self.object_exist = True
                            self.object_exist_lock.release()

                            if info['object'][0:1] == b'0':
                                self.move_trash_to_bin(constant.TRASH_recycle)
                            elif info['object'][1:2] == b'0':
                                self.move_trash_to_bin(constant.TRASH_kitchen)
                            elif info['object'][2:3] == b'0':
                                self.move_trash_to_bin(constant.TRASH_other)
                            elif info['object'][3:6] != b'111':
                                self.move_trash_to_bin(constant.TRASH_harmful)
                            else:
                                logging.info('no info about trash from sensor')
                                self.object_exist_lock.acquire()
                                self.object_exist = False
                                self.object_exist_lock.release()

                            self.arduino_commu_lock.release()
                        else:
                            # smart detect is not open,use K210 to classify
                            self.object_exist_lock.acquire()
                            self.object_exist = True
                            self.object_exist_lock.release()

                    else:
                        logging.debug('no object')


        elif sender == 'ThreadBuzzer':
            if info[constant.STATUS] == constant.FAIL:
                logging.error('ThreadBuzzer ' + info[constant.STATUS])
            else:
                pass

        else:
            logging.error('unknown sender')

    def move_trash_to_bin(self, class_name):
        logging.info('move trash to bin ' + class_name)
        # map trash to a bin
        index = 0
        for m in config.bin_map:
            if (class_name == m[2]):
                index = m[0]
        # increase count
        self.bin_count_lock.acquire()
        self.bin_count[index] += 1
        self.bin_count_lock.release()
        self.last_class_lock.acquire()
        self.last_class = class_name
        self.last_class_lock.release()

        # move trash to specific bin
        self.is_moving_lock.acquire()
        self.is_moving = True
        self.is_moving_lock.release()
        self.status_label.setText(constant.STATUS_LABEL_MOVING)
        self.threadMove = ThreadMove(index=index)
        self.threadMove.mainThread.connect(self.main_controller)
        self.threadMove.start()

    def update_count_label(self):
        for i in range(0, 4):
            self.count_label[i].setText(str(self.bin_count[i]))

    def update_full_label(self, state):
        for i in range(0, 4):
            if state[i:i+1] == b'1':
                self.capacity_label[i].setText(constant.FULL)
            else:
                self.capacity_label[i].setText(constant.UN_FULL)

    def activate_buzzer(self, bin_full):
        #self.update_full_label(bin_full)
        
        is_full = False
        if bin_full != b'0000':
            is_full = True

        # The state machine
        if is_full and self.buzzer_full_count < config.full_counts:
            self.buzzer_full_count += 1
        elif (not is_full) and self.buzzer_full_count > 0:
            self.buzzer_full_count -= 1
        turn_on = False
        if self.buzzer_full_count == config.full_counts:
            turn_on = True

        if turn_on:
            if not self.is_buzzer_on:
                #self.update_full_label(bin_full)
                logging.info('turn on buzzer')
                self.buzzer_state.acquire()
                self.is_buzzer_on = True
                self.buzzer_state.release()
                buzzer_on()
                logging.info('1_bin_full:'+str(bin_full))
                self.update_full_label(bin_full)
                
                '''
                self.threadBuzzer = ThreadBuzzer()
                self.threadBuzzer.mainThread.connect(self.main_controller)
                self.threadBuzzer.start()
                '''
        if not turn_on:
            if self.is_buzzer_on:
                #self.update_full_label(bin_full)
                logging.info('turn off buzzer')
                self.buzzer_state.acquire()
                self.is_buzzer_on = False
                self.buzzer_state.release()
                buzzer_off()
                logging.info('2_bin_full:'+str(bin_full))
                self.update_full_label(b'0000')
                '''
                self.is_buzzer_on = False
                if not self.threadBuzzer.isFinished():
                    self.threadBuzzer.exit()
                '''

    def error_handler(self):

        pass

    def keyPressEvent(self, event):
        logging.info('keyborad event:' + str(event.key()))
        if event.key() == QtCore.Qt.Key_Escape:
            logging.info('app exit!!!')
            app = QApplication.instance()
            app.quit()
            pass


# receive Arduino thread
class ThreadArduino(QThread):
    mainThread = PQC.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ThreadArduino, self).__init__(parent)
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        except:
            logging.error('can not open serial port')
            logging.error(traceback.format_exc())

    def __del__(self):
        logging.error('ThreadArduino is aborted')

    def run(self):
        info = {'sender': 'ThreadArduino'}

        try:
            while True:
                re = self.ser.readline()
                if re == b'' or len(re) != 13:
                    logging.debug('Arduino data is wrong')
                    info[constant.STATUS] = constant.FAIL
                else:
                    info['object'] = re[0:8]
                    info['bin_full'] = re[8:12]
                    # logging.info(str(info['bin_full']))
                    logging.debug('Arduino data:' + re.decode('utf-8'))
                    info[constant.STATUS] = constant.SUCCESS
                self.mainThread.emit(info)
        except:
            logging.error('ThreadArduino error')
            logging.error(traceback.format_exc())
            info[constant.STATUS] = constant.FAIL
            self.mainThread.emit(info)
            self.ser.close()


# receive Arduino thread
class ThreadK210(QThread):
    mainThread = PQC.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ThreadK210, self).__init__(parent)
        try:
            self.ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
        except:
            logging.error('can not open serial port')
            logging.error(traceback.format_exc())

    def __del__(self):
        logging.error('ThreadK210 is aborted')

    def run(self):
        info = {'sender': 'ThreadK210'}

        try:
            while True:
                re = self.ser.readline()
                if re == b'':
                    logging.debug('K210 data is null')
                    info[constant.STATUS] = constant.FAIL
                else:
                    re = re.decode('utf-8')[:-1]
                    logging.debug('K210 data:' + re)
                    info[constant.STATUS] = constant.SUCCESS
                    info['K210'] = re
                self.mainThread.emit(info)
        except:
            logging.error('ThreadK210 error')
            logging.error(traceback.format_exc())
            info[constant.STATUS] = constant.FAIL
            self.mainThread.emit(info)
            self.ser.close()


# motor move thread
class ThreadMove(QThread):
    mainThread = PQC.pyqtSignal(dict)

    def __init__(self, parent=None, index=0):
        super(ThreadMove, self).__init__(parent)
        self.index = index
        pass

    def __del__(self):
        logging.info('ThreadMove is aborted')
        pass

    def run(self):
        info = {'sender': 'ThreadMove'}
        try:
            time.sleep(config.fly_delay)
            moveto(self.index)
            info[constant.STATUS] = constant.SUCCESS
        except:
            logging.error('ThreadMove error')
            logging.error(traceback.format_exc())
            info[constant.STATUS] = constant.FAIL

        self.mainThread.emit(info)


# buzzer thread
class ThreadBuzzer(QThread):
    mainThread = PQC.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ThreadBuzzer, self).__init__(parent)
        pass

    def __del__(self):
        logging.info('ThreadBuzzer deleted')

    def run(self):
        info = {'sender': 'ThreadBuzzer'}

        try:
            buzzer_loop(config.buzzer_delay)
        except:
            logging.error('ThreadBuzzer error')
            logging.error(traceback.format_exc())
            info[constant.STATUS] = constant.FAIL
            self.mainThread.emit(info)
