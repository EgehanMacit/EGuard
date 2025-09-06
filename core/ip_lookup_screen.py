from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from threading import Thread
from network.ip_lookup import get_external_ip  # senin IP alma fonksiyonun

class IPLookupScreen(Screen):
    ip_address = StringProperty("0.0.0.0")  # KV dosyasında label ile bağlanacak

    def fetch_ip(self):
        self.ip_address = "Fetching IP address..."
        Thread(target=self._fetch_ip_thread, daemon=True).start()

    def _fetch_ip_thread(self):
        try:
            ip = get_external_ip()
            if not ip:
                ip = "Could not fetch IP"
        except Exception as e:
            ip = f"Error: {e}"
        # Kivy main thread'inde property güncelle
        self.ip_address = ip
