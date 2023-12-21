import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# Tạo cửa sổ chính
window = tk.Tk()
window.title("Hình Tròn và Xử Lý Va Chạm")

# Kích thước cửa sổ
window.geometry("700x700")

# Tạo khung vuông bên trong cửa sổ
frame = tk.Frame(window, width=500, height=500, bg="black")
frame.place(x=100, y=100)

# Tạo một canvas trong khung vuông để vẽ hình tròn
canvas = tk.Canvas(frame, width=500, height=500, bg="black")
canvas.pack()


# Tạo hình tròn thứ nhất và lưu ID của nó
circle1_x, circle1_y = 100, 100  # Tọa độ ban đầu của hình tròn 1
circle1_radius = 20  # Bán kính ban đầu của hình tròn 1
circle1 = canvas.create_oval(circle1_x - circle1_radius, circle1_y - circle1_radius,
                             circle1_x + circle1_radius, circle1_y + circle1_radius, fill="blue")

# Tạo văn bản cho hình tròn 1 và lưu ID của nó
text1 = canvas.create_text(circle1_x, circle1_y - circle1_radius - 10, text="Hoa1", fill="white",
                           font=("Helvetica", 12))

# Tạo hình tròn thứ hai và lưu ID của nó
circle2_x, circle2_y = 200, 200  # Tọa độ ban đầu của hình tròn 2
circle2_radius = 20  # Bán kính ban đầu của hình tròn 2
circle2 = canvas.create_oval(circle2_x - circle2_radius, circle2_y - circle2_radius,
                             circle2_x + circle2_radius, circle2_y + circle2_radius, fill="red")

# Tạo văn bản cho hình tròn 2 và lưu ID của nó
text2 = canvas.create_text(circle2_x, circle2_y - circle2_radius - 10, text="Hoa2", fill="white",
                           font=("Helvetica", 12))

# Tạo biến trạng thái để theo dõi trò chơi và thông báo
game_over = False
collision_message_id = None

# Hàm để di chuyển hình tròn và kiểm tra va chạm
def move_and_check_collision(event):
    global circle1_radius, circle2_radius, game_over, collision_message_id, circle1_x, circle1_y, circle2_x, circle2_y

    # Kiểm tra trạng thái trò chơi
    if game_over:
        return

    # Xác định sự kiện phím và xử lý
    if event.keysym == 'Up':
        if circle1_y - circle1_radius > 0:
            canvas.move(circle1, 0, -10)
            canvas.move(text1, 0, -10)
            circle1_y -= 10  # Cập nhật tọa độ y của hình tròn 1
    elif event.keysym == 'Down':
        if circle1_y + circle1_radius < 500:
            canvas.move(circle1, 0, 10)
            canvas.move(text1, 0, 10)
            circle1_y += 10  # Cập nhật tọa độ y của hình tròn 1
    elif event.keysym == 'Left':
        if circle1_x - circle1_radius > 0:
            canvas.move(circle1, -10, 0)
            canvas.move(text1, -10, 0)
            circle1_x -= 10  # Cập nhật tọa độ x của hình tròn 1
    elif event.keysym == 'Right':
        if circle1_x + circle1_radius < 500:
            canvas.move(circle1, 10, 0)
            canvas.move(text1, 10, 0)
            circle1_x += 10  # Cập nhật tọa độ x của hình tròn 1
    elif event.keysym == 'k':
        circle1_radius += 5
        canvas.coords(circle1,
                      circle1_x - circle1_radius, circle1_y - circle1_radius,
                      circle1_x + circle1_radius, circle1_y + circle1_radius)
        canvas.coords(text1, circle1_x, circle1_y - circle1_radius - 10)
    elif event.keysym == 'm':
        if circle1_radius > 5:
            circle1_radius -= 5
            canvas.coords(circle1,
                          circle1_x - circle1_radius, circle1_y - circle1_radius,
                          circle1_x + circle1_radius, circle1_y + circle1_radius)
            canvas.coords(text1, circle1_x, circle1_y - circle1_radius - 10)
    elif event.keysym == 'a':
        if circle2_x - circle2_radius > 0:
            canvas.move(circle2, -10, 0)
            canvas.move(text2, -10, 0)
            circle2_x -= 10  # Cập nhật tọa độ x của hình tròn 2
    elif event.keysym == 'f':
        if circle2_x + circle2_radius < 500:
            canvas.move(circle2, 10, 0)
            canvas.move(text2, 10, 0)
            circle2_x += 10  # Cập nhật tọa độ x của hình tròn 2
    elif event.keysym == 'w':
        if circle2_y - circle2_radius > 0:
            canvas.move(circle2, 0, -10)
            canvas.move(text2, 0, -10)
            circle2_y -= 10  # Cập nhật tọa độ y của hình tròn 2
    elif event.keysym == 'x':
        if circle2_y + circle2_radius < 500:
            canvas.move(circle2, 0, 10)
            canvas.move(text2, 0, 10)
            circle2_y += 10  # Cập nhật tọa độ y của hình tròn 2
    elif event.keysym == 'y':
        circle2_radius += 5
        canvas.coords(circle2, circle2_x - circle2_radius, circle2_y - circle2_radius,
                      circle2_x + circle2_radius, circle2_y + circle2_radius)
        canvas.coords(text2, circle2_x, circle2_y - circle2_radius - 10)
    elif event.keysym == 'h':
        if circle2_radius > 5:
            circle2_radius -= 5
            canvas.coords(circle2, circle2_x - circle2_radius, circle2_y - circle2_radius,
                          circle2_x + circle2_radius, circle2_y + circle2_radius)
            canvas.coords(text2, circle2_x, circle2_y - circle2_radius - 10)

    # Kiểm tra va chạm giữa hai hình tròn
    circle1_coords = canvas.coords(circle1)
    circle2_coords = canvas.coords(circle2)

    left1, top1, right1, bottom1 = circle1_coords
    left2, top2, right2, bottom2 = circle2_coords

    if right1 >= left2 and left1 <= right2 and bottom1 >= top2 and top1 <= bottom2:
        if collision_message_id is None:
            # Nếu thông báo va chạm chưa được hiển thị, thì hiển thị nó
            collision_message_id = canvas.create_text(200, 20, text="Hoa1 va chạm với Hoa2!", fill="white",
                                                     font=("Helvetica", 12))
            game_over = True  # Đánh dấu trò chơi kết thúc
            # Tạo một hộp thoại thông báo với nút "OK"
            response = messagebox.showinfo("Va chạm", "Hoa1 va chạm với Hoa2!\nNhấn OK để tiếp tục.")
            if response == "ok":
                game_over = False
                canvas.delete(collision_message_id)
                collision_message_id = None

# Bắt sự kiện phím bàn phím để di chuyển và kiểm tra va chạm
window.bind("<KeyPress>", move_and_check_collision)

# Khởi chạy vòng lặp chính của ứng dụng
window.mainloop()
