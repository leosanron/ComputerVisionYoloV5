import torch
import cv2
import numpy as np
import pandas as pd
import pathlib
import sys
import pygame
import time
from datetime import datetime
from funciones import play_audio, cargar_modelo, iniciar_variables, deteccion_objetos

# Temporal fix for PosixPath error on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model, cap  = cargar_modelo()

dfs, contador = iniciar_variables()

deteccion_objetos(model=model, cap=cap, dfs=dfs, contador=contador)