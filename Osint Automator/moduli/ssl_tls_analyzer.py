#Questo modulo recupera le info SSL/TLS inerenti a validità del certificato, emissione e scadenza, emittente, CA (Common Name), Algoritmo di firma e chiave pubblica ed infine eventuali problemi

import ssl 
import socket
import os
from datetime import datetime
from colorama import Fore, Style

def get_ssl_info(domain, port=443):
    try:
        #Mi connetto in maniera sicura al dominio
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                #Recupero i dati del certificato
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
        #Estraggo le informazioni + importanti
        issuer = dict(x[0] for x in cert.get("issuer",[]))
        subject = dict(x[0] for x in cert.get("subject", []))
        not_before = cert.get("notBefore")
        not_after = cert.get("notAfter")

        result = f"""
{Fore.CYAN}[ SSL/TLS CERTIFICATE INFO ]{Style.RESET_ALL}
Subject: {subject.get('commonName')}
Issuer: {issuer.get('organizationName')}
Valid From: {not_before}
Valid To: {not_after}
Cipher Suite: {cipher[0]}
Protocol Version: {cipher[1]}
Key Exchange: {cipher[2]}
"""
        #Salvataggio
        os.makedirs("output", exist_ok=True)
        with open("output/report_ssl_tls.txt", "w", encoding="utf-8") as f:
            f.write(result)

        return result + f"\n{Fore.GREEN}✓ Report headers salvato in output/report_ssl_tls.txt{Style.RESET_ALL}"
    
    except Exception as e:
        return f"{Fore.RED}Errore SSL/TLS: {e}{Style.RESET_ALL}"
    