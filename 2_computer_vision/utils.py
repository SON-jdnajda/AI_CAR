# Import các thư viện cần thiết
from numpy.lib.function_base import average
from controller import Robot
from controller import Camera
from controller import Display
from vehicle import Car
import numpy as np
import cv2
import cProfile
import io
import pstats

# Hàm decorator để sử dụng cProfile để profile một hàm khác
def profile(fnc):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner

# Hàm để lấy ảnh từ camera
def get_image(camera):
    raw_image = camera.getImage()  # Hàm này chiếm phần lớn thời gian CPU
    image = np.frombuffer(raw_image, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4)
    )
    return image

# Hàm tính sự khác biệt pixel giữa hai pixel
def pixel_difference(pixel1, pixel2):
    squared_dist = np.sum((pixel1 - pixel2) ** 2, axis=0)
    return np.sqrt(squared_dist)

# Hàm lọc màu sử dụng phương pháp tùy chỉnh
def colour_threshold(image, colour):
    binary_image = np.zeros(image.shape, dtype=np.uint8)
    binary_image[:][:][4] = 255  # kênh alpha
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            pixel = image[r][c][:-1]
            difference = pixel_difference(colour, pixel)
            if difference < 50:  # 30 từ mã nguồn C
                binary_image[r][c][:-1] = 255
    return binary_image

# Hàm lọc màu sử dụng OpenCV
def colour_threshold_cv2(image, colour, error):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = colour - error / 2
    higher = colour + error / 2
    mask = cv2.inRange(hsv, lower, higher)
    return mask

# Hàm tính trung bình cột chuẩn hóa của ảnh nhị phân
def calculate_normalized_average_col(binary_image):
    th_idx = np.where(binary_image == 255)
    if not th_idx:
        print("WARNING: Binary image ALL zeros")
        return None, None  # TODO: cải thiện
    else:
        average_column = np.average(th_idx[1])
        normalized_column = (
            average_column - binary_image.shape[1] / 2
        ) / binary_image.shape[1]
        return normalized_column, int(average_column)

# Hàm hiển thị ảnh nhị phân với cột trung bình được làm nổi bật
def display_binary_image(display_th, binary_image, average_column):
    binary_image_gbra = np.dstack(
        (
            binary_image,
            binary_image,
            binary_image,
        )
    )
    binary_image_gbra[:, average_column, 0] = 255  # màu đỏ
    binary_image_gbra[:, average_column, 1] = 0  # màu xanh lá cây
    binary_image_gbra[:, average_column, 2] = 0  # màu xanh dương
    image_ref = display_th.imageNew(
        binary_image_gbra.tobytes(),
        Display.RGB,
        width=binary_image_gbra.shape[1],
        height=binary_image_gbra.shape[0],
    )
    display_th.imagePaste(image_ref, 0, 0, False)

# Hàm chính
if __name__ == "__main__":
    # Đọc một ảnh từ file
    image = cv2.imread("image.png")

    # Định nghĩa một khoảng màu vàng trong định dạng HSV
    yellow_pixel = np.array([25, 127, 127])
    error = np.array([5, 255, 255])

    # Áp dụng lọc màu sử dụng OpenCV
    binary_image = colour_threshold_cv2(image, yellow_pixel, error)
    
    # Tính cột trung bình chuẩn hóa từ ảnh nhị phân
    normalized_column, average_column = calculate_normalized_average_col(binary_image)

    # Hiển thị ảnh nhị phân
    cv2.imshow("binary image", binary_image)
    cv2.waitKey()
