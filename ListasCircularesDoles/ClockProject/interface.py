import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytz
import math
import pygame
import os
from utils import save_alarms_to_file, load_alarms_from_file
from structures import CircularDoublyLinkedList

pygame.mixer.init()
ALARM_SOUND = "alarm.wav"

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual World Clock")
        self.root.geometry("600x700")
        self.root.configure(bg="#f8f0ff")

        self.selected_timezone = pytz.timezone("America/Bogota")
        self.alarm_list = CircularDoublyLinkedList()
        self.current_alarm_playing = False

        self.load_alarms()
        self.create_widgets()
        self.update_clock()
        self.update_analog_clock()

    def load_alarms(self):
        saved_alarms = load_alarms_from_file()
        for alarm_time in saved_alarms:
            self.alarm_list.append(alarm_time)

    def save_alarms(self):
        save_alarms_to_file(self.alarm_list.to_list())

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TLabel", background="#f8f0ff", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=10, relief="raised")

        ttk.Label(self.root, text="Select Timezone:").pack(pady=5)
        self.timezone_combo = ttk.Combobox(self.root, values=pytz.all_timezones, width=40)
        self.timezone_combo.set("America/Bogota")
        self.timezone_combo.pack(pady=5)
        self.timezone_combo.bind("<<ComboboxSelected>>", self.change_timezone)

        self.time_label = ttk.Label(self.root, text="", font=("Helvetica", 20, "bold"), background="#f8f0ff", foreground="black")
        self.time_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Alarm input fields
        frame = tk.Frame(self.root, bg="#f8f0ff")
        frame.pack(pady=5)

        ttk.Label(frame, text="Hour:").grid(row=0, column=0)
        self.hour_var = tk.StringVar()
        self.hour_spin = ttk.Spinbox(frame, from_=1, to=12, width=5, textvariable=self.hour_var)
        self.hour_spin.grid(row=0, column=1)

        ttk.Label(frame, text="Minute:").grid(row=0, column=2)
        self.minute_var = tk.StringVar()
        self.minute_spin = ttk.Spinbox(frame, from_=0, to=59, width=5, textvariable=self.minute_var)
        self.minute_spin.grid(row=0, column=3)

        ttk.Label(frame, text="AM/PM:").grid(row=0, column=4)
        self.ampm_var = tk.StringVar(value="AM")
        self.ampm_menu = ttk.Combobox(frame, values=["AM", "PM"], width=5, textvariable=self.ampm_var)
        self.ampm_menu.grid(row=0, column=5)

        ttk.Button(self.root, text="Set Alarm", command=self.set_alarm, style="TButton").pack(pady=5)
        self.stop_btn = ttk.Button(self.root, text="Stop Alarm", command=self.stop_alarm, style="TButton")
        self.stop_btn.pack(pady=5)

        ttk.Label(self.root, text="Pending Alarms:").pack(pady=5)
        self.alarm_dropdown = ttk.Combobox(self.root, values=[], width=30)
        self.alarm_dropdown.pack(pady=5)

        ttk.Button(self.root, text="Delete Selected Alarm", command=self.delete_selected_alarm, style="TButton").pack(pady=5)
        self.update_alarm_dropdown()

    def change_timezone(self, event):
        selected = self.timezone_combo.get()
        self.selected_timezone = pytz.timezone(selected)

    def update_clock(self):
        now = datetime.now(self.selected_timezone)
        current_time = now.strftime("%I:%M %p")
        self.time_label.config(text=now.strftime("%Y-%m-%d %H:%M:%S"))

        for alarm_time in self.alarm_list.to_list():
            if current_time == alarm_time and not self.current_alarm_playing:
                self.play_alarm(alarm_time)
                break

        self.root.after(1000, self.update_clock)

    def update_analog_clock(self):
        now = datetime.now(self.selected_timezone)
        self.canvas.delete("all")

        center_x, center_y = 150, 150
        radius = 100

        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                fill="#fff0f5", outline="black", width=2)

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            x_outer = center_x + radius * math.cos(angle)
            y_outer = center_y + radius * math.sin(angle)

            if i % 5 == 0:
                x_inner = center_x + (radius - 15) * math.cos(angle)
                y_inner = center_y + (radius - 15) * math.sin(angle)
                hour = i // 5 if i != 0 else 12
                tx = center_x + (radius - 30) * math.cos(angle)
                ty = center_y + (radius - 30) * math.sin(angle)
                self.canvas.create_text(tx, ty, text=str(hour), font=("Helvetica", 10, "bold"))
            else:
                x_inner = center_x + (radius - 5) * math.cos(angle)
                y_inner = center_y + (radius - 5) * math.sin(angle)

            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill="black")

        hour = now.hour % 12
        minute = now.minute
        second = now.second

        hour_angle = math.radians((hour + minute / 60) * 30 - 90)
        self.canvas.create_line(center_x, center_y,
                                center_x + 50 * math.cos(hour_angle),
                                center_y + 50 * math.sin(hour_angle),
                                width=4, fill="black")

        min_angle = math.radians((minute + second / 60) * 6 - 90)
        self.canvas.create_line(center_x, center_y,
                                center_x + 70 * math.cos(min_angle),
                                center_y + 70 * math.sin(min_angle),
                                width=3, fill="purple")

        sec_angle = math.radians(second * 6 - 90)
        self.canvas.create_line(center_x, center_y,
                                center_x + 90 * math.cos(sec_angle),
                                center_y + 90 * math.sin(sec_angle),
                                width=1, fill="pink")

        self.root.after(1000, self.update_analog_clock)

    def set_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            ampm = self.ampm_var.get().upper()
            if ampm not in ["AM", "PM"]:
                raise ValueError("Invalid AM/PM")

            if hour < 1 or hour > 12 or minute < 0 or minute > 59:
                raise ValueError("Invalid time input")

            time_str = f"{hour:02d}:{minute:02d} {ampm}"
            if time_str not in self.alarm_list.to_list():
                self.alarm_list.append(time_str)
                self.save_alarms()
                self.update_alarm_dropdown()
                messagebox.showinfo("Alarm", f"Alarm set for {time_str}")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format")

    def update_alarm_dropdown(self):
        alarm_values = self.alarm_list.to_list()
        self.alarm_dropdown['values'] = alarm_values
        if alarm_values:
            self.alarm_dropdown.set(alarm_values[-1])
        self.save_alarms()

    def play_alarm(self, alarm_time):
        try:
            if os.path.exists(ALARM_SOUND):
                pygame.mixer.music.load(ALARM_SOUND)
                pygame.mixer.music.play(loops=-1)
                self.current_alarm_playing = True
                self.alarm_list.remove_alarm(alarm_time)
                self.update_alarm_dropdown()
                messagebox.showinfo("Alarm", "It's time!")
        except Exception as e:
            print("Error playing sound:", e)

    def stop_alarm(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.current_alarm_playing = False

    def delete_selected_alarm(self):
        selected = self.alarm_dropdown.get()
        if selected in self.alarm_list.to_list():
            self.alarm_list.remove_alarm(selected)
            self.update_alarm_dropdown()
            messagebox.showinfo("Deleted", f"Deleted alarm: {selected}")
