import os
import shutil
import random
import myconfig

# 清空图像
def remove_all(delete_dir):
    print('delete ', delete_dir)
    dirs = os.listdir(delete_dir)
    print('delete', dirs)
    for dir in dirs:
        images = os.listdir(delete_dir + dir)
        for i in images:
            # print(i)
            os.remove(delete_dir + dir + '/' + i)
    pass


def show_stats(source_data_dir):
    print(source_data_dir)
    total = 0
    classes = os.listdir(source_data_dir)
    for c in classes:
        images = os.listdir(source_data_dir + c)
        print(c + " :" + str(len(images)))
        total+=len(images)
    print('total :'+str(total))
    pass


def img_shutil(source_data_dir, test_ratio, train_dir, test_dir):
    # print('img_shutil')
    classes = os.listdir(source_data_dir)
    for c in classes:
        num = 1
        images = os.listdir(source_data_dir + c)

        test_list = []
        test_count = 0

        # select test images
        while True:
            # print(test_count, (len(images) * test_ratio))
            if test_count >= (len(images) * test_ratio):
                break
            test_image = images[random.randint(0, len(images)-1)]
            if test_image not in test_list:
                print(test_image)
                test_list.append(test_image)
                test_count += 1
            else:
                pass
        print(test_list)

        # copy images to dirs
        for image in images:
            if image not in test_list:
                print(image)
                shutil.copy(source_data_dir + c + '/' + image, train_dir + c)
            else:
                print(image)
                shutil.copy(source_data_dir + c + '/' + image, test_dir + c)
            num += 1
    pass


if __name__ == '__main__':
    # show_stats(myconfig.data_dir)
    # print(len(os.listdir(myconfig.data_dir)))

    show_stats('data/game_data_v4/')
    print(len(os.listdir('data/game_data_v4/')))


    pass
