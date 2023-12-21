import pyautogui
import time

def post_to_facebook(content):
    coor = pyautogui.locateOnScreen('opera2.jpg', grayscale=True, confidence=0.9)
    if coor is not None:  # Kiểm tra xem coor có giá trị hay không
        coor_center = pyautogui.center(coor)
        pyautogui.click(coor_center.x, coor_center.y)
        time.sleep(5)

    coor = pyautogui.locateOnScreen('input.jpg', grayscale=True, confidence=0.9)
    if coor is not None:  # Kiểm tra xem coor có giá trị hay không
        coor_center = pyautogui.center(coor)
        pyautogui.click((coor_center.x)+50 , coor_center.y)
        pyautogui.typewrite("facebook.com")
        pyautogui.press('enter')
        time.sleep(5)

    create_post_button = pyautogui.locateOnScreen('tus2.jpg', grayscale=True, confidence=0.9)
    if create_post_button:
        create_post_center = pyautogui.center(create_post_button)
        pyautogui.click(create_post_center.x, create_post_center.y)
        time.sleep(3)

        pyautogui.write(content)
        checkin_button = pyautogui.locateOnScreen('checkin.jpg', grayscale=True, confidence=0.9)
        if checkin_button:
            checkin_center = pyautogui.center(checkin_button)
            pyautogui.click(checkin_center.x, checkin_center.y)
            time.sleep(3)
            search_button = pyautogui.locateOnScreen('timkiem.jpg', grayscale=True, confidence=0.9)
            if search_button:
                search_center = pyautogui.center(search_button)
                pyautogui.click(search_center.x, search_center.y)
                time.sleep(3)

                # Nhập "Đại học Quang Bình" vào ô tìm kiếm
                pyautogui.typewrite("dai hoc quang binh")
                time.sleep(3)

                # Nhấp vào kết quả tìm kiếm đầu tiên
                result_button = pyautogui.locateOnScreen('dhqb2.jpg', grayscale=True, confidence=0.9)
                if result_button:
                    result_center = pyautogui.center(result_button)
                    pyautogui.click(result_center.x, result_center.y)
                    time.sleep(3)
        post_button = pyautogui.locateOnScreen('dangtus.jpg', grayscale=True, confidence=0.9)
        if post_button:
            post_button_center = pyautogui.center(post_button)
            pyautogui.click(post_button_center.x, post_button_center.y)
            time.sleep(5)

        else:
            print("Không tìm thấy nút Đăng bài")
    else:
        print("Không tìm thấy nút Tạo bài viết")

def main():
    posts = []
    with open('content.txt', 'r') as file:
        for post in file.readlines():
            posts.append(post.strip())
    count = 0
    while count < 10:
        post = posts[count]
        post_to_facebook(post)
        time.sleep(1)
        count += 1
    print("Đã đăng tất cả các bài viết")



if __name__ == '__main__':
    main()