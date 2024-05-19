import torch
import cv2
import numpy as np
import pathlib
import pandas as pd

# Temporal fix for PosixPath error on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom', force_reload=True, 
                       path='C:/Users/1020821046/Documents/CIENCIA DE DATOS/Folder/modeloYolov5/best2-200.pt')

# Start VideoCapture
cap = cv2.VideoCapture(0)

# Initialize DataFrame to store detection information
while True:
    # Read frames
    ret, frame = cap.read()

    # Check if frame is successfully read
    if not ret:
        print("Error: No se pudo leer el frame de la cámara.")
        break

    # Perform detections
    detect = model(frame)

    # Extract detection information
    info = detect.pandas().xyxy[0]  # im1 predictions
    print(info)

    # Show FPS
    cv2.imshow('Car Detector', np.squeeze(detect.render()))

    # Check for key press
    key = cv2.waitKey(5)
    if key == 27:  # ESC key
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()