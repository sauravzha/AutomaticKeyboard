import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import pyautogui
import threading
import time
import json
import random
from ttkthemes import ThemedTk

class AutoTyperApp(ThemedTk):
    def __init__(self):
        super().__init__()
        self.set_theme("equilux")
        self.title("Automatic Keyboard")
        self.geometry("820x650")
        self.attributes("-topmost", True)

        # Configure style for the dark theme
        style = ttk.Style(self)
        style.configure('TLabel', background='#464646', foreground='#ffffff')
        style.configure('TButton', background='#5a5a5a', foreground='#ffffff')
        style.configure('TFrame', background='#464646')
        style.configure('TLabelframe', background='#464646', bordercolor="#686868")
        style.configure('TLabelframe.Label', background='#464646', foreground='#ffffff')
        style.configure('TCheckbutton', background='#464646', foreground='#ffffff')
        self.configure(background='#464646')

        self.typing_thread = None
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()
        self.pause_event.set()  # Initially not paused

        self.delay_var = tk.StringVar()
        self.word_by_word_var = tk.BooleanVar(value=False)

        self.create_widgets()
        self.load_settings()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")

        # Text Box
        self.text_box = tk.Text(main_frame, height=10, wrap="word", font=("Segoe UI", 12), relief="flat")
        self.text_box.pack(expand=True, fill="both", padx=5, pady=5)

        # --- Controls ---
        controls_labelframe = ttk.Labelframe(main_frame, text="Actions", padding="10")
        controls_labelframe.pack(fill="x", padx=5, pady=5)

        # Using a frame inside to pack buttons with proper spacing
        btn_frame = ttk.Frame(controls_labelframe)
        btn_frame.pack(fill="x")

        self.paste_button = ttk.Button(btn_frame, text="Paste", command=self.paste_text)
        self.paste_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.copy_button = ttk.Button(btn_frame, text="Copy", command=self.copy_text)
        self.copy_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.start_button = ttk.Button(btn_frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.fast_paste_button = ttk.Button(btn_frame, text="Fast Paste", command=self.fast_paste)
        self.fast_paste_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.pause_button = ttk.Button(btn_frame, text="Pause", command=self.pause_typing, state="disabled")
        self.pause_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.resume_button = ttk.Button(btn_frame, text="Resume", command=self.resume_typing, state="disabled")
        self.resume_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.stop_button = ttk.Button(btn_frame, text="Stop", command=self.stop_typing, state="disabled")
        self.stop_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)
        self.clear_button = ttk.Button(btn_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side="left", padx=2, pady=2, fill="x", expand=True)

        # --- Speed and Mode ---
        speed_labelframe = ttk.Labelframe(main_frame, text="Speed & Mode", padding="10")
        speed_labelframe.pack(fill="x", padx=5, pady=5)
        speed_labelframe.columnconfigure(1, weight=1) # Make the slider/entry column expandable

        # Speed Slider
        ttk.Label(speed_labelframe, text="Speed Slider:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.speed_slider = ttk.Scale(speed_labelframe, from_=0.0, to=0.5, orient="horizontal", command=self.on_slider_move)
        self.speed_slider.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Presets
        ttk.Label(speed_labelframe, text="Presets:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.speed_dropdown = ttk.Combobox(speed_labelframe, values=["48 WPM (0.25s)", "0.1s", "0.2s", "0.5s", "1s"], width=15)
        self.speed_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.speed_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)

        # Custom Delay
        ttk.Label(speed_labelframe, text="Custom Delay (s):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.delay_entry = ttk.Entry(speed_labelframe, textvariable=self.delay_var, width=10)
        self.delay_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.delay_entry.bind("<KeyRelease>", self.on_custom_delay_change)

        # Word by Word Mode
        self.word_by_word_check = ttk.Checkbutton(speed_labelframe, text="Type word by word", variable=self.word_by_word_var)
        self.word_by_word_check.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # --- Virtual Keyboard ---
        keyboard_labelframe = ttk.Labelframe(main_frame, text="Virtual Keyboard", padding="10")
        keyboard_labelframe.pack(fill="both", expand=True, padx=5, pady=5)
        self.create_keyboard(keyboard_labelframe)

        # --- Creator Label ---
        creator_label = ttk.Label(main_frame, text="Created by Saurav Jha", font=("Segoe UI", 8))
        creator_label.pack(side="bottom", pady=(10, 0))

    def create_keyboard(self, parent):
        keys = [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', ('Backspace', 2)],
            [('Tab', 1.5), 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', ('\\', 1.5)],
            [('Caps', 1.7), 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", ('Enter', 2.3)],
            [('Shift', 2.2), 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ('Shift', 2.8)],
            [('Space', 10)]
        ]

        for key_row in keys:
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill="x", padx=2, pady=2)
            for key in key_row:
                if isinstance(key, tuple):
                    text, width_ratio = key
                    btn = ttk.Button(row_frame, text=text, command=lambda k=text: self.on_key_press(k))
                    btn.pack(side="left", padx=1, pady=1, fill="x", expand=True, ipadx=int(width_ratio * 5))
                else:
                    btn = ttk.Button(row_frame, text=key, command=lambda k=key: self.on_key_press(k))
                    btn.pack(side="left", padx=1, pady=1, fill="x", expand=True)

    def on_key_press(self, key):
        if key == "Backspace":
            self.text_box.delete("end-2c", "end-1c")
        elif key == "Enter":
            self.text_box.insert("end", '\n')
        elif key == "Space":
            self.text_box.insert("end", ' ')
        elif key == "Tab":
            self.text_box.insert("end", '\t')
        elif key in ["Shift", "Caps"]:
            pass
        else:
            self.text_box.insert("end", key)

    def paste_text(self):
        try:
            self.text_box.insert("end", pyperclip.paste())
        except pyperclip.PyperclipException as e:
            messagebox.showwarning("Paste Error", f"Could not paste from clipboard: {e}")

    def copy_text(self):
        try:
            pyperclip.copy(self.text_box.get("1.0", "end-1c"))
        except pyperclip.PyperclipException as e:
            messagebox.showwarning("Copy Error", f"Could not copy to clipboard: {e}")

    def clear_text(self):
        self.text_box.delete("1.0", "end")

    def get_typing_delay(self):
        try:
            return float(self.delay_var.get())
        except (ValueError, tk.TclError):
            return 0.05  # Fallback

    def start_typing(self):
        text_to_type = self.text_box.get("1.0", "end-1c")
        if not text_to_type:
            messagebox.showwarning("Input Error", "Text box is empty.")
            return

        self.toggle_controls(typing=True)
        self.stop_event.clear()
        self.pause_event.set()

        self.typing_thread = threading.Thread(target=self.type_text, args=(text_to_type,), daemon=True)
        self.typing_thread.start()

    def fast_paste(self):
        text_to_paste = self.text_box.get("1.0", "end-1c")
        if not text_to_paste:
            messagebox.showwarning("Input Error", "Text box is empty.")
            return
        
        time.sleep(2) # Time to focus the window
        pyperclip.copy(text_to_paste)
        pyautogui.hotkey('ctrl', 'v')

    def type_text(self, text):
        time.sleep(2)
        base_delay = self.get_typing_delay()

        if self.word_by_word_var.get():
            words = text.split(' ')
            for i, word in enumerate(words):
                if self.stop_event.is_set():
                    break
                self.pause_event.wait()
                
                pyautogui.typewrite(word + (' ' if i < len(words) - 1 else ''))
                
                randomized_delay = base_delay * random.uniform(0.75, 1.25)
                time.sleep(randomized_delay)
        else:
            for char in text:
                if self.stop_event.is_set():
                    break
                self.pause_event.wait()
                
                randomized_delay = base_delay * random.uniform(0.75, 1.25)
                time.sleep(randomized_delay)
                pyautogui.typewrite(char)
        
        self.after(0, self.on_typing_finish)

    def on_typing_finish(self):
        self.toggle_controls(typing=False)

    def pause_typing(self):
        self.pause_event.clear()
        self.pause_button["state"] = "disabled"
        self.resume_button["state"] = "normal"

    def resume_typing(self):
        self.pause_event.set()
        self.pause_button["state"] = "normal"
        self.resume_button["state"] = "disabled"

    def stop_typing(self):
        self.stop_event.set()
        self.pause_event.set()
        if self.typing_thread and self.typing_thread.is_alive():
            self.typing_thread.join(timeout=1)
        self.on_typing_finish()

    def toggle_controls(self, typing):
        state = "disabled" if typing else "normal"
        self.start_button["state"] = state
        self.fast_paste_button["state"] = state
        self.pause_button["state"] = "normal" if typing else "disabled"
        self.stop_button["state"] = "normal" if typing else "disabled"

    def on_slider_move(self, value):
        self.delay_var.set(f"{float(value):.3f}")
        self.speed_dropdown.set('')

    def on_dropdown_select(self, event):
        val = self.speed_dropdown.get()
        delay = 0.05
        if "WPM" in val:
            delay = float(val.split('(')[1].replace('s)', ''))
        else:
            delay = float(val.replace('s', ''))
        self.delay_var.set(str(delay))
        self.speed_slider.set(delay)

    def on_custom_delay_change(self, event):
        self.speed_dropdown.set('')
        try:
            val = float(self.delay_var.get())
            self.speed_slider.set(val)
        except (ValueError, tk.TclError):
            pass

    def save_settings(self):
        settings = {
            "delay": self.delay_var.get(),
            "word_by_word": self.word_by_word_var.get()
        }
        with open("config.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                settings = json.load(f)
                delay = settings.get("delay", "0.05")
                self.delay_var.set(delay)
                self.speed_slider.set(float(delay))
                self.word_by_word_var.set(settings.get("word_by_word", False))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.delay_var.set("0.05")
            self.speed_slider.set(0.05)
            self.word_by_word_var.set(False)

    def on_closing(self):
        self.save_settings()
        if self.typing_thread and self.typing_thread.is_alive():
            self.stop_typing()
        self.destroy()

if __name__ == "__main__":
    app = AutoTyperApp()
    app.mainloop()
