import cv2
import sys
import os
import math
import numpy as np
# from scipy.ndimage import gaussian_filter1d
from histogram_matching import ExactHistogramMatcher
import time


def check_monotonically_increase(parameter_tup):
    """Check if a, b, c could let g(r) monotonically increase in [0,1]"""

    a, b, c = parameter_tup
    if c == 0:
        if a >= 0 and a + 2 * b >= 0 and not(a == 0 and b == 0):
            return True
        return False
    if c < 0:
        if b**2 > 3 * a * c:
            q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            if q_plus <= 0 and q_minus >= 1:
                return True
        return False
    if c > 0:
        if b**2 < 3 * a * c:
            return True
        elif b**2 == 3 * a * c:
            if b >= 0 or 3 * c + b <= 0:
                return True
        else:
            q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            if q_plus <= 0 or q_minus >= 1:
                return True
        return False


def calc_discrete_entropy(cm_x, cm_y, max_distance, parameter_tup, im, distance):
    """
    Calculate the discrete entropy after the brightness of the picture is
    adjusted by the gain function with given parameters
    """

    # print(parameter_tup)

    a, b, c = parameter_tup
    row, col = im.shape

    histogram = [0 for i in range(256)]
    # histogram = [0 for i in range(8)]

    count = 0
    for i in range(col):
        for j in range(row):
            # calculate the distance from the current pixel to picture's center of mass and the corresponding r value
            # distance = math.sqrt((i - cm_x)**2 + (j - cm_y)**2)
            r = distance[count] / max_distance
            count += 1

            # evaluate the gain function and adjust pixel luminance value
            g = 1 + a * r**2 + b * r**4 + c * r**6
            intensity = im[j, i] * g

            # map the luminance value to the corresponding histogram bins

            bin = 255 * math.log(1 + intensity) / math.log(256)
            # bin = 7 * math.log(1 + intensity) / math.log(256)
            floor_bin = math.floor(bin)
            ceil_bin = math.ceil(bin)

            # if the luminance value exceeds 255 after adjustion, simply add histogram bins at the upper end
            if bin > len(histogram) - 1:
                for k in range(len(histogram), ceil_bin + 1):
                    histogram.append(0)

            histogram[floor_bin] += 1 + floor_bin - bin
            histogram[ceil_bin] += ceil_bin - bin

    # Use Gausssian kernel to smooth the histogram
    # histogram = gaussian_filter1d(histogram, 4)

    histogram_sum = sum(histogram)
    H = 0

    # Calculate discrete entropy
    for i in range(len(histogram)):
        p = histogram[i] / histogram_sum
        if p != 0:
            H += p * math.log(p)

    # print(H)

    return -H


def find_parameters(cm_x, cm_y, max_distance, im, distance):
    """
    Find a, b, c that could minimize the entropy of the image, given the
    image's cenrter of mass and the distance from the image's farthest vertex
    to center of mass
    """
    x = []
    y = []
    t = 0

    a = b = c = 0
    delta = 2
    min_H = None

    # set up a explored set to optimize running time
    explored = set()

    while delta > 1 / 128:
        initial_tup = (a, b, c)

        for parameter_tup in [(a + delta, b, c), (a - delta, b, c),
                              (a, b + delta, c), (a, b - delta, c),
                              (a, b, c + delta), (a, b, c - delta)]:

            if parameter_tup not in explored:
                explored.add(parameter_tup)

                if check_monotonically_increase(parameter_tup):
                    curr_H = calc_discrete_entropy(
                        cm_x, cm_y, max_distance, parameter_tup, im, distance)
                    t += 1
                    x.append(t)
                    y.append(curr_H)
                    # if the entropy is lower than current minimum, set parameters to current ones
                    if min_H is None or curr_H < min_H:
                        min_H = curr_H
                        a, b, c = parameter_tup

        # if the current parameters minimize the entropy with the current delta, reduce the delta
        if initial_tup == (a, b, c):
            delta /= 2

    return a, b, c, x, y


def vignetting_correction(im):
    """
    Correct the vignetting of the image with the parameters that could minimize
    the discrete entropy.
    """

    # convert rgb image to grayscale
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    row, col = imgray.shape

    cm_x = 192
    cm_y = 192
    max_distance = math.sqrt(max(
        (vertex[0] - cm_x)**2 + (vertex[1] - cm_y)**2 for vertex in [[0, 0], [0, row], [col, 0], [col, row]]))

    distance = []
    for i in range(col):
        for j in range(row):
            distance.append(math.sqrt((i - cm_x)**2 + (j - cm_y)**2))

    # a, b, c, x, y = find_parameters(cm_x, cm_y, max_distance, imgray, distance)
    a, b, c = 0.0625, 1.75, -0.75
    print("参数：", a, b, c)
    count = 0
    # modify the original image
    ta = time.time()
    for x in range(col):
        for y in range(row):
            r = distance[count] / max_distance
            count += 1
            g = 1 + a * r**2 + b * r**4 + c * r**6
            modified = imgray[y, x] * g
            # # if the brightness after modification is greater than 255, then set the brightness to 255
            # if modified > 255:
            #     modified = 255
            # imgray[y, x] = modified
            imgray[y, x] = modified if modified < 255 else 255
    tb = time.time()
    print("xy耗时：{0}".format(tb - ta))
    return imgray


if __name__ == '__main__':
    t1 = time.time()
    path = r'data/test/image'
    savepath = r"data/test/stitch_img"
    reference_img = cv2.imread('data/reference.jpg')
    filelist = os.listdir(path)
    filelist.sort(key=lambda x: int(x[4:-4]))  # 从正数第四个字符到倒数第四个字符中间的数字排序
    num = 0
    for filename in filelist:
        img = cv2.imread(os.path.join(path, filename))
        # 直方图规定化
        t2 = time.time()
        reference_histogram = ExactHistogramMatcher.get_histogram(reference_img)
        img = ExactHistogramMatcher.match_image_to_histogram(img, reference_histogram)
        img = img.astype(np.uint8)
        # 渐晕校正
        t3 = time.time()
        img = vignetting_correction(img)
        cv2.imwrite(savepath + "/" + os.path.basename(filename), img)
        num += 1
        t4 = time.time()
        print("已处理成功：", num)
        print("规定化耗时：{0}".format(t3-t2), "渐晕耗时：{0}".format(t4-t3))
    print("共处理：", num, "张图片","共耗时：{0}".format(t4-t1))




