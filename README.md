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

### **1️⃣ Install PyTorch and CUDA**  
- **Official PyTorch Installation Guide:** [PyTorch Install](https://pytorch.org/get-started/locally/)  
- **CUDA Toolkit Download:** [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64)  
- If you have a **GPU**, install **CUDA Toolkit** and then install the corresponding PyTorch version.  
- If you **do not have a GPU**, install the CPU version of PyTorch.  

---

### **2️⃣ Install Ultralytics YOLOv5**  
Clone the YOLOv5 repository and install dependencies:  [YOLOv5](https://github.com/ultralytics/yolov5)
```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

---

### **3️⃣ Install LabelImg for Dataset Annotation**
Clone the LabelImg repository and install dependencies: [LabelImg](https://github.com/tzutalin/labelImg)
```bash
git clone https://github.com/tzutalin/labelImg
pip install pyqt5 lxml --upgrade
cd labelImg
pyrcc5 -o libs/resources.py resources.qrc
```

---

### **4️⃣ Label Dataset Using LabelImg**
Open LabelImg and annotate images with bounding boxes.
Save the labeled images inside:
```kotlin
data/
├── images/
├── labels/
```

---

### **5️⃣ Define dataset.yaml File**
Inside the yolov5 folder, create a dataset.yaml file with the following structure:
```yaml
# Dataset Configuration File
path: ../data  # Root dataset directory
train: images  # Training images (relative to 'path')
val: images    # Validation images (relative to 'path')

# Number of Classes
nc: 17 

# Class Names
names: ['dog', 'person', 'cat', 'tv', 'car', 'meatballs', 'marinara sauce', 
        'tomato soup', 'chicken noodle soup', 'french onion soup', 'chicken breast', 
        'ribs', 'pulled pork', 'hamburger', 'cavity', 'awake', 'drowsy']
```

---

### **6️⃣ Train YOLOv5 Model**
Run the training script inside the yolov5 folder:
```bash
cd yolov5
python train.py --img 320 --batch 16 --epochs 500 --data dataset.yaml --weights yolov5s.pt --workers 2
```

---

### **7️⃣ Run the Application**
After training, run the main application:
```bash
python app.py
```

---

## 🎯 Features
✅ Real-time driver drowsiness detection
✅ Uses YOLOv5 for object detection
✅ Audio alert system for drowsy drivers
✅ Custom dataset labeling and training

---

## 📌 Dependencies
- Python 3.8+
- PyTorch
- CUDA (for GPU acceleration)
- OpenCV
- Ultralytics YOLOv5
- LabelImg
