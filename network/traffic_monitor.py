# network/traffic_monitor.py
import psutil

def aktif_ag_baglanti_listesi():
    baglantilar = psutil.net_connections()
    sonuc = []
    for c in baglantilar:
        sonuc.append({
            "fd": c.fd,
            "family": c.family.name if hasattr(c.family, "name") else str(c.family),
            "type": c.type.name if hasattr(c.type, "name") else str(c.type),
            "local_address": f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "",
            "remote_address": f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "",
            "status": c.status
        })
    return sonuc
