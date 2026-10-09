import time
import pyttsx3


class AlertSystem:
    def __init__(self, cooldown_seconds=5):
        """
        Inicializa el motor de texto a voz y la gestión de la alerta.
        :param cooldown_seconds: Tiempo en segundos entre cada alerta de voz.
        """
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = 0

        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Velocidad de la voz
        except Exception as e:
            print(f"[ERROR] No se pudo inicializar pyttsx3: {e}")
            self.engine = None

    def trigger_alert(self, message="Se detectó una persona usando la computadora"):
        """
        Emite la alerta hablada si ya transcurrió el tiempo de cooldown.
        """
        current_time = time.time()
        
        if current_time - self.last_alert_time >= self.cooldown_seconds:
            self.last_alert_time = current_time
            print(f"\n[ALERTA EMITIDA] {message}\n")

            if self.engine:
                self.engine.say(message)
                self.engine.runAndWait()