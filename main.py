import cv2 as cv
import numpy as np
import random
import time


def main():
    img = cv.imread("img.png", 1)
    c_img = edge_detection(img)
    division_list = division(c_img, 8)
    coordinate_list = coordinate(division_list)
    polygon_map = polygon(coordinate_list)
    trim_polygon_map = polygon_map[256:2048, 256:2048]
    cv.imwrite("./rendered/rendered.png", trim_polygon_map)


def edge_detection(self):
    img_blur = cv.GaussianBlur(self, ksize=(5, 5), sigmaX=3)
    c_img = cv.Canny(img_blur, 50, 120)
    return c_img


def division(self, uv_division):
    height, width = self.shape
    division_list = []

    div_num = int(height / uv_division)
    count = 0
    black = cv.imread("./data/base2.png", 0)
    for h in range(uv_division + 2):
        for w in range(uv_division + 2):
            if h == 0 or h == 9 or w == 0 or w == 9:
                img = black
            else:
                img = self[(h - 1) * div_num:(h - 1) * div_num + div_num,
                      (w - 1) * div_num:(w - 1) * div_num + div_num]
            division_list.append(img)
            count += 1
    return division_list


def division_color(self, uv_division):
    height, width, ch = self.shape
    division_list = []

    div_num = int(height / uv_division)
    for h in range(uv_division):
        for w in range(uv_division):
            img = self[h * div_num:h * div_num + div_num,
                  w * div_num:w * div_num + div_num]
            division_list.append(img)
    return division_list


def coordinate(self):
    random_list = []
    global_random_list = []
    count = 0
    for i in self:
        fuga = coordinate_pick(i)
        x_panel = count % 10
        y_panel = count // 10

        if len(fuga) < 1:
            x = random.randrange(0, 255)
            y = random.randrange(0, 255)
            random_list.extend([[x + 256 * x_panel, y + 256 * y_panel]])
        else:
            random_pick = random.randrange(0, len(fuga))
            random_list.extend([[fuga[random_pick][0] + 256 * x_panel,
                                 fuga[random_pick][1] + 256 * y_panel]])
        global_random_list.extend([random_list])
        random_list = []
        count += 1
    return global_random_list


def coordinate_pick(self):
    height, width = self.shape
    white_coordinate = []
    for i in range(height):
        for j in range(width):
            if self[i, j] == 255:
                white_coordinate.append([i, j])
    return white_coordinate


def polygon(self):
    base = cv.imread("./data/base.png", 1)
    img = cv.imread("img.png", 1)
    base[0, 0] = [255, 255, 255]
    base = cv.resize(base, (2560, 2560))
    count = 0
    for i in range(len(self)):
        for j in range(len(self[i])):
            if i < 10 or (i + 1) % 10 == 0 or i % 10 == 0 or i > 89:
                count += 1
            else:
                if 10 <= i <= 19 or (i - 1) % 10 == 0 or (
                        i + 2) % 10 == 0 or 90 <= i <= 99:
                    color_list = []
                    for k in range(7):
                        x = random.randrange(0, 2047)
                        y = random.randrange(0, 2047)
                        random_color = img[x, y]
                        b, g, r = map(int, random_color)
                        if b > 220:
                            b -= 30
                        if g > 220:
                            g -= 30
                        if r > 220:
                            r -= 30
                        color = [b, g, r]
                        color_list.append(color)
                    base = draw(self, base, i, color_list)
                else:
                    div_img = division_color(img, 8)
                    pic = div_img[i - count]
                    # こ↑こ↓
                    color_list = []
                    for k in range(7):
                        x = random.randrange(0, 255)
                        y = random.randrange(0, 255)
                        bgr = pic[x, y]
                        b, g, r = map(int, bgr)
                        color = [b, g, r]
                        color_list.append(color)
                    base = draw(self, base, i, color_list)
    return base


def draw(self, base, i, color):
    x, y = map(int, self[i][0])
    x_1, y_1 = map(int, self[i - 11][0])
    x_2, y_2 = map(int, self[i - 10][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[0])

    x_1, y_1 = map(int, self[i - 10][0])
    x_2, y_2 = map(int, self[i - 9][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[1])

    x_1, y_1 = map(int, self[i - 11][0])
    x_2, y_2 = map(int, self[i - 1][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[2])

    x_1, y_1 = map(int, self[i - 1][0])
    x_2, y_2 = map(int, self[i + 9][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[3])

    x_1, y_1 = map(int, self[i + 9][0])
    x_2, y_2 = map(int, self[i + 10][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[4])

    x_1, y_1 = map(int, self[i + 10][0])
    x_2, y_2 = map(int, self[i + 11][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[5])

    x_1, y_1 = map(int, self[i + 11][0])
    x_2, y_2 = map(int, self[i + 1][0])
    pts = np.array(((x, y), (x_1, y_1), (x_2, y_2)))
    cv.fillPoly(base, [pts], color[6])

    cv.imwrite("./progress/rendered{}.png".format(i), base)
    return base


if __name__ == "__main__":
    start = time.time()
    main()
    print("実行時間 : {} sec".format(time.time() - start))
