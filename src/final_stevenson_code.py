# -----------------------------------------

# Digital Image Processing-Based Stevenson Screen
# Developed by:
# Abhijeet Rastogi
# Mohak Joshi
# Summer Interns 2026
# India Meteorological Department (IMD)

# -----------------------------------------

import cv2
import time
import os
import threading
import tkinter as tk
from picamera2 import Picamera2
from libcamera import Transform
import RPi.GPIO as GPIO
import numpy as np
import csv
from datetime import datetime

# ==============================
# CALIBRATION
# ==============================
PIXEL_AT_5C = 505
PIXEL_AT_45C = 63

TEMP_LOW = 12
TEMP_HIGH = 45

# ===============================
# CAMERA + ROI SETTINGS
# ===============================
FRAME_W,FRAME_H=700,640

ROI_X,ROI_Y=323,1
ROI_W,ROI_H=9,620

SAVE_DIR="/home/iot/Desktop/image_new_stevenson"
os.makedirs(SAVE_DIR,exist_ok=True)
# ===============================
# GPIO SETUP
# ===============================
WHITE=18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(WHITE,GPIO.OUT)
def leds_off():
    GPIO.output(WHITE,0)

latest_frame=None
ref=None
running=True
temperature=0
current_mode="Black_White"

# ===============================
# CAMERA INIT (WITH 180° FLIP)
# ===============================
picam2=Picamera2()
config=picam2.create_video_configuration(
    main={"size":(FRAME_W,FRAME_H),"format":"RGB888"},
    transform=Transform(hflip=0,vflip=0)
)
picam2.configure(config)
picam2.start()
time.sleep(2)

# ===============================
# CAMERA MODE SETTINGS
# ===============================
def apply_camera_mode(mode):
    if mode in ["Black_White"]:
        picam2.set_controls({
                "AeEnable": False,
                "AwbEnable": False,   
                "AnalogueGain": 10.0,
        })
    else:
        picam2.set_controls({
            "AwbEnable": True,
            "AeEnable": True,
        })
# ===============================
# NOISE REDUCTION + CONTRAST
# ===============================
def clean_frame(frame):
    global current_mode
    frame=np.array(frame,dtype=np.uint8)
    # base smoothing
    frame=cv2.bilateralFilter(frame,5,40,40)
    # ---------- BLACK AND WHITE SPECIAL PROCESS ----------
    if current_mode in ["Black_White"]:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # strong contrast
        clahe = cv2.createCLAHE(clipLimit=1.8,tileGridSize=(8,8))
        gray=clahe.apply(gray)
        # sharpening
        kernel=np.array([[0,-1,0],
                         [-1,5,-1],
                         [0,-1,0]])
        gray=cv2.filter2D(gray,-1,kernel)

        frame=cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    # ---------- NORMAL PROCESS ----------
    else:
        lab=cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
        l,a,b=cv2.split(lab)

        clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
        l=clahe.apply(l)

        lab=cv2.merge((l,a,b))
        frame=cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
    return frame
# ===============================
# CAMERA LOOP
# ===============================
def camera_loop():
    global latest_frame,ref,running,temperature
    while running:
        # -------- 5 FRAME AVERAGING --------
        frames=[]
        for _ in range(5):
            frames.append(picam2.capture_array().astype(np.float32))

        frame=np.mean(frames,axis=0).astype(np.uint8)
#     alpha = 0.2

#     avg = None
# 
#     while running:
# 
#         frame = picam2.capture_array()
# 
#         if avg is None:
#             avg = frame.astype(np.float32)
#         else:
#             cv2.accumulateWeighted(frame, avg, alpha)
# 
#         frame = cv2.convertScaleAbs(avg)
        # -----------------------------------
        frame=clean_frame(frame)
        latest_frame=frame.copy()
        cv2.rectangle(frame,(ROI_X,ROI_Y),
                      (ROI_X+ROI_W,ROI_Y+ROI_H),
                                  (0,255,0),1)

        load_reference()
        if ref is not None:
            live = latest_frame[ROI_Y:ROI_Y+ROI_H,
                                  ROI_X:ROI_X+ROI_W]
            # Default Reference
            #ref = cv2.imread("/home/iot/Desktop/image_stevenson_screen/REFERENCE.png")
        # =====================================================
        # CONVERT TO GRAYSCALE
        # =====================================================
            if len(ref.shape) == 3:
                ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
            else:
                ref_gray = ref.copy()

            if len(live.shape) == 3:
                live_gray = cv2.cvtColor(live, cv2.COLOR_BGR2GRAY)
            else:
                live_gray = live.copy()

         # =====================================================
         # REMOVE NOISE
         # =====================================================
            ref_gray = cv2.GaussianBlur(ref_gray, (5,5), 0)
            live_gray = cv2.GaussianBlur(live_gray, (5,5), 0)

        # =====================================================
        # DIFFERENCE IMAGE
        # =====================================================
            diff = cv2.absdiff(ref_gray, live_gray)

        # =====================================================
        # CREATE 1D PROFILE
        # =====================================================
            profile = np.mean(diff,axis=1).astype(np.float32)
            profile = cv2.GaussianBlur(
                profile.reshape(-1,1),
                (1,9),
                0).flatten()

        # =====================================================
        # ADAPTIVE THRESHOLD
        # =====================================================
            #background = np.median(profile)
            background = np.mean(profile[:20])
            #maximum = np.max(profile)
            #contrast = maximum - background
            peak = np.mean(np.sort(profile)[-5:])
            contrast = peak - background
            print("Contrast", contrast)
            factor = calculate_factor(background,contrast)
            threshold = background + (np.max(profile)-background)*factor
            
            print("Background  :", background)
            print("Maximum     :", np.max(profile))
            print("Threshold   :", threshold)
        # =====================================================
        # FIND MERCURY LEVEL
        # =====================================================
            required_rows = 7               # # Increase if the mercury level is detected due to noise.
            mercury_row = None

            for y in range(len(profile)-required_rows):
                if np.all(profile[y:y+required_rows] >= threshold):
                    mercury_row = y
                    correction = row_factor(mercury_row)
                    mercury_row = mercury_row + correction
                    break
            if mercury_row is None:
                mercury_row = np.argmax(profile)
            print("Mercury Row :", mercury_row)
            # ====================================================
            # CALIBRATION
            # =====================================================
            temp = TEMP_LOW + \
            ((PIXEL_AT_5C-mercury_row)/
            (PIXEL_AT_5C-PIXEL_AT_45C))\
            *(TEMP_HIGH-TEMP_LOW)
            
            temperature = round(temp, 1)
            print(f"Temperature : {temperature:.2f} °C")

        # =====================================================
        # DISPLAY
        # =====================================================
        display = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
#         cv2.line(display,
#                 (0, int(mercury_row)),
#                 (display.shape[1]-1, int(mercury_row)),(0,255,0),2)
        if cv2.waitKey(1)&0xFF==ord('q'):
            stop_all()

        if temperature is not None:
            cv2.putText(frame,
                f"Temperature : {temperature:.2f} C",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
        else:
            cv2.putText(frame,
                "Capture Reference First",
                (10, 60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 0, 255),2)
        cv2.imshow("Live Preview", frame)
        cv2.imshow("diff",diff)
    if cv2.waitKey(1)&0xFF==ord('q'):
        stop_all()
    picam2.stop()
    cv2.destroyAllWindows()
    
# =======================
# LOAD REFERENCE
# =======================
def load_reference():
    global ref
    if os.path.exists("/home/iot/Desktop/image_new_stevenson"):
        ref = cv2.imread("/home/iot/Desktop/image_new_stevenson/REFERENCE.png")
        if ref is not None:
            print("Reference loaded.")
        else:
            print("Reference file corrupted.")
            ref = None
    else:
        print("No reference found.")
        ref = None
# ======================================================
# CALIBRATION
# ======================================================
ROW_FACTOR = [
    (547, 0),
    (476, 0),                   # First value: detected mercury row.
    (474, 0),                   # Second value: row offset (+/-) for fine-tuning the detected mercury position.
    (406, 0),
    (403, 0),
    (333, 0),
    (265, 0),
    (194, 0),
    (167, 0),
    (153, 0),
    (125, 0),
    (83 , 0),
    (56 , 0)
]
def row_factor(row):
    global temperature
    table = sorted(ROW_FACTOR, reverse=True)
    if row >= table[0][0]:
        return table[0][1]
    if row <= table[-1][0]:
        return table[-1][1]
    for i in range(len(table)-1):
        r1,f1 = table[i]
        r2,f2 = table[i+1]
        if r1 >= row >= r2:
            return f1 + (row-r1)*(f2-f1)/(r2-r1)
    return 0
# =======================
# CALCLATE FACTOR
# =======================
# def calculate_factor(background, contrast):
#     global temperature
#     # 10°C - 20°C
#     if contrast >= 22:
#         factor = 0.45
#     elif contrast >= 18:
#         factor = 0.42
#     elif contrast >= 14:
#         factor = 0.40
#     # 25°C - 35°C
#     elif contrast >= 10:
#         factor = 0.30
#     elif contrast >= 8:
#         factor = 0.21
#     # 35°C - 45°C
#     else:
#         if background < 16:
#             factor = 0.18
#         elif background < 18:
#             factor = 0.18
#         elif background < 19:
#             factor = 0.182
#         else:
#             factor = 0.18
#     return factor

def calculate_factor(background, contrast):

    # Very bright background
    if background >= 20:            # Modify these values to adjust .                                     
        if contrast >= 26:            # the adaptive threshold for different contrast ranges   
            return 0.3
        elif contrast >= 22:
            return 0.33
        elif contrast >= 18:
            return 0.36
        else:
            return 0.4

    # Medium background
    elif background >= 16:
        if contrast >= 26:
            return 0.35
        elif contrast >= 22:
            return 0.37
        elif contrast >= 18:
            return 0.39
        else:
            return 0.41

    # Dark background
    else:
        if contrast >= 26:
            return 0.35
        elif contrast >= 22:
            return 0.40
        elif contrast >= 18:
            return 0.42
        else:
            return 0.4
# ====================================
# CSV FILE
# ====================================
def save_csv():
    global temperature, running
    CSV_FILE = "/home/iot/Desktop/temperature_log.csv"
    # Create CSV file with header if it doesn't exist
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Temperature (°C)"])
    while running:        
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        # Save data
        if temperature != 0:
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([date, current_time, temperature])           
            print("new temperature is ",temperature)
            print(f"{date} {current_time} -> {temperature:.2f} °C saved")
        time.sleep(30)
# ===============================
# MODE BUTTONS
# ===============================
def set_white():
    global current_mode
    current_mode="White RGB"
    leds_off()
    GPIO.output(WHITE,1)
    apply_camera_mode(current_mode)
    
def set_white_black():
    global current_mode
    current_mode="Black_White"
    leds_off()
    GPIO.output(WHITE,1)
    apply_camera_mode(current_mode)
# ===============================
# REFERENCE
# ===============================
def take_reference():
    global ref
    if latest_frame is None:return
    ref=latest_frame[ROI_Y:ROI_Y+ROI_H,
                     ROI_X:ROI_X+ROI_W].copy()
    cv2.imwrite(os.path.join(SAVE_DIR,"REFERENCE.png"),ref)
    print("Reference captured")
# ===============================
# SCREENSHOT
# ===============================
def take_shot():
    if latest_frame is None:return
    temp_value=temp_entry.get().strip()
    if temp_value=="":temp_value="0"
    roi=latest_frame[ROI_Y:ROI_Y+ROI_H,
                     ROI_X:ROI_X+ROI_W]
    color_dir=os.path.join(SAVE_DIR,current_mode.replace(" ","_"))
    os.makedirs(color_dir,exist_ok=True)
    counter=1
    while os.path.exists(
        f"{color_dir}/{current_mode}_{temp_value}C_SS_{counter:02d}.png"):
        counter+=1
    filename=f"{color_dir}/{current_mode}_{temp_value}C_SS_{counter:02d}.png"
    cv2.imwrite(filename,roi)
    print("Saved:",filename)
# ===============================
# STOP
# ===============================
def stop_all():
    global running
    running=False
    leds_off()
    GPIO.cleanup()
    root.quit()
# ===============================
# GUI
# ===============================
root=tk.Tk()
root.title("Stevenson Screen")
tk.Label(root,text="Select Mode",font=("Arial",14)).pack(pady=8)

tk.Button(root,text="LED ON",width=20,bg="blue",fg="white",command=set_white).pack(pady=4)
tk.Button(root,text="BLACK & WHITE",width=20,bg="black",fg="white",command=set_white_black).pack(pady=4)
tk.Button(root,text="LED OFF",width=20,bg="blue",fg="white",command=leds_off).pack(pady=6)

tk.Label(root,text="Temperature (°C):").pack(pady=(10,2))
temp_entry=tk.Entry(root,width=10)
temp_entry.insert(0,"0")
temp_entry.pack(pady=4)

tk.Button(root,text="TAKE REFERENCE PHOTO",width=22,bg="blue",fg="white",command=take_reference).pack(pady=6)
tk.Button(root,text="SCREENSHOT",width=20,bg="lightblue",command=take_shot).pack(pady=10)
tk.Button(root,text="QUIT",width=20,bg="red",command=stop_all).pack(pady=4)

threading.Thread(target=camera_loop,daemon=True).start()
threading.Thread(target=save_csv, daemon=True).start()
root.mainloop()







