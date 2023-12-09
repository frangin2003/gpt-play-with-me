import cv2
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from datetime import datetime
import os

class Application:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.video_capture = None
        self.audio_stream = None
        self.is_recording = False
        self.timer = None
        self.capture_folder = "captures"
        if not os.path.exists(self.capture_folder):
            os.makedirs(self.capture_folder)
        self.create_gitignore()

    def setup_ui(self):
        # Webcam Image
        self.webcam_image = tk.Label(self.root)
        self.webcam_image.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 0))

        # Dropdown Frame
        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(side=tk.TOP, fill=tk.X, pady=(30, 30))

        # Video Devices Dropdown
        self.video_devices_dropdown = ttk.Combobox(self.dropdown_frame, font=('Helvetica', 21))  # Increased font size by 50%
        self.video_devices_dropdown['values'] = self.detect_video_devices()
        self.video_devices_dropdown.current(0)
        self.video_devices_dropdown.bind("<<ComboboxSelected>>", self.on_video_device_change)
        self.video_devices_dropdown.pack(side=tk.LEFT, padx=(50, 0))

        # Audio Devices Dropdown
        self.audio_devices_dropdown = ttk.Combobox(self.dropdown_frame, font=('Helvetica', 21))  # Increased font size by 50%
        self.audio_devices_dropdown['values'] = self.detect_audio_devices()
        self.audio_devices_dropdown.current(0)
        self.audio_devices_dropdown.bind("<<ComboboxSelected>>", self.on_audio_device_change)
        self.audio_devices_dropdown.pack(side=tk.RIGHT, padx=(0, 50))

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 30))

        # Capture Button
        self.capture_button = tk.Button(self.buttons_frame, text="Capture! 📷", command=self.capture_image, font=('Helvetica', 30))  # Increased font size by 3x
        self.capture_button.pack(side=tk.LEFT, padx=(50, 50), pady=(0, 0))

        # Talk Button
        self.talk_button = tk.Button(self.buttons_frame, text="Talk! 🎤", command=self.toggle_recording, font=('Helvetica', 30))  # Increased font size by 3x
        self.talk_button.pack(side=tk.RIGHT, padx=(50, 50), pady=(0, 0))

        # Status Label
        self.status_label = tk.Label(self.root, text="", anchor='w')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=(10, 0), pady=(0, 20))

    def detect_video_devices(self):
        # This function attempts to open video devices and returns a list of available ones
        device_indexes = range(10)  # Check first 10 devices
        available_devices = []
        for index in device_indexes:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.isOpened():
                available_devices.append(f"Camera {index}")
                cap.release()
        return available_devices

    def detect_audio_devices(self):
        # This function returns a list of available audio devices
        device_count = sr.Microphone.list_microphone_names()
        return [name for index, name in enumerate(sr.Microphone.list_microphone_names())]

    def on_video_device_change(self, event):
        # Handle change in video device selection
        selected_index = int(self.video_devices_dropdown.get().split(' ')[-1])
        self.start_video_stream(selected_index)

    def on_audio_device_change(self, event):
        # Handle change in audio device selection
        # This will be implemented later with audio recording functionality
        pass

    def start_video_stream(self, device_index):
        # Start video stream on selected device
        self.video_capture = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
        threading.Thread(target=self.update_frame, daemon=True).start()

    def update_frame(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image_width, image_height = image.size
                window_width = self.root.winfo_width()
                window_height = self.root.winfo_height() - self.dropdown_frame.winfo_height() - self.buttons_frame.winfo_height() - self.status_label.winfo_height() - 150  # Subtract an additional 50 pixels to ensure buttons and dropdowns are always visible
                if image_width / window_width > image_height / window_height:
                    new_width = window_width
                    new_height = int(image_height * window_width / image_width)
                else:
                    new_height = window_height
                    new_width = int(image_width * window_height / image_height)
                image = image.resize((new_width, new_height))  # Resize image to match window size while keeping aspect ratio
                image = ImageTk.PhotoImage(image)
                self.webcam_image.config(image=image)
                self.webcam_image.image = image

    def capture_image(self):
        ret, frame = self.video_capture.read()
        if ret:
            filename = datetime.now().strftime("capture_%Y%m%d_%H%M%S.png")
            cv2.imwrite(os.path.join(self.capture_folder, filename), frame)
            self.status_label.config(text=f"Captured {filename}")

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.talk_button.config(text="Talk! 🎤")
            self.status_label.config(text="")
        else:
            self.is_recording = True
            self.talk_button.config(text="Stop! ⏹️")
            self.status_label.config(text="Recording...")
            threading.Thread(target=self.start_timer, daemon=True).start()
        # threading.Thread(target=self.update_frame, daemon=True).start()  # Always update the frame, regardless of recording status

    def start_timer(self):
        self.timer = 0
        self.update_timer()

    def update_timer(self):
        if self.is_recording:
            self.timer += 1
            self.status_label.config(text=f"Recording... {self.timer}s")
            self.root.after(1000, self.update_timer)

def main():
    root = tk.Tk()
    root.geometry("800x800")
    root.title("GPT play with me!")
    app = Application(root)
    root.after(100, app.start_video_stream, 0)  # Start video stream 100ms after GUI and webcam are loaded
    root.mainloop()

if __name__ == "__main__":
    main()
