from motor.motor import motor_setup, moveto, motor_destroy
import time

if __name__ == "__main__":
    print('motor test')
    test_num = 1

    motor_setup()
    try:
        # moveto(0)
        start = time.time()
        for i in range(0, test_num):
            for index in range(0, 4):
                moveto(index)
        end = time.time()

        print('trash count:', test_num * 4)
        print('time cost:', end - start)

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
        motor_destroy()
