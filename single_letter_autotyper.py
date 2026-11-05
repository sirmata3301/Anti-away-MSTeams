"""
Single-Letter Auto Typer (GUI)
- Types ONE letter repeatedly at a set interval.
- F6 = Start/Stop (global hotkey, works even when the window isn't focused)
Requires: pip install pynput
"""
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from pynput.keyboard import Controller, Key, Listener

kb = Controller()
HOTKEY = Key.f6


class AutoTyper:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.thread = None

        root.title("Single-Letter Auto Typer")
        root.resizable(False, False)
        frm = ttk.Frame(root, padding=12)
        frm.grid()

        # Letter (limited to 1 character)
        vcmd = (root.register(lambda s: len(s) <= 1), "%P")
        ttk.Label(frm, text="Letter:").grid(row=0, column=0, sticky="w")
        self.letter = tk.StringVar(value="a")
        ttk.Entry(frm, textvariable=self.letter, width=5, validate="key",
                  validatecommand=vcmd).grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Interval (ms):").grid(row=1, column=0, sticky="w")
        self.interval = tk.StringVar(value="100")
        ttk.Entry(frm, textvariable=self.interval, width=10).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Count (0 = infinite):").grid(row=2, column=0, sticky="w")
        self.count = tk.StringVar(value="0")
        ttk.Entry(frm, textvariable=self.count, width=10).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Start delay (sec):").grid(row=3, column=0, sticky="w")
        self.delay = tk.StringVar(value="3")
        ttk.Entry(frm, textvariable=self.delay, width=10).grid(row=3, column=1, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, pady=(10, 4))
        self.start_btn = ttk.Button(btns, text="Start (F6)", command=self.start)
        self.start_btn.pack(side="left", padx=4)
        self.stop_btn = ttk.Button(btns, text="Stop (F6)", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

        self.status = tk.StringVar(value="Idle")
        ttk.Label(frm, textvariable=self.status, foreground="gray").grid(row=5, column=0, columnspan=2)

        # Global hotkey listener
        Listener(on_press=self.on_key).start()
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_key(self, key):
        if key == HOTKEY:
            self.root.after(0, self.stop if self.running else self.start)

    def start(self):
        if self.running:
            return
        letter = self.letter.get()
        try:
            interval = max(1, int(self.interval.get())) / 1000
            count = max(0, int(self.count.get()))
            delay = max(0.0, float(self.delay.get()))
        except ValueError:
            messagebox.showerror("Invalid input", "Interval, count, and delay must be numbers.")
            return
        if len(letter) != 1:
            messagebox.showerror("Invalid input", "Enter exactly one letter.")
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.thread = threading.Thread(target=self.run, args=(letter, interval, count, delay), daemon=True)
        self.thread.start()

    def run(self, letter, interval, count, delay):
        end = time.time() + delay
        while self.running and time.time() < end:
            self.set_status(f"Starting in {end - time.time():.1f}s... click your target field")
            time.sleep(0.1)

        typed = 0
        while self.running and (count == 0 or typed < count):
            kb.type(letter)
            typed += 1
            self.set_status(f"Typing '{letter}'  |  {typed} typed")
            time.sleep(interval)

        self.root.after(0, self.finish, typed)

    def set_status(self, text):
        self.root.after(0, self.status.set, text)

    def stop(self):
        self.running = False

    def finish(self, typed):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status.set(f"Stopped  |  {typed} typed")

    def on_close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    AutoTyper(root)
    root.mainloop()
