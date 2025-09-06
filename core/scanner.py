from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
import os
import hashlib

class ScanPCScreen(Screen):
    scanning = False
    progress = 0
    scanned_files = 0
    total_files = 0

    def start_scan(self):
        self.scanning = True
        self.ids.result_box.clear_widgets()
        Clock.schedule_interval(self.scan_step, 0.1)
        self.files = self.get_files("C:/Users")  # Folder to scan automatically
        self.total_files = len(self.files)
        self.scanned_files = 0

    def stop_scan(self):
        self.scanning = False
        self.ids.progress_label.text = "Scan stopped."

    def get_files(self, directory):
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
        return file_list

    def scan_step(self, dt):
        if not self.scanning or self.scanned_files >= self.total_files:
            return False

        file = self.files[self.scanned_files]
        result = self.check_file(file)

        self.ids.result_box.add_widget(Label(text=result))

        self.scanned_files += 1
        self.progress = int((self.scanned_files / self.total_files) * 100)
        self.ids.progress_bar.value = self.progress
        self.ids.progress_label.text = f"%{self.progress}"

        return True

    def check_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
                file_hash = hashlib.sha256(data).hexdigest()
                # Simple example hash (replace with real virus signatures)
                if file_hash == "d41d8cd98f00b204e9800998ecf8427e":
                    return f"[MALICIOUS] {file_path}"
        except:
            return f"[SKIPPED] {file_path}"
        return f"[SAFE] {file_path}"
