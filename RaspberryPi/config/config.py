"""
    config files, to control the app

    author:zhanghad
    qq:1310200276
"""

'''ui relevant parameters'''
screen_size = (1024, 768)  # width,height

'''supersonic relevant parameters'''
bar_min = 0
bar_max = 42
bins_empty = [40, 40, 40, 40]
bins_full = [10, 10, 10, 10]
bin_max = 24
sonic_max = 40
full_counts = 100

'''motor relevant parameters'''
# motor 1(bottom) GPIO
motor_1_1 = 38  # PUL-
motor_1_2 = 40  # PUL+
motor_1_3 = 37  # DIR-
motor_1_4 = 35  # DIR+
# motor 2(up) GPIO
motor_2_1 = 31  # PUL- 31
motor_2_2 = 29  # PUL+ 29
motor_2_3 = 33  # DIR- 33
motor_2_4 = 32  # DIR+ 32
# motor delay
motor_move_delay = 0.00015
motor_stop_delay = 0.20

'''buzzer relevant parameters'''
buzzer = 12
buzzer_delay = 0.5

'''trash in to detect'''
fly_delay=0.3

'''predict relevant parameters'''
harmful_trash = {'battery','cell'}
kitchen_trash = {'fruit', 'apple', 'banana', 'kitchen', 'orange', 'pepper','carrot','potato'}
recycle_trash = {'paper', 'can', 'bottle', 'metal', 'cardboard', 'plastic'}
other_trash = {'cigarette', 'brick','background'}
#base_line = 0.5
'''
3 2
0 1
0 is default
'''
# trash map to bin
bin_map = [(2, harmful_trash, '有害'), (1, kitchen_trash, '厨余'), (0, recycle_trash, '可回收'), (3, other_trash, '其他')]


# control
smart_detect=True
motor_enable=True