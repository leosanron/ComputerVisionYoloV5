import torch
import cv2
import numpy as np
import pandas as pd
import pathlib
import sys
import pygame
import time
from datetime import datetime

def play_audio(filename):
    """
    Reproduce un archivo de audio dado.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def cargar_modelo():
    # Load the model
    model = torch.hub.load('ultralytics/yolov5', 'custom', force_reload=True, 
                        path='C:/Users/1020821046/Documents/CIENCIA DE DATOS/Folder/modeloYolov5/Modelo_1-2_16_150.pt')

    # Start VideoCapture
    cap = cv2.VideoCapture(0)
    return model, cap

def iniciar_variables():
    # Initialize DataFrame to store detection information
    dfs = pd.DataFrame(columns=["xmin", "ymin", "xmax", "ymax", "confidence", "class", "name","fecha_hora"])
    contador = -2    
    return dfs, contador

def deteccion_objetos(model, cap, dfs, contador):
    try:
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
            info = detect.pandas().xyxy[0]
            info["fecha_hora"] = datetime.now() # im1 predictions
            print(info)

            # Verificar si info está vacío
            
            if info.empty:
                # Crear un DataFrame con una fila llena de "0"
                info = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0,  datetime.now()]], columns=info.columns)
            print("vacio")

            # Append detection information to DataFrame
            dfs = pd.concat([dfs, info], ignore_index=True)
            # Obtener los últimos 6 registros de dfs
            ultimos_6 = dfs.tail(6)

            # Contar los valores de "name"
            conteo_nombres = ultimos_6["name"].value_counts()

            # Filtrar los nombres que tienen al menos 3 ocurrencias
            nombres_mayor_3 = conteo_nombres[conteo_nombres >= 3]

            # Imprimir los nombres que cumplen la condición

            contador += 1
            if contador >= 4:
                contador = 0
                if not nombres_mayor_3.empty:
                    print("Nombres con al menos 5 ocurrencias:")
                    print(nombres_mayor_3.index.tolist())

                if "LUCES BAJAS" in nombres_mayor_3.index:
                    play_audio("luces_bajas.mp3")
                elif "SEPERFICIE DESLIZANTE" in nombres_mayor_3.index:
                    play_audio("superficie_deslizante.mp3")
                elif "ESPACIAMIENTO" in nombres_mayor_3.index:
                    play_audio("señal_espaciamiento.mp3")
                elif "RIESGO DE ACCIDENTE" in nombres_mayor_3.index:
                    play_audio("riesgo_accidente.mp3")

            # Show FPS
            cv2.imshow('Detector', np.squeeze(detect.render()))

            # Check for key press
            key = cv2.waitKey(5)
            if key == 27:  # ESC key
                break

    except KeyboardInterrupt:
        print("Detención manual del proceso.")

    finally:
        # Release the camera and close all windows
        cap.release()
        cv2.destroyAllWindows()

        # Save DataFrame to Excel file
        excel_filename = 'detectiones.xlsx'
        dfs.to_excel(excel_filename, index=False)

        print("Datos guardados como: ", excel_filename)
