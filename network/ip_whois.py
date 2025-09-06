from ipwhois import IPWhois
import requests

def get_whois_info(ip):
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap(depth=1)
        return res
    except Exception as e:
        return {"error": str(e)}

def get_country_info(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country_name": data.get("country_name"),
                "country_code": data.get("country_code"),
                "region": data.get("region"),
                "city": data.get("city"),
                "org": data.get("org"),
            }
        else:
            return {"error": "Could not retrieve country information."}
    except Exception as e:
        return {"error": str(e)}
