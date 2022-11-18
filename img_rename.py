import os
import shutil
import time



def rename(read_directory, save_directory):
    img_list = []
    filelist = os.listdir(read_directory)
    for filename in filelist:
        if filename.endswith('.jpg'):
            img_list.append(filename)
        elif filename.endswith('.tif'):
            img_list.append(filename)
    i = 1  # 表示文件的命名是从1开始的
    for item in img_list:
        src = os.path.join(os.path.abspath(read_directory), item)
        dst = os.path.join(os.path.abspath(save_directory),
                           new_name + str(i) + '.jpg')  # 可以修改图片格式
        print(os.path.abspath(save_directory), new_name + str(i) + '.jpg')

        shutil.copy(src, dst)
        with open("%s" % save_directory + ".txt", "a") as file:
            file.write(item + " " + new_name + str(i) + '.jpg' + '\n')
        file.close()

        i = i + 1


if __name__ == '__main__':
    # t1 = time.time()
    read_directory = "data/test/Original image"
    save_directory = r"data/test/image"
    if os.path.exists(save_directory + ".txt"):  # 删除之前的重命名文件
        os.remove(save_directory + ".txt")
    new_name = "test"
    rename(read_directory, save_directory)
    # t2 = time.time()
    # print("重命名耗时：{0}".format(t2-t1))