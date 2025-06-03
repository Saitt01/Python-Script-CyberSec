#Questo modulo serve a raccogliere: DOMINIO, REGISTRAR, DATA CREAZIONE, AGGIORNAMENTO, SCADENZA, SERVER DNS E STATO.

import requests
import os
from colorama import Fore, Style

API_KEY = "INSERISCI LA TUA API QUI/INSERT HERE UR API :)"
API_URL = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

def safe(value, fallback="Non disponibile"):
    if isinstance(value, list):
        return ", ".join(value) if value else fallback
    return value if value else fallback

def get_whois_info(domain):
    #Setto i parametri x la richiesta API
    params = {
        "apiKey": API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    try:
        #Mando richiesta API e richedo risposta in JSON
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()

        whois = data.get("WhoisRecord", {})

        output = f"""
{Fore.CYAN}[ WHOIS INFO ]{Style.RESET_ALL}
Domain: {safe(whois.get('domainName'))}
Registrar: {safe(whois.get('registrarName'))}
Creation Date: {safe(whois.get('createdDate'))}
Expiration Date: {safe(whois.get('expiresDate'))}
Last Updated: {safe(whois.get('updatedDate'))}
Name Servers: {safe(whois.get('nameServers', {}).get('hostNames'))}
Status: {safe(whois.get('status'))}
"""

        if not whois.get("domainName"):
            output += f"\n{Fore.YELLOW}⚠️ Attenzione: il dominio potrebbe utilizzare un TLD che oscura le informazioni WHOIS pubbliche (es. .dev, .app){Style.RESET_ALL}\n"

        #Salvatasggio
        os.makedirs("output", exist_ok=True)
        with open("output/report_whois.txt", "w", encoding="utf-8") as f:
            f.write(output)

        return output + f"{Fore.GREEN}✓ Report WHOIS salvato in output/report_whois.txt{Style.RESET_ALL}\n"

    except Exception as e:
        return f"{Fore.RED}Errore WHOIS API: {e}{Style.RESET_ALL}"
