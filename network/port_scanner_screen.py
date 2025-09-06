# network/port_scanner_screen.py

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from threading import Thread
from .port_scanner import scan_ports  # import from the same network folder

class PortScannerScreen(Screen):
    ip_input = ObjectProperty()
    start_port_input = ObjectProperty()
    end_port_input = ObjectProperty()
    result_list = ObjectProperty()

    def start_scan(self):
        ip = self.ip_input.text.strip()
        try:
            start = int(self.start_port_input.text)
            end = int(self.end_port_input.text)
        except ValueError:
            self.result_list.text = "Port numbers are not valid."
            return

        self.result_list.text = "Scanning..."
        Thread(target=self.scan_ports_thread, args=(ip, start, end), daemon=True).start()

    def scan_ports_thread(self, ip, start, end):
        open_ports = scan_ports(ip, start, end)
        result_text = "Open ports:\n" + "\n".join(str(p) for p in open_ports) if open_ports else "No open ports found."
        self.result_list.text = result_text
