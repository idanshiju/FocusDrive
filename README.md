# FocusDrive: Driver Drowsiness Detection and Alert System  

**FocusDrive** is a real-time driver drowsiness detection system that uses a **custom YOLOv5 model** in **PyTorch** to classify drivers as **awake or drowsy**. If drowsiness persists for **3 seconds**, an **audio alarm** is triggered to alert the driver. The system also logs session details, including total time, awake time, and drowsy time.

---

## 📌 Features  
✅ **Real-time detection** using a custom **YOLOv5** model  
✅ **Audio alert** if drowsiness persists for **3 seconds**  
✅ **Logs session details** in a CSV file  
✅ **User-friendly UI** built with **Tkinter (customtkinter)**  
✅ **Video processing** using **OpenCV**  
✅ **Audio playback** with **VLC**  

---

## 🛠 Tech Stack  
- **Python**, **PyTorch**, **YOLOv5**  
- **OpenCV** for video processing  
- **customtkinter** for UI  
- **VLC** for audio alerts  
- **Label Studio (labelImg)** for dataset annotation  

---

## 📂 Dataset  
- **160 images** (80 awake, 80 drowsy)  
- Labeled using **Label Studio**  

---

## 🚀 Installation & Usage  

### 🔹 1. Clone the repository  
```bash
git clone https://github.com/your-username/FocusDrive.git
cd FocusDrive
