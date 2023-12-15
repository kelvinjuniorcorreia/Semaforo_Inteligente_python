import cv2
import time

def contar_carros(frame, car_cascade, roi_position, label):
    gray_roi = cv2.cvtColor(frame[roi_position[1]:roi_position[1]+roi_position[3], roi_position[0]:roi_position[0]+roi_position[2]], cv2.COLOR_BGR2GRAY)

    # Detecta carros na área definida pela ROI
    cars = car_cascade.detectMultiScale(gray_roi, scaleFactor=1.1, minNeighbors=3, minSize=(2, 2))
    total_carros = len(cars)

    return total_carros

# Caminho do vídeo
video_path = 'Trafego_florida.mp4'
cap = cv2.VideoCapture(video_path)

# Carrega o classificador Haar Cascade
car_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

# Define a posição das regiões de interesse (ROIs)
roi_position_upper_right = (850, 200, 420, 160)
roi_position_lower_left = (10, 320, 450, 180)

# Inicializa semáforos e tempo de avaliação
semaforo1 = "Vermelho"
semaforo2 = "Vermelho"
tempo_inicial = time.time()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Desenha retângulo para mostrar a área de interesse
    cv2.rectangle(frame, (roi_position_upper_right[0], roi_position_upper_right[1]), (roi_position_upper_right[0] + roi_position_upper_right[2], roi_position_upper_right[1] + roi_position_upper_right[3]), (0, 0, 255), 2)
    cv2.rectangle(frame, (roi_position_lower_left[0], roi_position_lower_left[1]), (roi_position_lower_left[0] + roi_position_lower_left[2], roi_position_lower_left[1] + roi_position_lower_left[3]), (0, 0, 255), 2)

    # Chama a função para contar os carros
    total_carros_upper_right = contar_carros(frame, car_cascade, roi_position_upper_right, "Upper Right")
    total_carros_lower_left = contar_carros(frame, car_cascade, roi_position_lower_left, "Lower Left")

    # Exibe os valores de ambos os semáforos e o tempo atual
    cv2.rectangle(frame, (8, 130), (480, 55), (255, 255, 255), -1)
    cv2.putText(frame, f'Semaforo 1: {semaforo1}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Total Carros (Semaforo 1): {total_carros_upper_right}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.rectangle(frame, (798, 130), (1270, 55), (255, 255, 255), -1)
    cv2.putText(frame, f'Semaforo 2: {semaforo2}', (800, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Total Carros (Semaforo 2): {total_carros_lower_left}', (800, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.putText(frame, f'{time.time() - tempo_inicial:.2f}', (600, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Atualiza a cor dos semáforos após os 10 segundos
    if time.time() - tempo_inicial > 10:
        if total_carros_upper_right > total_carros_lower_left:
            semaforo1 = "Verde"
            semaforo2 = "Vermelho"
        else:
            semaforo1 = "Vermelho"
            semaforo2 = "Verde"

        tempo_inicial = time.time()

    # Exibe o frame
    cv2.imshow('Video Analysis', frame)

    if cv2.waitKey(25) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
