import tkinter as tk

def toggle_color(square):
    current_color = square.cget("bg")
    if current_color == "red":
        square.config(bg="blue")
    else:
        square.config(bg="red")

root = tk.Tk()
root.title("Giao diện 3x3")
root.geometry("600x600")

# Danh sách các từ vựng tiếng Anh và nghĩa tương ứng
vocabulary = ["hello", "sun", "tree", "cat", "dog", "house", "car", "book", "computer"]
meanings = ["xin chào", "mặt trời", "cây", "mèo", "chó", "nhà", "xe hơi", "sách", "máy tính"]

# Tạo khung chứa thanh chắn
separator = tk.Frame(root, width=2, bd=2, relief=tk.SUNKEN)
separator.pack(side=tk.LEFT, fill=tk.Y)

# Tạo khung chứa 9 ô vuông màu đỏ ở bên trái
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT)

# Tạo khung chứa 9 ô vuông màu xanh ở bên phải
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT)

# Tạo tiêu đề "Từ Vựng" phía trên 9 ô bên trái
vocab_label = tk.Label(left_frame, text="Từ Vựng", font=("Helvetica", 12))
vocab_label.pack()

# Tạo tiêu đề "Nghĩa Từ Vựng" phía trên 9 ô bên phải
meaning_label = tk.Label(right_frame, text="Nghĩa Từ Vựng", font=("Helvetica", 12))
meaning_label.pack()

# Tạo 9 ô vuông màu đỏ chia thành 3 hàng ở bên trái và thêm từ vựng vào từng ô
for i in range(3):
    row_frame = tk.Frame(left_frame)
    row_frame.pack()
    for j in range(3):
        index = i * 3 + j
        square = tk.Label(row_frame, width=10, height=5, bg="red", relief="solid", text=vocabulary[index])
        square.pack(side=tk.LEFT)
        square.bind("<Button-1>", lambda event, s=square: toggle_color(s))

# Tạo 9 ô vuông màu xanh chia thành 3 hàng ở bên phải và thêm nghĩa từ vựng vào từng ô
for i in range(3):
    row_frame = tk.Frame(right_frame)
    row_frame.pack()
    for j in range(3):
        index = i * 3 + j
        square = tk.Label(row_frame, width=10, height=5, bg="blue", relief="solid", text=meanings[index])
        square.pack(side=tk.LEFT)
        square.bind("<Button-1>", lambda event, s=square: toggle_color(s))

root.mainloop()
