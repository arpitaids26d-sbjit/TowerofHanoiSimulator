# main.py
# Tower of Hanoi Visual Simulator (Tkinter)

import tkinter as tk
from tkinter import messagebox
from hanoi_logic import get_all_moves, minimum_moves

# ---------- Settings (size, colors) ----------
CANVAS_W = 700
CANVAS_H = 350
BASE_Y = 320            # zameen ki height
ROD_X = [120, 350, 580] # teeno rods ki x position
ROD_NAMES = ["Source", "Auxiliary", "Destination"]
DISK_H = 22
DISK_COLORS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71",
               "#1abc9c", "#3498db", "#9b59b6", "#e84393"]


class HanoiApp:
    def __init__(self, root):
        self.root = root
        root.title("Tower of Hanoi Visual Simulator")
        root.resizable(False, False)

        # State variables
        self.rods = [[], [], []]   # har rod ke disks (bada = bada number)
        self.moves = []            # saari moves
        self.move_index = 0        # abhi kaunsi move chal rahi hai
        self.running = False       # animation chal rahi hai ya nahi
        self.paused = False
        self.after_id = None       # timer ka id
        self.num_disks = 0

        self.build_ui()

    # ---------- UI banana ----------
    def build_ui(self):
        top = tk.Frame(self.root, pady=8)
        top.pack()

        tk.Label(top, text="Number of disks (1-8):").grid(row=0, column=0, padx=5)
        self.entry = tk.Entry(top, width=5, justify="center")
        self.entry.insert(0, "3")
        self.entry.grid(row=0, column=1, padx=5)

        self.start_btn = tk.Button(top, text="Start", width=8, bg="#2ecc71",
                                   command=self.start)
        self.start_btn.grid(row=0, column=2, padx=5)

        self.pause_btn = tk.Button(top, text="Pause", width=8, bg="#f1c40f",
                                   command=self.toggle_pause, state="disabled")
        self.pause_btn.grid(row=0, column=3, padx=5)

        self.reset_btn = tk.Button(top, text="Reset", width=8, bg="#e74c3c",
                                   fg="white", command=self.reset)
        self.reset_btn.grid(row=0, column=4, padx=5)

        tk.Label(top, text="Speed:").grid(row=0, column=5, padx=(15, 2))
        self.speed = tk.Scale(top, from_=100, to=1500, orient="horizontal",
                              length=120, showvalue=False)
        self.speed.set(600)  # milliseconds delay
        self.speed.grid(row=0, column=6)

        self.canvas = tk.Canvas(self.root, width=CANVAS_W, height=CANVAS_H,
                                bg="#ecf0f1")
        self.canvas.pack()

        self.info = tk.Label(self.root, text="Disks daalo aur Start dabao",
                             font=("Arial", 12, "bold"), pady=8)
        self.info.pack()

        self.draw()

    # ---------- Drawing ----------
    def draw(self):
        self.canvas.delete("all")
        # zameen
        self.canvas.create_rectangle(20, BASE_Y, CANVAS_W - 20, BASE_Y + 10,
                                     fill="#7f8c8d", outline="")
        # rods + naam
        for i, x in enumerate(ROD_X):
            self.canvas.create_rectangle(x - 4, 60, x + 4, BASE_Y,
                                         fill="#34495e", outline="")
            self.canvas.create_text(x, BASE_Y + 25, text=ROD_NAMES[i],
                                    font=("Arial", 11, "bold"))
        # disks
        for i, rod in enumerate(self.rods):
            for level, disk in enumerate(rod):
                width = 30 + disk * 20
                y2 = BASE_Y - level * DISK_H
                y1 = y2 - DISK_H + 2
                x = ROD_X[i]
                self.canvas.create_rectangle(
                    x - width // 2, y1, x + width // 2, y2,
                    fill=DISK_COLORS[(disk - 1) % len(DISK_COLORS)],
                    outline="black")

    # ---------- Buttons ----------
    def start(self):
        if self.running:
            return
        # Input check
        try:
            n = int(self.entry.get())
            if n < 1 or n > 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please 1 se 8 ke beech number daalo.")
            return

        self.reset()  # pehle sab saaf karo
        self.num_disks = n
        self.rods[0] = list(range(n, 0, -1))  # sabse bada neeche
        self.moves = get_all_moves(n)
        self.move_index = 0
        self.running = True
        self.paused = False

        self.start_btn.config(state="disabled")
        self.entry.config(state="disabled")
        self.pause_btn.config(state="normal", text="Pause")
        self.update_info()
        self.draw()
        self.after_id = self.root.after(self.speed.get(), self.next_move)

    def toggle_pause(self):
        if not self.running:
            return
        if self.paused:
            self.paused = False
            self.pause_btn.config(text="Pause")
            self.after_id = self.root.after(self.speed.get(), self.next_move)
        else:
            self.paused = True
            self.pause_btn.config(text="Resume")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def reset(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        self.paused = False
        self.rods = [[], [], []]
        self.moves = []
        self.move_index = 0
        self.start_btn.config(state="normal")
        self.entry.config(state="normal")
        self.pause_btn.config(state="disabled", text="Pause")
        self.info.config(text="Disks daalo aur Start dabao")
        self.draw()

    # ---------- Animation ----------
    def next_move(self):
        if not self.running or self.paused:
            return

        if self.move_index < len(self.moves):
            src, dst = self.moves[self.move_index]
            disk = self.rods[src].pop()   # source se disk uthao
            self.rods[dst].append(disk)   # destination par rakho
            self.move_index += 1
            self.draw()
            self.update_info(f"Disk {disk}: {ROD_NAMES[src]} -> {ROD_NAMES[dst]}")
            self.after_id = self.root.after(self.speed.get(), self.next_move)
        else:
            self.finish()

    def update_info(self, extra=""):
        total = minimum_moves(self.num_disks)
        text = f"Move: {self.move_index} / {total}   (2^{self.num_disks} - 1 = {total})"
        if extra:
            text += f"\n{extra}"
        self.info.config(text=text)

    def finish(self):
        self.running = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.entry.config(state="normal")
        self.update_info("Puzzle Solved!")
        messagebox.showinfo("Completed",
                            f"Puzzle solved in {self.move_index} moves!")


# ---------- Program yahan se start hota hai ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiApp(root)
    root.mainloop()