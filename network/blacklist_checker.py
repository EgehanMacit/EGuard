import requests

API_KEY = "YOUR_OWN_API_KEY"  # Place your AbuseIPDB API key here

def check_ip_blacklist(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY,
    }
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            if data.get("data", {}).get("abuseConfidenceScore", 0) > 0:
                return {
                    "listed": True,
                    "score": data["data"]["abuseConfidenceScore"],
                    "country": data["data"]["countryCode"],
                    "usageType": data["data"]["usageType"],
                    "isp": data["data"]["isp"],
                    "domain": data["data"]["domain"],
                    "lastReported": data["data"]["lastReportedAt"],
                    "reports": data["data"]["totalReports"],
                }
            else:
                return {"listed": False}
        else:
            return {"error": data.get("errors", "Unknown error")}
    except Exception as e:
        return {"error": str(e)}
