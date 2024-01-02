# Import các thư viện cần thiết
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Hàm tính sự khác biệt pixel giữa hai pixel(khoảng cách Euclidean)
def pixel_difference(pixel1, pixel2):
    squared_dist = np.sum((pixel1 - pixel2) ** 2, axis=0)
    return np.sqrt(squared_dist)

# Hàm lọc màu sử dụng phương pháp tùy chỉnh
def colour_threshold(image, colour, threshold):
# Dòng này tạo một mảng NumPy mới có hình dạng giống như hình ảnh đầu vào nhưng khởi tạo nó dưới dạng một mảng hoàn toàn bằng 0. Kiểu dữ liệu của mảng được đặt thành số nguyên 8 bit không dấu ( np.uint8).
    binary_image = np.zeros(image.shape, dtype=np.uint8) 
# Dòng này đặt giá trị kênh alpha của tất cả các pixel trong ảnh nhị phân thành 255. Nhận xét cho biết giá trị này tương ứng với kênh alpha.
    binary_image[:][:][4] = 255  # kênh alpha
# Các vòng lặp lồng nhau này lặp qua từng hàng ( r) và từng cột ( c) của hình ảnh đầu vào.
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
# Dòng này trích xuất các giá trị màu của pixel hiện tại.
            pixel = image[r][c][:]
            difference = pixel_difference(colour, pixel)
# Nếu chênh lệch được tính toán dưới ngưỡng được chỉ định thì pixel tương ứng trong ảnh nhị phân được đặt thành màu trắng (255) cho tất cả các kênh màu ngoại trừ kênh màu cuối cùng (kênh alpha).
            if difference < threshold:
                binary_image[r][c][:-1] = 255        
    return binary_image

# Hàm chính
if __name__ == "__main__":
    # Đọc ảnh từ file và chuyển đổi không gian màu
    image_bgr = cv2.imread("2_computer_vision/image_from_sim.png")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Ảnh nhị phân
    yellow_pixel = np.array([25, 127, 127])  # màu vàng trong không gian màu HSV
    threshold = 40  # TODO: sửa giá trị này và hiểu rõ những thay đổi
    binary_image = colour_threshold(image_hsv, yellow_pixel, threshold)

    # Hiển thị ảnh gốc và ảnh nhị phân
    f, axarr = plt.subplots(1, 2)
    axarr[0].title.set_text("Original")
    axarr[0].imshow(image_rgb)
    axarr[1].title.set_text("After threshold")
    axarr[1].imshow(binary_image)
    plt.show()
