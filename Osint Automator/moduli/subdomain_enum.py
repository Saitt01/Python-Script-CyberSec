#Questo modulo esegue una ricerca passiva dei sottodomini (subdomain enumeration) di un dominio tramite il servizio crt.sh, che fornisce i certificati SSL pubblicamente registrati.

import requests
import os
from colorama import Fore, Style

def get_subdomains_crtsh(domain):

    #Costruisco url x crtsh
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    #Set x salvare domini unici
    found = set()

    #Mando richiesta http 
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            #Se la risponsta è 200, allora converto la risposta dell'API in formato JSON
            data = response.json()

            for entry in data:
                #Per ogni entry in data, prendi il valore del campo "name_value" che contiene 1 o + sottodomini
                name = entry.get("name_value", "")

                #Per ognuno di esso, separali ogni \n e 'lisitali'
                for sub in name.split("\n"):
                    if sub.endswith(domain):
                        found.add(sub.strip())

    except Exception as e:
        print(f"{Fore.RED}Errore crt.sh: {e}{Style.RESET_ALL}")

    
    #Salvataggio
    os.makedirs("output", exist_ok=True)

    if found:
        sorted_subs = sorted(found)
        with open("output/report_subdomains.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(sorted_subs))

        print(f"{Fore.CYAN}[ SUBDOMAIN ENUM ]{Style.RESET_ALL}")
        for sub in sorted_subs:
            print(f"- {sub}")

        return f"{Fore.GREEN}✓ {len(sorted_subs)} sottodomini trovati e salvati in output/report_subdomains.txt{Style.RESET_ALL}\n"
    else:
        return f"{Fore.YELLOW}Nessun sottodominio trovato.{Style.RESET_ALL}"
