# Questo tool serve a raccogliere, analizzare e presentare le informazioni pubbliche (OSINT) trovate su un dominio.

import pyfiglet
from colorama import Fore,Style
from moduli.whois_lookup import get_whois_info
from moduli.subdomain_enum import get_subdomains_crtsh
from moduli.dns_enum import dns_enum
from moduli.header_analyzer import analyze_header
from moduli.ssl_tls_analyzer import get_ssl_info
from moduli.ip_lookup import ip_lookup
import os

ascii_art = pyfiglet.figlet_format("OsintAutomator", font="slant")

if __name__ == "__main__":
    print(f"{Fore.CYAN}{ascii_art}-by saitt01\n{Style.RESET_ALL}")
    domain = input("Inserisci il dominio (es. esempio.com): ")
    print(get_whois_info(domain))
    print(get_subdomains_crtsh(domain))
    print(dns_enum(domain))
    print(analyze_header(domain))
    print(get_ssl_info(domain))
    print(ip_lookup(domain))



