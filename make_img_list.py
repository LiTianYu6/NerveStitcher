import os

def make_img_list(img_dir, list_dir):
    '''
    生成待拼接图像stitching_list.txt文件
    img_dir:图像文件路径
    '''
    img_list = os.listdir(img_dir)
    img_name = []

    for i in img_list:
        if i.endswith('.jpg'):
            img_name.append(i)
    img_name.sort(key=lambda x: int(x[4:-4]))  # 从正数第四个字符到倒数第四个字符中间的数字排序
    first_name = img_name[0]
    for name in img_name[1:]:
        with open("%s" % list_dir, "a") as file:
            file.write(first_name + " " + name + '\n')
        first_name = name
        file.close()
    print("已成功生成待拼接图像列表: " + list_dir)