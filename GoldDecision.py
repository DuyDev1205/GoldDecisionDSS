import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def split_and_wrap(data):
    # Tách dữ liệu bằng dấu cách
    parts = data.split()
    # Kiểm tra xem có 2 dữ liệu hay không
    if len(parts) == 2:
        # Nếu có, đặt dữ liệu thứ 2 xuống dòng
        wrapped_text = f"{parts[0]}\n{parts[1]}"
    else:
        # Nếu không, giữ nguyên dữ liệu
        wrapped_text = data
    return wrapped_text

# Tải nội dung của trang web
url = 'https://bieudogiavang.vn/gia-vang-sjc'
response = requests.get(url)

# Khởi tạo danh sách table_data
table_data = []

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Phân tích nội dung HTML bằng BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm bảng đầu tiên trong trang web
    table = soup.find('table')

    # Duyệt qua các dòng của bảng
    for row in table.find_all('tr'):
        # Khởi tạo danh sách chứa dữ liệu của mỗi dòng
        row_data = []

        # Duyệt qua các ô dữ liệu trong dòng
        for cell in row.find_all(['td', 'th']):
            # Lấy nội dung của ô và chuẩn hóa
            cell_text = ' '.join(cell.get_text().split())
            # Nếu là cột 3 hoặc cột 4, thực hiện tách và đặt xuống dòng
            if len(row_data) == 3 or len(row_data) == 4:
                cell_text = split_and_wrap(cell_text)
            row_data.append(cell_text)

        # Nếu row_data không rỗng, thêm vào table_data
        if any(row_data):
            table_data.append(row_data)

    # In bảng với tabulate
    headers = table_data[0]  # Sử dụng dòng đầu tiên làm header
    print(tabulate(table_data[1:], headers=headers, tablefmt='pretty'))
else:
    print("Không thể kết nối đến trang web.")
