import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


window = tk.Tk()
window.title("Game Hình Tròn")


window.geometry("700x700")

# Tạo khung vuông bên trong cửa sổ
frame = tk.Frame(window, width=500, height=500, bg="black")
frame.place(x=100, y=100)

# Tạo một canvas trong khung vuông để vẽ hình ảnh avatar
canvas = tk.Canvas(frame, width=500, height=500, bg="black")
canvas.pack()

game_over = False
collision_message_id = None
circle1_radius = 20
circle2_radius = 20

# Tạo hình tròn cho avatar thứ nhất
avatar1_x, avatar1_y = 100, 100  # Tọa độ ban đầu của avatar 1
# avatar1_circle = canvas.create_oval(avatar1_x - circle1_radius, avatar1_y - circle1_radius,
#                                     avatar1_x + circle1_radius, avatar1_y + circle1_radius, fill="blue")

# Tải hình ảnh avatar thứ nhất và chuyển đổi thành định dạng hình ảnh tkinter
avatar1_img = Image.open("avatar1.png")  # Thay "avatar1.png" bằng tên tệp ảnh của bạn
avatar1_img = avatar1_img.resize((circle1_radius * 2, circle1_radius * 2), Image.BICUBIC)
avatar1_img = ImageTk.PhotoImage(avatar1_img)

# Tạo hình ảnh avatar thứ hai và lưu ID của nó
avatar2_x, avatar2_y = 200, 200  # Tọa độ ban đầu của avatar 2
# avatar2_circle = canvas.create_oval(avatar2_x - circle2_radius, avatar2_y - circle2_radius,
#                                     avatar2_x + circle2_radius, avatar2_y + circle2_radius, fill="green")

# Tải hình ảnh avatar thứ hai và chuyển đổi thành định dạng hình ảnh tkinter
avatar2_img = Image.open("avatar2.png")  # Thay "avatar2.png" bằng tên tệp ảnh của bạn
avatar2_img = avatar2_img.resize((circle2_radius * 2, circle2_radius * 2), Image.BICUBIC)
avatar2_img = ImageTk.PhotoImage(avatar2_img)

# Tạo hình ảnh avatar thứ nhất và lưu ID của nó
avatar1_image = canvas.create_image(avatar1_x, avatar1_y, image=avatar1_img)
text1 = canvas.create_text(avatar1_x, avatar1_y - circle1_radius - 10, text="Hoa1", fill="white",
                           font=("arial", 12))
# Tạo hình ảnh avatar thứ hai và lưu ID của nó
avatar2_image = canvas.create_image(avatar2_x, avatar2_y, image=avatar2_img)
text2 = canvas.create_text(avatar2_x, avatar2_y - circle1_radius - 10, text="Hoa2", fill="white",
                           font=("arial", 12))
# Hàm để di chuyển avatar và kiểm tra va chạm
def move_and_check_collision(event):
    global game_over, collision_message_id, avatar1_x, avatar1_y, avatar2_x, avatar2_y, circle1_radius, circle2_radius
    global avatar1_img, avatar2_img
    # Kiểm tra trạng thái trò chơi
    if game_over:
        return

    # Xác định sự kiện phím và xử lý
    if event.keysym == 'Up':
        if avatar1_y > circle1_radius:
            canvas.move(avatar1_image, 0, -10)
            canvas.move(text1, 0, -10)
            avatar1_y -= 10
    elif event.keysym == 'Down':
        if avatar1_y < 500 - circle1_radius:
            canvas.move(avatar1_image, 0, 10)
            canvas.move(text1, 0, 10)
            avatar1_y += 10
    elif event.keysym == 'Left':
        if avatar1_x > circle1_radius:
            canvas.move(avatar1_image, -10, 0)
            canvas.move(text1, -10, 0)
            avatar1_x -= 10
    elif event.keysym == 'Right':
        if avatar1_x < 500 - circle1_radius:
            canvas.move(avatar1_image, 10, 0)
            canvas.move(text1, 10, 0)
            avatar1_x += 10
    elif event.keysym == 'k':
        circle1_radius += 5
        new_image = Image.open("avatar1.png")
        new_image = new_image.resize((circle1_radius * 2, circle1_radius * 2), Image.BICUBIC)
        avatar1_img = ImageTk.PhotoImage(new_image)
        canvas.itemconfig(avatar1_image, image=avatar1_img)
        canvas.coords(text1, avatar1_x, avatar1_y - circle1_radius - 10)
    elif event.keysym == 'm':
        if circle1_radius > 5:
            circle1_radius -= 5
            new_image = Image.open("avatar1.png")
            new_image = new_image.resize((circle1_radius * 2, circle1_radius * 2), Image.BICUBIC)
            avatar1_img = ImageTk.PhotoImage(new_image)
            canvas.itemconfig(avatar1_image, image=avatar1_img)
            canvas.coords(text1, avatar1_x, avatar1_y - circle1_radius - 10)
    elif event.keysym == 'w':
        if avatar2_y > circle2_radius:
            canvas.move(avatar2_image, 0, -10)
            canvas.move(text2, 0, -10)
            avatar2_y -= 10
    elif event.keysym == 'x':
        if avatar2_y < 500 - circle2_radius:
            canvas.move(avatar2_image, 0, 10)
            canvas.move(text2, 0, 10)
            avatar2_y += 10
    elif event.keysym == 'a':
        if avatar2_x > circle2_radius:
            canvas.move(avatar2_image, -10, 0)
            canvas.move(text2, -10, 0)
            avatar2_x -= 10
    elif event.keysym == 'f':
        if avatar2_x < 500 - circle2_radius:
            canvas.move(avatar2_image, 10, 0)
            canvas.move(text2, 10, 0)
            avatar2_x += 10
    elif event.keysym == 'y':
        circle2_radius += 5
        new2_image = Image.open("avatar2.png")
        new2_image = new2_image.resize((circle2_radius * 2, circle2_radius * 2), Image.BICUBIC)
        avatar2_img = ImageTk.PhotoImage(new2_image)
        canvas.itemconfig(avatar2_image, image=avatar2_img)
        canvas.coords(text2, avatar2_x, avatar2_y - circle2_radius - 10)
    elif event.keysym == 'h':
        if circle2_radius > 5:
            circle2_radius -= 5
            new2_image = Image.open("avatar2.png")
            new2_image = new2_image.resize((circle2_radius * 2, circle2_radius * 2), Image.BICUBIC)
            avatar2_img = ImageTk.PhotoImage(new2_image)
            canvas.itemconfig(avatar2_image, image=avatar2_img)
            canvas.coords(text2, avatar2_x, avatar2_y - circle2_radius - 10)
    # Kiểm tra va chạm giữa hai avatar
    if (avatar1_x - avatar2_x) ** 2 + (avatar1_y - avatar2_y) ** 2 <= (circle1_radius + circle2_radius) ** 2:
        if collision_message_id is None:
            # Nếu thông báo va chạm chưa được hiển thị, thì hiển thị nó
            collision_message_id = canvas.create_text(250, 20, text="Hoa1 va chạm với Hoa2!", fill="white",
                                                     font=("Helvetica", 12))
            game_over = True  # Đánh dấu trò chơi kết thúc
            # Tạo một hộp thoại thông báo với nút "OK"
            response = messagebox.showinfo("Va chạm", "Hoa1 va chạm với Hoa2!\nNhấn OK để tiếp tục.")
            if response == "ok":
                game_over = False
                canvas.delete(collision_message_id)
                collision_message_id = None


window.bind("<KeyPress>", move_and_check_collision)


window.mainloop()
