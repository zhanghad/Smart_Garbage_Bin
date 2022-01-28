import cv2

cap = cv2.VideoCapture(0)

'''
width=640
height=480
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)#设置图像宽度
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#设置图像高度
'''

# 显示图像
while True:
    ret, frame = cap.read()  # 读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
    print(frame.shape)
    # img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#转灰度图
    # cv2.imshow("img",img)
    cv2.imshow("frame", frame)  # 图像不处理的情况

    input = cv2.waitKey(20)
    if input == ord('q'):  # 如过输入的是q就break，结束图像显示，鼠标点击视频画面输入字符
        break

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 销毁窗口
