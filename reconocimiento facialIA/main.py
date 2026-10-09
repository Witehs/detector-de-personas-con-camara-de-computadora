import cv2
from src.detector import FaceDetector
from src.alert_system import AlertSystem


def main():
    print("==========================================")
    print(" Detección Facial con MediaPipe & Alerta ")
    print("==========================================")

    # 1. Inicializar componentes
    detector = FaceDetector(min_detection_confidence=0.6)
    alert_system = AlertSystem(cooldown_seconds=5)

    # 2. Iniciar captura de webcam (0 es la cámara por defecto)
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("[ERROR] No se pudo acceder a la webcam.")
        return

    print("[INFO] Presiona la tecla 'q' para salir de la aplicación.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] No se pudo leer el fotograma de la cámara.")
            break

        # Procesar fotograma con MediaPipe
        face_locations, face_names = detector.process_frame(frame)

        # Si se detecta al menos un rostro, se dispara la alerta de voz
        if len(face_names) > 0:
            alert_system.trigger_alert("Atención, se detectó una persona usando la computadora")

        # Dibujar rectángulos y texto en la pantalla por cada rostro
        for (top, right, bottom, left), label in zip(face_locations, face_names):
            # Dibujar caja verde en el rostro
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Fondo para la etiqueta de texto
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            
            # Texto
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 10), font, 0.6, (0, 0, 0), 1)

        # Mostrar ventana con el video
        cv2.imshow('Monitor de Presencia - MediaPipe', frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos al cerrar
    video_capture.release()
    cv2.destroyAllWindows()
    print("[INFO] Programa finalizado correctamente.")


if __name__ == "__main__":
    main()