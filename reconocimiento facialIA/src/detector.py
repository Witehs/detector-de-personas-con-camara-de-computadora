import os
import urllib.request
import cv2


class FaceDetector:
    def __init__(self, min_detection_confidence=0.6):
        # 1. Intentar cargar desde la ruta por defecto de OpenCV
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # 2. Si falló la carga automática, descargar el archivo XML localmente
        if self.face_cascade.empty():
            local_xml = "haarcascade_frontalface_default.xml"
            if not os.path.exists(local_xml):
                print("[INFO] Descargando modelo de rostros Haar Cascade...")
                url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
                urllib.request.urlretrieve(url, local_xml)

            self.face_cascade = cv2.CascadeClassifier(local_xml)

        if self.face_cascade.empty():
            raise RuntimeError("[ERROR] No se pudo cargar el archivo XML de Haar Cascade.")

    def process_frame(self, frame):
        """
        Procesa el fotograma en escala de grises y detecta rostros.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detección de rostros
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        scaled_locations = []
        face_names = []

        for (x, y, w, h) in faces:
            top = y
            right = x + w
            bottom = y + h
            left = x

            scaled_locations.append((top, right, bottom, left))
            face_names.append("Persona Detectada")

        return scaled_locations, face_names