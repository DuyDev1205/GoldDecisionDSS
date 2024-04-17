from GoldDecision import connectDB
from selenium import webdriver
import mysql.connector
if __name__ == "__main__":
# Tạo một cấu hình cho trình duyệt Chrome
    chrome_options = webdriver.ChromeOptions()
    # Thêm tùy chọn để ngăn thông báo DevTools hiển thị trong terminal
    chrome_options.add_argument('--log-level=3')
    # Khởi tạo trình duyệt với cấu hình
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://webgia.com/gia-vang/sjc/")

    config = {
        "host": "localhost",
        "port": "3306",
        "user": "root",
        "password": "123456",
        "database": "dss"
    }
    connection = mysql.connector.connect(**config)
    connectDB('golddss',driver,connection)