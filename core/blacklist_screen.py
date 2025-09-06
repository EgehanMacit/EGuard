from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from threading import Thread
from network.blacklist_checker import check_ip_blacklist

class BlacklistScreen(Screen):
    ip_input = StringProperty("")
    sonuc_text = StringProperty("")

    def sorgula(self):
        ip = self.ids.ip_input.text.strip()
        if not ip:
            self.sonuc_text = "Please enter a valid IP."
            return
        self.sonuc_text = "Checking..."
        Thread(target=self._sorgu_thread, args=(ip,), daemon=True).start()

    def _sorgu_thread(self, ip):
        result = check_ip_blacklist(ip)
        if "error" in result:
            self.sonuc_text = f"Error: {result['error']}"
        elif result.get("listed"):
            self.sonuc_text = (
                f"IP is Blacklisted!\n"
                f"Confidence Score: {result['score']}\n"
                f"Country: {result['country']}\n"
                f"Usage Type: {result['usageType']}\n"
                f"ISP: {result['isp']}\n"
                f"Domain: {result['domain']}\n"
                f"Last Reported: {result['lastReported']}\n"
                f"Total Reports: {result['reports']}"
            )
        else:
            self.sonuc_text = "IP is Not Blacklisted."
