# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import quote_plus
#
# # Từ vựng bạn muốn tìm kiếm
# search_word = "cave"  # Thay đổi thành từ vựng bạn muốn tìm
#
# # Tạo URL tìm kiếm Google
# search_url = f"https://www.google.com/search?q={quote_plus(search_word)}&source=lnms&tbm=isch"
#
# # Gửi yêu cầu GET đến trang tìm kiếm Google
# response = requests.get(search_url)
#
# # Kiểm tra xem yêu cầu có thành công không
# if response.status_code == 200:
#     # Sử dụng BeautifulSoup để phân tích mã HTML của trang
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # Tìm tất cả các thẻ img trong trang
#     img_tags = soup.find_all('img')
#
#     # Kiểm tra xem có ít nhất một thẻ img hay không
#     if len(img_tags) > 0:
#         # Lấy URL của ảnh đầu tiên
#         first_image_url = img_tags[0]['src']
#
#         # Hiển thị URL của ảnh đầu tiên
#         print(f"URL của ảnh đầu tiên: {first_image_url}")
#     else:
#         print("Không tìm thấy ảnh.")
# else:
#     print("Lỗi khi gửi yêu cầu GET đến trang tìm kiếm Google.")
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from PIL import Image
from io import BytesIO

# Từ vựng bạn muốn tìm kiếm
search_word = "pig"  # Thay đổi thành từ vựng bạn muốn tìm

# Tạo URL tìm kiếm Google
search_url = f"https://www.google.com/search?q={quote_plus(search_word)}&source=lnms&tbm=isch"

# Gửi yêu cầu GET đến trang tìm kiếm Google
response = requests.get(search_url)

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích mã HTML của trang
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các thẻ img trong trang
    img_tags = soup.find_all('img')

    # Tìm ảnh đầu tiên hợp lệ (chứa giao thức http hoặc https)
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url and img_url.startswith('http'):
            # Tải và hiển thị ảnh
            image_response = requests.get(img_url)
            image_data = BytesIO(image_response.content)
            image = Image.open(image_data)
            image.show()
            break  # Kết thúc khi tìm thấy ảnh hợp lệ
    else:
        print("Không tìm thấy ảnh hợp lệ.")
else:
    print("Lỗi khi gửi yêu cầu GET đến trang tìm kiếm Google.")
