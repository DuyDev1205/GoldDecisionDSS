import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, timedelta

def findBody(driver):
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
def findHeader(driver):
    # Tìm tất cả các ô dữ liệu trong bảng
    thead_element = driver.find_element(By.XPATH, "//table[@class='table table-radius table-hover']//tbody")
    th_elements = thead_element.find_elements(By.TAG_NAME, "th")
    headers=[]
    for th_element in th_elements:
        headers.append(th_element.text)
    return headers
def insertDB(driver):
    khu_vuc=findHeader(driver)
    loai_vang, mua_vao, ban_ra = findBody(driver)
    cursor = connection.cursor()
    querry="INSERT INTO golddss (Khu_vuc, Loai_vang, Mua_vao, Ban_ra) VALUES (%s, %s, %s, %s)"
    reset_count="ALTER TABLE golddss AUTO_INCREMENT = 1"
    cursor.execute(reset_count)
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
def deleteDB():
    cursor = connection.cursor()
    delete_query="DELETE FROM golddss"
    cursor.execute(delete_query)
    connection.commit()
    print("Đã xóa toàn bộ dữ liệu từ bảng golddss thành công!")
def getDate():
    date_list = []
    # Tạo đối tượng cursor
    cursor = connection.cursor()
    cursor.execute("SELECT date FROM test_dss ORDER BY date ASC LIMIT 1")
    first_date_row = cursor.fetchone()
    if first_date_row:
        first_date_str = first_date_row[0]
        first_date = datetime.strptime(first_date_str, "%d/%m/%Y").date()
    else:
        first_date = datetime.today().date()
    # Lấy ngày hôm nay
    today = datetime.today().date()
    
    # Thêm 30 ngày gần nhất nếu không có dữ liệu
    if not first_date_row:
        current_date = today
        for _ in range(30):
            current_date_str = current_date.strftime("%d/%m/%Y")
            date_list.append(current_date_str)
            current_date -= timedelta(days=1)

    # Thêm ngày còn thiếu nếu ngày đầu tiên không phải hôm nay
    if first_date != today:
        current_date = today
        while current_date >= first_date:
            current_date_str = current_date.strftime("%d/%m/%Y")
            check_date_query = "SELECT COUNT(*) FROM test_dss WHERE date = %s"
            cursor.execute(check_date_query, (current_date_str,))
            if cursor.fetchone()[0] == 0:
                date_list.append(current_date_str)
                print(f"Đã thêm ngày: {current_date_str}\n")
            current_date -= timedelta(days=1)
    cursor.close()
    connection.close()
    return date_list    
def connectDB(data,driver):
        # Thông tin kết nối
    try:
        if connection.is_connected():
            print("Kết nối thành công!")
            deleteDB()
            insertDB(driver)
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
    # connectDB('golddss',driver)
    for i in getDate():
        print(i)