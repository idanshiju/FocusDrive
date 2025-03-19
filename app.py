import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
import torch
import vlc
import os
import time
import csv

# Initialize main window
app = tk.Tk()
app.geometry("600x600")
app.title("Driver Drowsiness Detection")
ctk.set_appearance_mode("dark")

# Video frame setup
vidFrame = tk.Frame(app, height=480, width=600, bg="black")
vidFrame.pack()
vid = ctk.CTkLabel(vidFrame, text="")  
vid.pack()

# Detection variables
drowsy_counter = 0
alarm_active = False
alarm_player = None
audio_path = "D:/Major/audio/videoplayback.m4a"
if not os.path.exists(audio_path):
    print(f"Error: Audio file not found at {audio_path}")
    exit()

# Function to reset alarm
def reset_counter():
    global drowsy_counter, alarm_active, alarm_player
    drowsy_counter = 0
    alarm_active = False
    if alarm_player:
        alarm_player.stop()
        alarm_player.release()
        alarm_player = None
    print("Alarm reset and counter cleared.")

# Reset button
resetButton = ctk.CTkButton(app, text="Reset Alarm", command=reset_counter, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="teal")
resetButton.pack(pady=10)

# Load YOLO model
model = torch.hub.load("ultralytics/yolov5", "custom", path="D:/Major/yolov5/runs/train/exp12/weights/last.pt", force_reload=True)

# Camera initialization
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Error: Could not open the camera.")
    app.destroy()
    exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# CSV file setup
csv_filename = "D:/Major/drowsiness_log.csv"
session_start = time.time()
session_drowsy_time = 0
drowsy_timers = {}

# Get session count from CSV
def get_session_count():
    return sum(1 for _ in open(csv_filename)) if os.path.exists(csv_filename) else 1
session_count = get_session_count()

# Function to process video feed and detect drowsiness
def detect():
    global detect_id, drowsy_counter, alarm_active, alarm_player, session_drowsy_time
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame)
    rendered_img = np.squeeze(results.render()).astype(np.uint8)

    is_drowsy = False
    if len(results.xywh[0]) > 0:
        dconf, dclass = results.xywh[0][0][4].item(), int(results.xywh[0][0][5])
        if dconf > 0.5 and dclass == 16:
            drowsy_counter += 1
            is_drowsy = True
        else:
            drowsy_counter = max(0, drowsy_counter - 1)

        if drowsy_counter >= 10 and (not alarm_active or alarm_player.get_state() != vlc.State.Playing):
            alarm_active = True
            if not alarm_player:
                alarm_player = vlc.MediaPlayer(audio_path)
            alarm_player.stop()
            alarm_player.play()
    else:
        drowsy_counter = 0

    # Track drowsiness time
    if is_drowsy:
        drowsy_timers.setdefault("start", time.time())
    elif "start" in drowsy_timers:
        session_drowsy_time += time.time() - drowsy_timers.pop("start")

    # Update video frame
    vid.imgtk = ImageTk.PhotoImage(Image.fromarray(rendered_img))
    vid.configure(image=vid.imgtk)

    detect_id = vid.after(10, detect)

# Function to display session summary
def show_summary(total_time, awake_time, drowsy_time):
    summary_window = tk.Toplevel(app)
    summary_window.title("Session Summary")
    summary_window.geometry("300x200")

    for text in [("Session Summary", 14, "bold"), (f"Total Time: {total_time}", 12), (f"Awake Time: {awake_time}", 12), (f"Drowsy Time: {drowsy_time}", 12)]:
        tk.Label(summary_window, text=text[0], font=("Arial", text[1], text[2] if len(text) > 2 else "")).pack(pady=5)

    ctk.CTkButton(summary_window, text="OK", command=lambda: (summary_window.destroy(), app.quit()), height=40, width=100).pack(pady=10)

# Function to log session and display summary
def log_session():
    global session_count, session_start, session_drowsy_time
    session_end = time.time()
    total_time, awake_time = session_end - session_start, (session_end - session_start) - session_drowsy_time

    # Format times
    formatted_times = [time.strftime("%H:%M:%S", time.gmtime(t)) for t in [total_time, awake_time, session_drowsy_time]]

    # Write to CSV
    with open(csv_filename, "a", newline="") as file:
        writer = csv.writer(file)
        if os.stat(csv_filename).st_size == 0:
            writer.writerow(["Session", "Start Time", "End Time", "Total Time", "Awake Time", "Drowsy Time"])
        writer.writerow([session_count, time.strftime("%H:%M:%S", time.localtime(session_start)), time.strftime("%H:%M:%S", time.localtime(session_end)), *formatted_times])

    session_count += 1
    show_summary(*formatted_times)

# Function to stop detection, release resources, and log session
def stop_and_log():
    global cap
    if cap.isOpened():
        cap.release()
    vid.after_cancel(detect_id)
    log_session()

# Bind close event and start detection
app.protocol("WM_DELETE_WINDOW", stop_and_log)
detect()
app.mainloop()

# Release camera after closing
cap.release()