# import requests
# from bs4 import BeautifulSoup
# url = "https://dict.laban.vn/find?type=1&query=every"
# response = requests.get(url)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, "html.parser")
#     content_div = soup.find("div", {"id": "content_selectable", "class": "content"})
#     extracted_text = content_div.get_text()
#     print(extracted_text)
# else:
#     print("Failed to retrieve the web page.")
# import requests
# from bs4 import BeautifulSoup
#
# url = "https://dict.laban.vn/find?type=1&query=every"
#
# try:
#     response = requests.get(url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     # Find the element by its class name
#     content_div = soup.find("div", class_="content")
#
#     # Extract text
#     if content_div:
#         extracted_text = content_div.get_text()
#         print(extracted_text)
#     else:
#         print("Content div not found on the page.")
# except requests.exceptions.RequestException as e:
#     print("Failed to retrieve the web page:", e)
import requests
from bs4 import BeautifulSoup

# Thay đổi từ khóa truy vấn ở đây
search_word = "hello"

# Tạo URL với từ khóa truy vấn mới
url = f"https://dict.laban.vn/find?type=1&query={search_word}"

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm phần tử chứa nghĩa của từ
    content_div = soup.find("div", class_="content")

    # Trích xuất văn bản
    if content_div:
        extracted_text = content_div.get_text()
        print(extracted_text)
    else:
        print("Không tìm thấy nghĩa của từ.")
except requests.exceptions.RequestException as e:
    print("Lỗi khi truy xuất trang web:", e)
