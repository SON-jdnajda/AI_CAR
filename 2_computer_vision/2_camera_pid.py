# Import các thư viện và module cần thiết
from controller import Display
from vehicle import Car
from vehicle import Driver
import utils  # Đây là module tự định nghĩa, được giả định rằng nó chứa các hàm hỗ trợ
import numpy as np

# Hàm chính
def main():
    # Tạo đối tượng Robot (xe)
    robot = Car()
    driver = Driver()

    # Lấy time step của thế giới hiện tại
    timestep = int(robot.getBasicTimeStep())

    # Tạo đối tượng camera và kích hoạt camera
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # Kích hoạt hiển thị ngưỡng
    display_th = Display("display_th")

    # Định nghĩa màu vàng trong không gian màu HSV
    yellow_pixel = np.array([25, 127, 127])  # HSV
    error = np.array([8, 80, 80])  # giá trị lỗi trên 80 (phát hiện cây bụi)

    # Vòng lặp chính
    while robot.step() != -1:
        # Lấy ảnh từ camera
        image = utils.get_image(camera)

        # Xử lý ảnh (tạo ảnh nhị phân)
        binary_image = utils.colour_threshold_cv2(image, yellow_pixel, error)

        # Chuẩn hóa cột [-0.5, 0.5]
        normalized_column, average_column = utils.calculate_normalized_average_col(binary_image)
        angle = normalized_column * 1.0  # TODO: cần điều chỉnh

        # In thông tin về cột đã chuẩn hóa và góc lái
        print(f"INFO: normalized column {normalized_column:.2f}")
        print(f"INFO: angle {angle:.2f}")

        # Hiển thị ảnh nhị phân với cột trung bình làm nổi bật
        utils.display_binary_image(display_th, binary_image, average_column)

        # Đặt góc lái và tốc độ điều khiển
        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(50)

# Kiểm tra nếu đây là file chính để thực thi
if __name__ == "__main__":
    main()
