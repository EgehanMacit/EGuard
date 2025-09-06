import psutil
import time
from threading import Thread
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

class BehaviorMonitor:
    def __init__(self, callback):
        self.running = False
        self.callback = callback
        self.known_pids = {}   # pid: start time
        self.active_pids = set()  # currently active pids
        self.stopped_pids = {} # pid: stop time

    def start(self):
        self.running = True
        self.thread = Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1)

    def _monitor(self):
        while self.running:
            try:
                current_pids = set()
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    pid = proc.info['pid']
                    current_pids.add(pid)

                    if pid not in self.known_pids:
                        self.known_pids[pid] = time.time()
                        self.callback(f"Newly Started: {proc.info['name']} (PID: {pid})", status="new")
                    else:
                        elapsed = time.time() - self.known_pids[pid]
                        if elapsed >= 60:
                            self.callback(f"Running: {proc.info['name']} (PID: {pid})", status="ok")

                stopped = set(self.known_pids.keys()) - current_pids
                for pid in stopped:
                    if pid not in self.stopped_pids:
                        self.stopped_pids[pid] = time.time()
                        self.callback(f"Stopped: PID {pid}", status="error")

                self.active_pids = current_pids

                # Cleanup old stopped processes after 5 minutes
                to_delete = []
                for pid, stop_time in self.stopped_pids.items():
                    if time.time() - stop_time > 300:
                        to_delete.append(pid)
                for pid in to_delete:
                    self.stopped_pids.pop(pid, None)
                    self.known_pids.pop(pid, None)

            except Exception:
                pass
            time.sleep(2)

class BehaviorAnalysisScreen(Screen):
    def on_enter(self):
        self.ids.log_box.clear_widgets()
        self.monitor = BehaviorMonitor(callback=self.add_log)
        self.monitor.start()

    def on_leave(self):
        if hasattr(self, 'monitor'):
            self.monitor.stop()

    def add_log(self, message, status="ok"):
        def add_label(dt):
            if status == "ok":
                color = get_color_from_hex("#00FF00")  # green
            elif status == "error":
                color = get_color_from_hex("#FF0000")  # red
            elif status == "new":
                color = get_color_from_hex("#FFA500")  # orange
            else:
                color = get_color_from_hex("#FFFFFF")  # white

            lbl = Label(text=message, size_hint_y=None, height=30, color=color)
            self.ids.log_box.add_widget(lbl)

        Clock.schedule_once(add_label)
