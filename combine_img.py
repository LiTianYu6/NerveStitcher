import numpy as np
import cv2
import os

from PIL import Image
from pathlib import Path

def calculate_img_size(x_move, y_move):
    '''
    x: 左加右减
    y: 上加下减
    '''
    # print(x_move,y_move)
    x, x_min, x_max = 0, 0, 0
    y, y_min, y_max = 0, 0, 0
    for i in range(len(x_move)):
        x += x_move[i]
        if x_min > x:
            x_min = x
        if x_max < x:
            x_max = x
    # print(x_min, x_max)
    for i in range(len(y_move)):
        y += y_move[i]
        if y_min > y:
            y_min = y
        if y_max < y:
            y_max = y
    # print(y_min, y_max)

    sum_x = abs(x_max) + abs(x_min)
    sum_y = abs(y_max) + abs(y_min)

    if x_min< 0 and x_max > 0:
        x = sum_x - abs(x_min)
    else:
        x = x_max

    if y_min< 0 and y_max > 0:
        y = sum_y - abs(y_min)
    else:
        y = y_max
    # print(x, y)
    return int(sum_x), int(sum_y), int(x), int(y)


def create_img(img_size, sum_x, sum_y):
    """
    img_size：图像原尺寸
    sum_x：图像x轴增长尺寸
    sum_y：图像y轴增长尺寸
    """
    bg_img = np.zeros((img_size[1] + sum_y, img_size[0] + sum_x, 3), dtype=np.uint8)  # 注意此处x，y是相反的,矩阵由(列x行)表示

    return bg_img


def combine_first_img(img, bg_img, x, y):
    """
    img：待拼接图像
    bg_img：背景图像（全黑色）
    注意！！！bg_img是由行x列组成（x,y），左上角为坐标原点。
    """
    bg_img = Image.fromarray(np.uint8(bg_img))
    img = Image.fromarray(np.uint8(img))
    bg_img.paste(img, (x, y))
    bg_img = np.asarray(bg_img)  # 得到含有初始图像的背景图像
    center_point = [x, y]

    return center_point, bg_img


def combine_image(input_dir, bg_img, count, x_move, y_move, center_point):
    '''
    count:拼接图像计数器，用于拼接失败时断续重拼，防止pairs重复读取.txt文件之前的图像

    由于x_move, y_move中为“左加右减，上加下减”策略，移动图像过程中需明确：
    ①右上移动时，从(0, sum_y)开始，x逐渐增大，y逐渐减小 ----> x_move[i]取反,y_move[i]取反
    ②右下移动时，从(0, 0)开始，x逐渐增大，y逐渐增大 ----> x_move[i]取反,y_move[i]取反
    ③左下移动时，从(sum_x, sum_y)开始，x逐渐减小，y逐渐增加 ----> x_move[i]取反,y_move[i]取反
    ④左上移动时，从(sum_x, 0)开始，x逐渐减小，y逐渐减小 ----> x_move[i]取反,y_move[i]取反
    总结：x_move[i]取反,y_move[i]取反
    '''
    if not os.path.exists(input_dir + '/result/'):
        os.makedirs(input_dir + '/result/')

    input_pairs_path = input_dir + "stitching_list.txt"
    with open(input_pairs_path, 'r') as f:
        pairs = [l.split() for l in f.readlines()]
    p = count
    for i in range(len(x_move)):
        temp_count, pair = list(enumerate(pairs))[count + i]
        # print(temp_count, pair)
        name0, name1 = pair[:2]
        # 只需要list中第二列图像(待拼接图像)
        img1 = cv2.imread(input_dir + '%s' % name1)
        img1 = Image.fromarray(np.uint8(img1))
        bg_img = Image.fromarray(np.uint8(bg_img))
        center_point[0] += -np.int(x_move[i])
        center_point[1] += -np.int(y_move[i])
        bg_img.paste(img1, (center_point[0], center_point[1]))
        bg_img = np.asarray(bg_img)  # 得到拼接图像
        p = temp_count

        cv2.imwrite(input_dir + '/result/result%i.jpg' % temp_count, bg_img)

    count = p + 2  # 从0开始+1，跳过错误拼接组+1，共+2

    return count, bg_img


def combine(img_first_stitching, x_move, y_move, input_dir, count):
    sum_x, sum_y, x, y = calculate_img_size(x_move, y_move)
    bg_img = create_img([384, 384], sum_x, sum_y)
    center_point, bg_img = combine_first_img(img_first_stitching, bg_img, x, y)
    count, result_img = combine_image(input_dir, bg_img, count, x_move, y_move, center_point)

    return count, result_img