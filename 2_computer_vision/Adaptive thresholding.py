# Import các thư viện cần thiết
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Hàm chính
if __name__ == "__main__":
    # Đọc ảnh từ file và chuyển đổi không gian màu
    image_bgr = cv2.imread("2_computer_vision/image_from_sim.png")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Chuyển ảnh sang ảnh đa cấp độ xám
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Phân ngưỡng động
    adaptive_threshold = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # Hiển thị ảnh gốc và ảnh sau khi áp dụng phân ngưỡng động
    f, axarr = plt.subplots(1, 2)
    axarr[0].title.set_text("Original")
    axarr[0].imshow(image_rgb)
    axarr[1].title.set_text("After Adaptive Thresholding")
    axarr[1].imshow(adaptive_threshold, cmap='gray')
    plt.show()
