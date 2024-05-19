import cv2

# Abre la cámara
cap = cv2.VideoCapture(0)

# Verifica si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

# Bucle para capturar imágenes de la cámara
while True:
    # Captura un cuadro de la cámara
    ret, frame = cap.read()

    # Muestra el cuadro capturado
    cv2.imshow('Camara', frame)

    # Espera a que se presione la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()