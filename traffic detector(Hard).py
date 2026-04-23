import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from ultralytics import YOLO
from collections import deque

# Load YOLO model
model = YOLO("yolov8n.pt")

# Video
cap = cv2.VideoCapture("traffic.1.mp4")

# Store counts for graph
counts = deque(maxlen=50)

# GUI setup
root = tk.Tk()
root.title("🚗 Smart Traffic AI Dashboard")
root.geometry("1000x700")

label = tk.Label(root)
label.pack()

info_label = tk.Label(root, text="Starting...", font=("Arial", 16))
info_label.pack()

def draw_lanes(frame):
    h, w, _ = frame.shape
    cv2.line(frame, (0, h//2), (w, h//2), (255, 0, 0), 2)
    return frame

def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.resize(frame, (900, 500))

    # Lane Detection
    frame = draw_lanes(frame)

    # YOLO Detection
    results = model(frame)

    vehicle_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label_name = model.names[cls]

            if label_name in ["car", "truck", "bus", "motorbike"]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame, label_name, (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2)
                vehicle_count += 1

    counts.append(vehicle_count)

    # Density logic
    if vehicle_count < 5:
        density = "Low"
    elif vehicle_count < 15:
        density = "Medium"
    else:
        density = "High"

    info_label.config(text=f"Vehicles: {vehicle_count} | Traffic: {density}")

    # Convert to Tkinter format
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label.imgtk = imgtk
    label.configure(image=imgtk)

    root.after(10, update_frame)

def show_graph():
    plt.plot(list(counts))
    plt.title("Vehicle Count Over Time")
    plt.xlabel("Frame")
    plt.ylabel("Vehicles")
    plt.show()

btn = tk.Button(root, text="📊 Show Graph", command=show_graph)
btn.pack(pady=10)

update_frame()
root.mainloop()