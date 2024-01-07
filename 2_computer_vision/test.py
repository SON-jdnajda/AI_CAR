import numpy as np
import matplotlib.pyplot as plt
import cv2
# Hàm lọc màu sử dụng phương pháp Otsu
def otsu_threshold(image):
    # Chuyển đổi ảnh sang ảnh xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Áp dụng phương pháp Otsu để tìm ngưỡng tốt nhất
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Tạo ảnh nhị phân 3 kênh màu (RGB)
    binary_image_rgb = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)

    return binary_image_rgb

# Hàm chính
if __name__ == "__main__":
    # Đọc ảnh từ file và chuyển đổi không gian màu
    image_bgr = cv2.imread("2_computer_vision/image_from_sim.png")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Ảnh nhị phân sử dụng phương pháp Otsu
    binary_image_otsu = otsu_threshold(image_rgb)

    # Hiển thị ảnh gốc và ảnh nhị phân sử dụng phương pháp Otsu
    f, axarr = plt.subplots(1, 2)
    axarr[0].title.set_text("Original")
    axarr[0].imshow(image_rgb)
    axarr[1].title.set_text("After Otsu threshold")
    axarr[1].imshow(binary_image_otsu)
    plt.show()
