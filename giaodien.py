import tkinter as tk
from tkinter import scrolledtext
from collections import deque

# =====================================================
# KÍCH THƯỚC
# =====================================================
ROWS = 5
COLS = 5
CELL_SIZE = 60

# =====================================================
# MA TRẬN PHÒNG
# 1 = BẨN
# 0 = SẠCH
# =====================================================
initial_room = [
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1]
]

room = []

# =====================================================
# BIẾN ĐIỀU KHIỂN
# =====================================================
paused = False
running = False
path = []
step_index = 0
current_algorithm = ""

# =====================================================
# GIAO DIỆN CHÍNH
# =====================================================
root = tk.Tk()

root.title("MÁY HÚT BỤI AI - BFS DFS")
root.geometry("1450x820")
root.configure(bg="#EAF4FF")

# =====================================================
# MENU TRÁI
# =====================================================
menu_frame = tk.Frame(
    root,
    bg="#1F3B5B",
    width=220
)

menu_frame.pack(side="left", fill="y")

menu_title = tk.Label(
    menu_frame,
    text="MENU",
    font=("Arial", 24, "bold"),
    bg="#1F3B5B",
    fg="white"
)

menu_title.pack(pady=30)

# =====================================================
# KHUNG GIỮA
# =====================================================
center_frame = tk.Frame(
    root,
    bg="#F5F9FF"
)

center_frame.pack(side="left", fill="both", expand=True)

# =====================================================
# DEMO
# =====================================================
demo_label = tk.Label(
    center_frame,
    text="DEMO",
    font=("Arial", 24, "bold"),
    bg="#F5F9FF",
    fg="#123456"
)

demo_label.pack(pady=10)

# =====================================================
# CANVAS NHỎ HƠN
# =====================================================
canvas = tk.Canvas(
    center_frame,
    width=380,
    height=380,
    bg="white",
    bd=3,
    relief="ridge"
)

canvas.pack()

# =====================================================
# KHUNG NÚT
# =====================================================
button_frame = tk.Frame(
    center_frame,
    bg="#F5F9FF"
)

button_frame.pack(pady=10)

# =====================================================
# GIẢI PHÁP
# =====================================================
solution_label = tk.Label(
    center_frame,
    text="GIẢI PHÁP",
    font=("Arial", 18, "bold"),
    bg="#F5F9FF",
    fg="#123456"
)

solution_label.pack(pady=10)

solution_text = tk.Text(
    center_frame,
    width=75,
    height=12,
    font=("Consolas", 11),
    bd=2,
    relief="solid"
)

solution_text.pack(pady=5)

# =====================================================
# KHUNG PHẢI
# =====================================================
right_frame = tk.Frame(
    root,
    bg="#DCEEFF",
    width=350
)

right_frame.pack(side="right", fill="y")

right_title = tk.Label(
    right_frame,
    text="QT HOẠT ĐỘNG",
    font=("Arial", 20, "bold"),
    bg="#DCEEFF",
    fg="#123456"
)

right_title.pack(pady=15)

# =====================================================
# KHUNG CUỘN QT HOẠT ĐỘNG
# =====================================================
activity_text = scrolledtext.ScrolledText(
    right_frame,
    width=42,
    height=38,
    font=("Consolas", 10),
    bd=2,
    relief="solid"
)

activity_text.pack(padx=10, pady=10)

# =====================================================
# RESET PHÒNG
# =====================================================
def reset_room():

    global room

    room = [row[:] for row in initial_room]

# =====================================================
# VẼ PHÒNG
# =====================================================
def draw_room(robot_x=None, robot_y=None):

    canvas.delete("all")

    for i in range(ROWS):

        for j in range(COLS):

            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE

            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # MÀU Ô
            if room[i][j] == 1:
                color = "orange"
            else:
                color = "white"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=2
            )

            # TEXT
            if room[i][j] == 1:
                text = "B"
            else:
                text = "S"

            canvas.create_text(
                x1 + 30,
                y1 + 15,
                text=text,
                font=("Arial", 10, "bold")
            )

            # ROBOT
            if i == robot_x and j == robot_y:

                canvas.create_oval(
                    x1 + 15,
                    y1 + 25,
                    x2 - 15,
                    y2 - 5,
                    fill="blue"
                )

# =====================================================
# BFS
# =====================================================
def create_bfs_path():

    queue = deque()
    visited = set()

    queue.append((0, 0))

    result = []

    while queue:

        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        result.append((x, y))

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < ROWS and 0 <= ny < COLS:

                if (nx, ny) not in visited:
                    queue.append((nx, ny))

    return result

# =====================================================
# DFS
# =====================================================
def create_dfs_path():

    stack = [(0, 0)]

    visited = set()

    result = []

    while stack:

        x, y = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        result.append((x, y))

        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < ROWS and 0 <= ny < COLS:

                if (nx, ny) not in visited:
                    stack.append((nx, ny))

    return result

# =====================================================
# HIỂN THỊ GIẢI PHÁP
# =====================================================
def show_solution():

    solution_text.delete(1.0, tk.END)

    solution_text.insert(
        tk.END,
        "GIẢI PHÁP CUỐI CÙNG\n\n"
    )

    solution_text.insert(
        tk.END,
        f"Thuật toán sử dụng: {current_algorithm}\n\n"
    )

    solution_text.insert(
        tk.END,
        f"Tổng số bước: {len(path)}\n\n"
    )

    solution_text.insert(
        tk.END,
        "KẾT LUẬN:\n"
    )

    solution_text.insert(
        tk.END,
        "- Robot đã làm sạch toàn bộ phòng.\n"
    )

    if current_algorithm == "BFS":

        solution_text.insert(
            tk.END,
            "- BFS duyệt theo chiều rộng.\n"
        )

        solution_text.insert(
            tk.END,
            "- BFS tìm kiếm tối ưu.\n"
        )

    else:

        solution_text.insert(
            tk.END,
            "- DFS duyệt theo chiều sâu.\n"
        )

        solution_text.insert(
            tk.END,
            "- DFS đi sâu trước rồi quay lui.\n"
        )

# =====================================================
# DEMO
# =====================================================
def run_demo():

    global step_index
    global running

    if paused:
        return

    if step_index >= len(path):

        running = False

        show_solution()

        return

    x, y = path[step_index]

    # HÚT BỤI
    if room[x][y] == 1:
        room[x][y] = 0

    draw_room(x, y)

    activity_text.insert(
        tk.END,
        f"Bước {step_index + 1}: "
        f"Robot tới ({x},{y})\n"
    )

    activity_text.see(tk.END)

    step_index += 1

    root.after(500, run_demo)

# =====================================================
# CHẠY BFS
# =====================================================
def run_bfs():

    global path
    global step_index
    global paused
    global running
    global current_algorithm

    current_algorithm = "BFS"

    reset_room()

    activity_text.delete(1.0, tk.END)

    step_index = 0

    paused = False
    running = True

    path = create_bfs_path()

    run_demo()

# =====================================================
# CHẠY DFS
# =====================================================
def run_dfs():

    global path
    global step_index
    global paused
    global running
    global current_algorithm

    current_algorithm = "DFS"

    reset_room()

    activity_text.delete(1.0, tk.END)

    step_index = 0

    paused = False
    running = True

    path = create_dfs_path()

    run_demo()

# =====================================================
# DỪNG
# =====================================================
def pause_demo():

    global paused

    paused = True

# =====================================================
# CHẠY TIẾP
# =====================================================
def resume_demo():

    global paused

    if paused:

        paused = False

        run_demo()

# =====================================================
# STYLE BUTTON
# =====================================================
btn_style = {
    "font": ("Arial", 13, "bold"),
    "width": 15,
    "height": 2,
    "bg": "#4A90E2",
    "fg": "white",
    "bd": 0,
    "cursor": "hand2"
}

# =====================================================
# NÚT BFS
# =====================================================
bfs_btn = tk.Button(
    menu_frame,
    text="BFS",
    command=run_bfs,
    **btn_style
)

bfs_btn.pack(pady=20)

# =====================================================
# NÚT DFS
# =====================================================
dfs_btn = tk.Button(
    menu_frame,
    text="DFS",
    command=run_dfs,
    **btn_style
)

dfs_btn.pack(pady=20)

# =====================================================
# NÚT CHẠY
# =====================================================
run_btn = tk.Button(
    button_frame,
    text="CHẠY",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    width=12,
    command=resume_demo
)

run_btn.grid(row=0, column=0, padx=10)

# =====================================================
# NÚT DỪNG
# =====================================================
pause_btn = tk.Button(
    button_frame,
    text="DỪNG",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=12,
    command=pause_demo
)

pause_btn.grid(row=0, column=1, padx=10)

# =====================================================
# KHỞI TẠO
# =====================================================
reset_room()
draw_room()

# =====================================================
# MAINLOOP
# =====================================================
root.mainloop()