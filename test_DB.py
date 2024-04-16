import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

config = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "123456",
    "database": "dss"
}

# Function to retrieve date from the database
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
    return date_list

# Function to input date on the web page

def inputDate(driver):
    date_values = []
    valid_dates = []
    try:
        for item in getDate():
            date_input = driver.find_element(By.XPATH, '//*[@id="hcalendar"]')
            button = driver.find_element(By.XPATH, '//*[@id="tracuu"]/div/form/button')
            
            date_input.send_keys(Keys.CONTROL + 'a')  # Clear existing input
            date_input.send_keys(item)  # Input the date
            button.click()  # Click the button to submit the date

            try:
                # After submitting the date, check for the specific element
                driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/p')
                print(f"{item} không cập nhật dữ liệu.")
            except NoSuchElementException:
                # If the specific element does not exist, add the date to valid_dates
                valid_dates.append(item)
                date_input = driver.find_element(By.XPATH, '//*[@id="hcalendar"]')
                date_values.append(date_input.get_attribute("value"))
                # print(f"{item} hợp lệ và đã được thêm vào.")

    except StaleElementReferenceException:
        print("Lỗi StaleElementReferenceException")
    
    return valid_dates,date_values  # Return valid_dates if you want to keep track of which dates were valid

# Initialize the Chrome browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://webgia.com/gia-vang/sjc/")

# Call the function to input date
# for days in inputDate(driver):
#     date_value = days
#     if date_value is not None:
#         print("Ngày tháng từ trường input là:", date_value)
# print(inputDate(driver))
# print(getDate())
connection = mysql.connector.connect(**config)
valid,date=inputDate(driver)
print(len(date))
print(valid)
# Close the browser
driver.quit()
