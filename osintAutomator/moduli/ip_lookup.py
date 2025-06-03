#Questo modulo ha la funzione scoprire dove si trova il server fisicamente, chi è il provider/host e se l'ip è un cloud provider, un ISP privato o un datacenter

import requests
import socket
import os
from colorama import Fore, Style

def ip_lookup(domain):
    try:
        #Risolvo IP e utilizzo API di ip-api.com per ottenere le informazioni
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = response.json()

        if data["status"] == "success":
            result = f"""
{Fore.CYAN}[ IP GEOLOCATION & HOSTING INFO ]{Style.RESET_ALL}
IP Address: {ip}
Country: {data.get('country')} ({data.get('countryCode')})
Region: {data.get('regionName')}
City: {data.get('city')}
ISP: {data.get('isp')}
Org: {data.get('org')}
Hosting: {data.get('org')}
ASN: {data.get('as')}
Reverse DNS: {data.get('reverse', 'N/A')}
"""

        else:
            result = f"{Fore.YELLOW}Impossibile recuperare le info per l'IP {ip}.{Style.RESET_ALL}"

    except Exception as e:
        result = f"{Fore.RED}Errore durante la geolocalizzazione IP: {e}{Style.RESET_ALL}"

    #Salvataggio
    os.makedirs("output", exist_ok=True)
    with open("output/report_ip_lookup.txt", "w", encoding="utf-8") as f:
        f.write(result)

    return result + f"\n{Fore.GREEN}✓ Report IP salvato in output/report_ip_lookup.txt{Style.RESET_ALL}"
