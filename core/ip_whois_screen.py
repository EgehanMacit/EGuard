from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from threading import Thread
from network.ip_whois import get_whois_info, get_country_info

class IPWhoisScreen(Screen):
    result_text = StringProperty("")

    def query(self):
        ip = self.ids.ip_input.text.strip()
        if not ip:
            self.result_text = "Please enter a valid IP."
            return
        self.result_text = "Querying..."
        Thread(target=self._query_thread, args=(ip,), daemon=True).start()

    def _query_thread(self, ip):
        try:
            whois = get_whois_info(ip)
            country = get_country_info(ip)

            result = ""

            if "error" in whois:
                result += f"Whois Error: {whois['error']}\n"
            else:
                net = whois.get('network', {})
                remarks = net.get('remarks', [{}])
                result += f"Whois:\nOrg: {net.get('name', 'Unknown')}\n"
                result += f"Handle: {net.get('handle', 'Unknown')}\n"
                result += f"Address: {remarks[0].get('description', 'Unknown')}\n"

            if "error" in country:
                result += f"\nCountry Info Error: {country['error']}"
            else:
                result += f"\nCountry: {country.get('country_name', 'Unknown')} ({country.get('country_code', '')})\n"
                result += f"City: {country.get('city', 'Unknown')}\n"
                result += f"Organization: {country.get('org', 'Unknown')}"

            self.result_text = result
        except Exception as e:
            self.result_text = f"Unexpected error: {str(e)}"
