# VISTA — Vision-based Intelligent Stevenson Thermometer Analyzer

A Raspberry Pi-based computer vision system for automated, non-contact temperature measurement from a Stevenson Screen thermometer. VISTA uses Picamera2, OpenCV, and digital image processing to detect the mercury level, estimate temperature through calibration, and record measurements automatically.

## 📌 Project Overview

Traditional Stevenson Screen thermometers require manual observation and recording. VISTA automates this process by capturing thermometer images using a Raspberry Pi camera and processing them using a computer vision pipeline.

The system performs image acquisition, frame averaging, image preprocessing, ROI extraction, reference-image comparison, adaptive thresholding, mercury-level detection, temperature calibration, real-time visualization, and CSV-based data logging.

## 🎯 Problem Statement

Manual thermometer observation can be time-consuming and may introduce errors during visual reading and data recording.

The objective of VISTA is to develop an automated vision-based system capable of:

- Detecting the mercury level from thermometer images
- Converting the detected position into temperature
- Displaying the temperature in real time
- Automatically recording temperature measurements

## ⚙️ Image Processing Pipeline

1. Image Acquisition
2. Frame Averaging
3. Image Preprocessing
4. ROI Extraction
5. Reference Image Comparison
6. Difference Image Generation
7. 1D Profile Generation
8. Adaptive Thresholding
9. Mercury Level Detection
10. Temperature Calculation
11. Data Logging

## 🔧 Hardware

- Raspberry Pi 4B
- Raspberry Pi Camera Module
- Stevenson Screen
- Mercury Thermometer
- White LED
- Monitor/Display

## 💻 Software & Libraries

- Python
- OpenCV
- NumPy
- Picamera2
- libcamera
- RPi.GPIO
- Tkinter
- CSV
- Threading

## ✨ Key Features

- Automated thermometer image acquisition
- Multi-frame averaging for noise reduction
- Image enhancement and preprocessing
- ROI-based thermometer analysis
- Reference-based image comparison
- Adaptive thresholding
- Automated mercury-level detection
- Pixel-to-temperature calibration
- Real-time temperature display
- Timestamped CSV data logging

## 📊 Output

The detected temperature is displayed on the live camera preview and recorded automatically in a CSV file for further analysis and monitoring.

## 🖥️ System Platform

**Compute Platform:** Raspberry Pi 4B  
**Camera:** Raspberry Pi Camera Module  
**Processing:** Python + OpenCV  
**Image Acquisition:** Picamera2

