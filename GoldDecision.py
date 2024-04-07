import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
# Tạo một cấu hình cho trình duyệt Chrome
chrome_options = webdriver.ChromeOptions()
# Thêm tùy chọn để ngăn thông báo DevTools hiển thị trong terminal
chrome_options.add_argument('--log-level=3')
# Khởi tạo trình duyệt với cấu hình
driver = webdriver.Chrome(options=chrome_options)
# Mở trang web
driver.get("https://webgia.com/gia-vang/sjc/")

config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "123456",
    "database": "dss"
}
connection = mysql.connector.connect(**config)
def findBody():
    loai_vang, mua_vao, ban_ra = [], [], []  # Di chuyển khởi tạo danh sách ra khỏi vòng lặp
    
    tr_elements = driver.find_elements(By.XPATH, "//table[@class='table table-radius table-hover']//tr")
    # In ra nội dung của phần tử đầu tiên
    for tr in tr_elements:
        td_elements = tr.find_elements(By.TAG_NAME, "td")
        
        if td_elements:
            loai_vang.append(td_elements[0].text)
            mua_vao.append(td_elements[1].text)
            ban_ra.append(td_elements[2].text)
    return loai_vang,mua_vao,ban_ra
def findHeader():
    # Tìm tất cả các ô dữ liệu trong bảng
    thead_element = driver.find_element(By.XPATH, "//table[@class='table table-radius table-hover']//tbody")
    th_elements = thead_element.find_elements(By.TAG_NAME, "th")
    headers=[]
    for th_element in th_elements:
        headers.append(th_element.text)
    return headers
def InsertDB():
    khu_vuc=findHeader()
    loai_vang, mua_vao, ban_ra = findBody()
    cursor = connection.cursor()
    querry="INSERT INTO golddss (Khu_vuc, Loai_vang, Mua_vao, Ban_ra) VALUES (%s, %s, %s, %s)"
    for i in range(len(loai_vang)):
        if i<=7:
            j=0
            cursor.execute(querry,(khu_vuc[j],loai_vang[i],mua_vao[i],ban_ra[i]))
        else:
            j+=1
            cursor.execute(querry,(khu_vuc[j],loai_vang[i],mua_vao[i],ban_ra[i]))
    connection.commit()
    print(cursor.rowcount, "record(s) were inserted.")
def getData(data):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {data}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
def ConnectDB(data):
        # Thông tin kết nối
    try:
        if connection.is_connected():
            print("Kết nối thành công!")
            InsertDB()
            getData(data)
        else:
            print("Kết nối không thành công!")
    except mysql.connector.Error as error:
        print("Lỗi khi kết nối đến cơ sở dữ liệu:", error)

    finally:
        # Đóng kết nối sau khi sử dụng xong
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Kết nối đã được đóng.")
if __name__=='__main__':
    ConnectDB('golddss')