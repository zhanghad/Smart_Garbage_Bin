from sensor.buzzer import buzzer_setup, buzzer_loop,buzzer_destroy,buzzer_off

if __name__ == '__main__':
    buzzer_setup()  # 设置GPIO管脚
    buzzer_off()
    '''
    try:  # 检测异常
        buzzer_loop(0.5)  # 调用循环函数
    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序
        buzzer_destroy()  # 释放资源
    '''
