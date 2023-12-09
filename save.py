import cv2
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import os

class Application:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.video_capture = None
        self.audio_stream = None
        self.is_recording = False
        self.capture_folder = "captures"
        if not os.path.exists(self.capture_folder):
            os.makedirs(self.capture_folder)

    def setup_ui(self):
        # Dropdown Frame
        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(side=tk.TOP, fill=tk.X)

        # Video Devices Dropdown
        self.video_devices_dropdown = ttk.Combobox(self.dropdown_frame, font=('Helvetica', 14))
        self.video_devices_dropdown['values'] = self.detect_video_devices()
        self.video_devices_dropdown.current(0)
        self.video_devices_dropdown.bind("<<ComboboxSelected>>", self.on_video_device_change)
        self.video_devices_dropdown.pack(side=tk.LEFT, padx=(50, 0))

        # Audio Devices Dropdown
        self.audio_devices_dropdown = ttk.Combobox(self.dropdown_frame, font=('Helvetica', 14))
        self.audio_devices_dropdown['values'] = self.detect_audio_devices()
        self.audio_devices_dropdown.current(0)
        self.audio_devices_dropdown.bind("<<ComboboxSelected>>", self.on_audio_device_change)
        self.audio_devices_dropdown.pack(side=tk.RIGHT, padx=(0, 50))

        # Webcam Image
        self.webcam_label = tk.Label(self.root)
        self.webcam_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start video stream on default device
        self.start_video_stream(0)

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
        self.is_recording = True
        threading.Thread(target=self.update_frame, daemon=True).start()

    def update_frame(self):
        while self.is_recording:
            ret, frame = self.video_capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                self.webcam_label.config(image=image)
                self.webcam_label.image = image

def main():
    root = tk.Tk()
    root.geometry("800x800")
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
