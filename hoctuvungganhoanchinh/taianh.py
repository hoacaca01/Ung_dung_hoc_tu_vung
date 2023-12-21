# import tkinter as tk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO
#
# # URL của ảnh
# image_url = "https://tse1.mm.bing.net/th?id=OIP.i9YmmZ3SluoTGUpXyTr9UAHaEK&amp;pid=Api&amp;P=0&amp;h=220"
#
# # Tạo cửa sổ Tkinter
# root = tk.Tk()
# root.title("Hiển thị ảnh")
#
# # Tải ảnh từ URL
# response = requests.get(image_url)
# image_data = response.content
#
# # Chuyển dữ liệu ảnh sang định dạng hình ảnh PIL
# image = Image.open(BytesIO(image_data))
#
# # Tạo một đối tượng PhotoImage từ hình ảnh PIL
# photo = ImageTk.PhotoImage(image)
#
# # Hiển thị ảnh trong cửa sổ Tkinter
# label = tk.Label(root, image=photo)
# label.pack()
#
# # Khởi chạy giao diện
# root.mainloop()
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# URL của từ vựng
# word_url = "https://tse1.mm.bing.net/th?id=OIP.i9YmmZ3SluoTGUpXyTr9UAHaEK&amp;pid=Api&amp;P=0&amp;h=220"  # Thay đổi URL này bằng URL thật
word_url = "/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif"
# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Thông tin từ vựng")

# Tạo một hàm để lấy thông tin từ trang web
def get_word_info():
    global word_info_label, word_image_label

    # Gửi yêu cầu GET đến URL của từ vựng
    response = requests.get(word_url)

    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code == 200:
        # Lấy URL của ảnh từ trang web (thay đổi tùy vào trang web)
        word_image_url = response.url

        # Tải ảnh từ URL
        image_response = requests.get(word_image_url)
        image_data = image_response.content

        # Chuyển dữ liệu ảnh sang định dạng hình ảnh PIL
        image = Image.open(BytesIO(image_data))

        # Tạo một đối tượng PhotoImage từ hình ảnh PIL
        photo = ImageTk.PhotoImage(image)

        # Hiển thị ảnh trong giao diện Tkinter
        word_image_label.config(image=photo)
        word_image_label.photo = photo

# Tạo nhãn cho hiển thị ảnh
word_image_label = tk.Label(root)
word_image_label.pack()

# Tạo nút để lấy thông tin từ vựng và hiển thị ảnh
get_info_button = tk.Button(root, text="Lấy thông tin từ vựng và ảnh", command=get_word_info)
get_info_button.pack()

# Khởi chạy giao diện
root.mainloop()

