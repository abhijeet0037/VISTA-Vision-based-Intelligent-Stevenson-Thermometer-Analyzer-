# VISTA — Vision-based Intelligent Stevenson Thermometer Analyzer

**An automated computer-vision system for reading temperature from a Stevenson screen thermometer using Raspberry Pi and digital image processing.**

VISTA (**Vision-based Intelligent Stevenson Thermometer Analyzer**) is a Raspberry Pi-based system that automatically captures and analyzes images of a Stevenson screen thermometer to estimate temperature without manual observation.

The system combines **Picamera2, OpenCV, NumPy, image registration, region-of-interest processing, thresholding, mercury detection, calibration, and data logging** to convert the visible mercury level into a temperature reading.

---

## 📌 Project Overview

Traditional Stevenson screen thermometers require manual observation and recording of temperature values. This process can introduce human reading errors and requires continuous monitoring.

VISTA automates this process by using a camera mounted near the thermometer and performing image-based analysis on the captured frames.

### Core Pipeline

```text
Camera
   ↓
Image Capture
   ↓
Image Registration
   ↓
ROI Adjustment
   ↓
Image Preprocessing
   ↓
Mercury Detection
   ↓
Temperature Calibration
   ↓
Temperature Estimation
   ↓
CSV Data Logging
```

---

## ✨ Key Features

* 📷 Automated image capture using **Picamera2**
* 🖥️ Raspberry Pi 4B based processing
* 🔄 Image registration for camera alignment
* 🎯 Region-of-Interest (ROI) based thermometer analysis
* 🧹 Image preprocessing and noise reduction
* 🧪 Mercury-column detection using digital image processing
* 🌡️ Pixel-to-temperature calibration
* 📊 Real-time temperature estimation
* 💾 Automatic temperature logging to CSV
* ⚙️ Designed for continuous automated operation

---

## 🧠 Image Processing Approach

VISTA processes each captured frame through several stages.

### 1. Image Capture

The Raspberry Pi camera captures an image of the thermometer inside the Stevenson screen.

The system uses **Picamera2** to interface with the camera module.

### 2. Image Registration

Camera movement or slight changes in orientation can shift the thermometer within the captured frame.

Image registration is used to align the current frame with a reference image before further processing.

Depending on the operating condition, registration techniques such as feature matching and geometric transformation can be used.

### 3. Region of Interest

After alignment, the thermometer region is isolated using a predefined ROI.

This reduces unnecessary processing and prevents background regions from interfering with mercury detection.

### 4. Image Preprocessing

The ROI is processed using digital image-processing techniques such as:

* Grayscale/color-space processing
* Thresholding
* Contrast adjustment
* Morphological operations
* Noise removal

The objective is to separate the mercury column from the thermometer background.

### 5. Mercury Detection

The processed ROI is scanned to determine the position of the mercury column.

The detected mercury position is represented in terms of its image coordinates/pixel row.

### 6. Temperature Calibration

The detected pixel position is converted into temperature using the calibrated relationship between thermometer scale position and temperature.

The calibration parameters depend on the physical geometry of the thermometer and camera setup.

### 7. Data Logging

The estimated temperature is stored along with the corresponding measurement information in a CSV file.

Example:

```text
Timestamp,Temperature
2026-08-09 15:30:00,30.2
2026-08-09 15:30:30,30.1
2026-08-09 15:31:00,30.3
```

---

## 🛠️ Hardware

| Component                    | Purpose                     |
| ---------------------------- | --------------------------- |
| Raspberry Pi 4B              | Main processing unit        |
| IMX219 Camera                | Image acquisition           |
| Stevenson Screen Thermometer | Temperature sensing element |
| Camera Mount                 | Maintains camera position   |

---

## 💻 Software & Technologies

* **Python**
* **OpenCV**
* **NumPy**
* **Picamera2**
* **Raspberry Pi OS**
* **CSV / Python data logging**

---

## 📂 Project Structure

```text
VISTA/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── src/
│   ├── camera.py
│   ├── registration.py
│   ├── preprocessing.py
│   ├── mercury_detection.py
│   ├── calibration.py
│   ├── temperature.py
│   └── data_logging.py
│
├── data/
│   └── sample/
│
├── results/
│   └── sample_outputs/
│
├── docs/
│   ├── flowchart.png
│   ├── system_architecture.png
│   └── project_report.pdf
│
└── tests/
    └── test_detection.py
```

> Update the structure above to exactly match the files that are actually present in the repository.

---

## 🔬 System Architecture

```text
                    ┌───────────────────┐
                    │   IMX219 Camera   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Image Capture   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Image Registration│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   ROI Extraction  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Image Preprocessing│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Mercury Detection │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Calibration    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Temperature Value │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   CSV Data Log    │
                    └───────────────────┘
```

---

## 📸 Processing Results

The recommended README should include example images showing the processing stages:

### Original Frame

```text
[Insert original camera image]
```

### Registered Image

```text
[Insert registered/aligned image]
```

### Thermometer ROI

```text
[Insert ROI image]
```

### Mercury Detection

```text
[Insert processed image with detected mercury level]
```

### Final Output

```text
Detected Temperature: XX.X °C
```

These visual results make the repository much easier to understand and demonstrate that the system is actually working.

---

## 📊 Performance Evaluation

The system should be evaluated using experimentally measured temperature values.

Recommended metrics:

| Metric                   |    Value |
| ------------------------ | -------: |
| Temperature range tested |  5–49 °C |
| Number of test samples   |   150    |
| Mean Absolute Error      |   0.1 °C |
| Maximum Error            |   0.5 °C |
| Average Accuracy         |   99.6 % |

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/abhijeet0037/VISTA-Vision-based-Intelligent-Stevenson-Thermometer-Analyzer-.git

cd VISTA-Vision-based-Intelligent-Stevenson-Thermometer-Analyzer-
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

For Raspberry Pi camera support, ensure that **Picamera2** and the required Raspberry Pi camera components are installed.

---

## ▶️ Usage

Connect the camera to the Raspberry Pi and position it so that the thermometer remains within the defined field of view.

Run the main application:

```bash
python3 main.py
```

The system will:

1. Capture an image.
2. Register the image with the reference frame.
3. Extract the thermometer ROI.
4. Preprocess the ROI.
5. Detect the mercury level.
6. Convert the detected position to temperature.
7. Display/store the temperature measurement.

---

## ⚙️ Calibration

Calibration is an important part of VISTA because the relationship between pixel position and temperature depends on the physical camera setup and thermometer geometry.

Before deployment:

1. Position the camera at the desired location.
2. Capture reference images.
3. Identify known thermometer temperature positions.
4. Determine the corresponding pixel coordinates.
5. Generate the pixel-to-temperature calibration relationship.
6. Store the calibration parameters used by the application.

Calibration should be repeated if the camera position, orientation, or thermometer mounting changes significantly.

---

## ⚠️ Limitations

The accuracy of the system can be affected by:

* Camera movement
* Camera rotation
* Changes in lighting
* Reflections on the thermometer
* Mercury-column visibility
* Background noise
* Incorrect ROI positioning
* Camera focus
* Calibration errors

The current system is therefore dependent on a controlled and consistent camera setup.

---

## 🔮 Future Improvements

Possible improvements include:

* Automatic ROI detection
* Improved illumination compensation
* More robust mercury segmentation
* Automatic camera-position correction
* Machine-learning based temperature correction
* Automatic calibration
* Web-based monitoring dashboard
* Remote temperature monitoring
* Improved error detection and confidence estimation
* Long-term environmental data analysis

---

## 🎯 Applications

VISTA can be adapted for:

* Automated meteorological observations
* Remote temperature monitoring
* Digitalization of analog thermometers
* Environmental monitoring stations
* Computer-vision based instrumentation
* Automated scientific data collection

---

## 👨‍💻 Author

**Abhijeet Rastogi**

B.Tech — Electronics & Communication Engineering

---

## 📜 License

This project is available under the license included in this repository.

---

## ⭐ Project Summary

**VISTA demonstrates how computer vision and embedded computing can be combined to automate the reading and logging of a traditional analog thermometer.**

The project integrates **Raspberry Pi, camera interfacing, digital image processing, geometric registration, mercury detection, calibration, and automated data logging** into a single measurement system.
