from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from network.traffic_monitor import aktif_ag_baglanti_listesi
from kivy.clock import Clock

class TrafficMonitorScreen(Screen):
    connection_list = ObjectProperty()  # KV id ile eşleşecek

    def on_pre_enter(self):
        self.update_connections()

    def update_connections(self, *args):
        connections = aktif_ag_baglanti_listesi()
        text = ""
        for c in connections:
            text += f"{c['local_address']} -> {c['remote_address']} [{c['status']}]\n"
        if self.connection_list:
            self.connection_list.text = text

    def start_auto_update(self):
        # Optionally update every 5 seconds
        self.event = Clock.schedule_interval(self.update_connections, 5)

    def stop_auto_update(self):
        if hasattr(self, 'event'):
            self.event.cancel()
