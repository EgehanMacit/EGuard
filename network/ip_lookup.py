import requests

def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            ip = response.json().get('ip')
            return ip
        else:
            return "Could not retrieve IP information."
    except Exception as e:
        return f"Error: {str(e)}"
