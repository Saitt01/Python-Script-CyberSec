#Questo modulo serve a raccogliere le informazioni DNS fondamentali su un dominio Target.

import dns.resolver
import os
from colorama import Fore, Style

def resolve_record(domain, record_type):
    try:
        #Cerco dei risultati ed in caso li restituisco in testo, altrimenti lista vuota
        answers = dns.resolver.resolve(domain, record_type, lifetime=5)
        return[r.to_text() for r in answers]
    except Exception:
        return[]
#Funzione basic che restituisce l'ipotetico output
def dns_enum(domain):
    result = f"{Fore.CYAN}[ DNS ENUMERATION ]{Style.RESET_ALL}\n"
    records = {
        "A": "IPv4",
        "AAAA": "IPv6",
        "MX": "Mail Servers",
        "NS": "Name Servers",
        "TXT": "Text Records",
        "CNAME": "Canonical Name"
    }
    #Per ogni valore li stampo riga x riga
    for rtype, label in records.items():
        values = resolve_record(domain, rtype)
        result += f"\n{label} ({rtype}):\n"
        if values:
            for v in values:
                result += f" - {v}\n"
        else:
            result += " - Messun record trovato.\n"

    # Salvataggio in output
    os.makedirs("output", exist_ok=True)
    with open("output/report_dns.txt", "w", encoding="utf-8") as f:
        f.write(result)

    result += f"\n{Fore.GREEN}✓ Report DNS salvato in output/report_dns.txt{Style.RESET_ALL}"
    return result