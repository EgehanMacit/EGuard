from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

# Disable fullscreen
Config.set('graphics', 'fullscreen', '0')

# Set specific window size
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Prevent user from resizing window
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from core.behavior_analysis import BehaviorAnalysisScreen  # ✅ Correct

from core.behavior_analysis import BehaviorAnalysisScreen
from core.sandbox_analysis_gui import SandboxAnalysisScreen

# Load KV files
Builder.load_file("ui/splash.kv")
Builder.load_file("ui/main.kv")
Builder.load_file("ui/modules/scan_menu.kv")
Builder.load_file("ui/modules/scan.kv")
Builder.load_file("ui/modules/behavior_analysis.kv")
Builder.load_file("ui/modules/sandbox_analysis.kv")


class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main, 3)  # wait 3 seconds

    def switch_to_main(self, dt):
        self.manager.current = "main"


class MainScreen(Screen):
    pass


class ScanMenuScreen(Screen):
    pass


class ScanPCScreen(Screen):
    progress = NumericProperty(0)
    scanning_event = None

    def start_scan(self):
        self.progress = 0
        self.ids.result_label.text = "Scan started..."
        self.scanning_event = Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        if self.progress >= 100:
            self.ids.result_label.text = "Scan completed! No viruses found."
            if self.scanning_event:
                self.scanning_event.cancel()
            return False
        self.progress += 1
        self.ids.progress_bar.value = self.progress

    def stop_scan(self):
        if self.scanning_event:
            self.scanning_event.cancel()
            self.ids.result_label.text = "Scan stopped."


class EgeGuardApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ScanMenuScreen(name="scan_menu"))
        sm.add_widget(ScanPCScreen(name="scan_pc"))
        sm.add_widget(BehaviorAnalysisScreen(name="behavior_analysis"))
        sm.add_widget(SandboxAnalysisScreen(name="sandbox_analysis"))
        sm.add_widget(FileScannerScreen(name="file_scanner"))
        sm.add_widget(QuarantineScreen(name="quarantine_report"))
        sm.add_widget(NetworkMenuScreen(name="network_menu"))
        sm.add_widget(PortScannerScreen(name="port_scanner"))
        sm.add_widget(TrafficMonitorScreen(name="traffic_monitor"))
        sm.add_widget(IPLookupScreen(name="ip_lookup"))
        sm.add_widget(IPWhoisScreen(name="ip_whois"))
        sm.add_widget(BlacklistScreen(name="blacklist"))

        return sm


from core.file_scanner_screen import FileScannerScreen
from kivy.uix.screenmanager import ScreenManager

screen_manager = ScreenManager()
screen_manager.add_widget(FileScannerScreen(name="file_scanner"))

from kivy.uix.screenmanager import Screen


class ScanMenuScreen(Screen):
    pass


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from core.scan_menu_screen import ScanMenuScreen
from core.file_scanner_screen import FileScannerScreen
from core.quarantine_screen import QuarantineScreen

# Load KV files
Builder.load_file("ui/modules/scan_menu.kv")
Builder.load_file("ui/modules/file_scanner.kv")
Builder.load_file("ui/modules/quarantine_report.kv")
Builder.load_file("ui/modules/port_scanner.kv")
Builder.load_file("ui/modules/traffic_monitor.kv")
Builder.load_file("ui/modules/ip_lookup.kv")
Builder.load_file("ui/modules/ip_whois.kv")
Builder.load_file("ui/modules/blacklist.kv")

from core.network_menu_screen import NetworkMenuScreen

Builder.load_file("ui/modules/network_menu.kv")

from network.port_scanner_screen import PortScannerScreen
from core.traffic_monitor_screen import TrafficMonitorScreen
from core.ip_lookup_screen import IPLookupScreen
from core.ip_whois_screen import IPWhoisScreen
from core.blacklist_screen import BlacklistScreen

import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    EgeGuardApp().run()
