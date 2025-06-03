#Questo modulo analizza gli Header di un dominio mandando una richiesta HEAD

import requests
from colorama import Fore, Style
import os 

def analyze_header(domain):
    #Creo url
    url = f"https://{domain}" if not domain.startswith("http") else domain

    try:
        #Mando richiesta HEAD e salva risposta
        response = requests.head(url, timeout=10, allow_redirects=True)
        headers = response.headers
        #Costruisco stringa x risultato
        result = f"{Fore.CYAN}[ HTTP HEADERS ANALYSIS ]{Style.RESET_ALL}\n"
        for key, value in headers.items():
            result += f"{key}: {value}\n"
    
    except requests.exceptions.SSLError:
        result = f"{Fore.YELLOW}[!] Errore SSL. Il sito potrebbe non supportare HTTPS.{Style.RESET_ALL}"
    except requests.exceptions.RequestException as e:
        result = f"{Fore.RED}Errore durante la richiesta HEAD: {e}{Style.RESET_ALL}"
    #Salvataggio
    os.makedirs("output", exist_ok=True)
    with open("output/report_headers.txt", "w", encoding="utf-8") as f:
        f.write(result)

    return result + f"\n{Fore.GREEN}✓ Report headers salvato in output/report_headers.txt{Style.RESET_ALL}"