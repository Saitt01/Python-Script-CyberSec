import os
import pyfiglet
from termcolor import colored
import ipaddress
import sys

### ASCII IMAGE & COLOR###
title = "AUTO NMAP"
color = "blue"
ascii_art = pyfiglet.figlet_format(title)
print(colored(ascii_art,color) + "-by Andrea Saitta\n\nScanType Available:\n1. Quick: A fast scan targeting the most common ports, offering speed over thoroughness.\n2. Full:  A detailed scan that identifies open ports, services, versions, and OS info.\n3. Stealth: A slower, stealthy scan designed to evade detection by using decoy IP addresses.\n4. OS: Focuses on detecting the target's operating system based on packet responses.\n")
#Color:
error = "red"
confirm = "green"

### NMAP FUNCTION ###
# This is the funtion with all available types of nmap, based on type selected it will run on shell a specific nmap targeting the ip address given in the input, thanks to os and then it will saves the result in a file named at beginning.
def auto_nmap(target_ip, scan_type):
    # Asking User the name file for saving scan:
    while True:
        output_file = input("Save the scan as: ")
    # Checking if the file already exists:
        if os.path.exists(output_file):
            overwrite = input(f"{output_file} already exists. Overwrite? (y/n): ")
            if overwrite.lower() in ["y","Y","yes","YES"]:
                break     # If the user confirm overwrite, exit the loop and continue
            else:
                print(colored("Please choose a different file name!",error))
        else:
            break         # If the file does not exist, exit the loop and continue

    # ScanType:
    if scan_type == "1":                     # Quick
        nmap = f"nmap -T4 -F -oN {output_file} {target_ip}"
    elif scan_type == "2":                   # Full
        nmap = f"nmap -sS -sV -A -oN {output_file} {target_ip}"    
    elif scan_type == "3":                   # Stealth
        nmap = f"nmap -sS -T2 -D RND:10 -oN {output_file} {target_ip}"    
    elif scan_type == "4":                   # OS
        nmap = f"nmap -O -oN {output_file} {target_ip}"
    ### NEED MORE? ADD MORE TYPE HERE
    else:
        print(colored("Not Valid ScanType, please use:\n1. Quick\n2. Full\n3. Stealth\n4. OS\nPlease try again!",error))
        main()

    # Execute NMAP & save result:
    os.system(nmap)
    print(colored(f"\nYour scan has been saved as: {output_file}\n",confirm))

    #Cicle to Continue or Exit from the script:
    while True:
        cont_or_exit = input("Do you want to exit?\n1. Yes\n2. No, I need an other scan\nSelect: ")
        if cont_or_exit == "1":
            print("See you!")
            sys.exit()
        elif cont_or_exit == "2":
            main()
            break
        else:
            print(colored("\nInvalid Input, please try again!",error))
            
### MAIN FUNCTION ###
# This is the main function, it'll ask user the target ip address then it will check on it, thanks to ipaddress library and as last it will ask the scan type, running then the auto nmap function.
def main():
    while True:
    #TargetIP and ScanType input:
        target_ip = input("Insert TargetIP: ")
        try:
            # Validating IP Address:
            ipaddress.ip_address(target_ip)
            check_ip = input(f"TargetIP: {target_ip} - confirm?(y/n): ") 
            if check_ip in ["y","Y","yes","YES"]:
                break
            elif check_ip in ["n","N","no","NO"]:
                print(colored("Please re-enter the TargetIP",error))
            else:
                print(colored("Unknown Command: try again!\n",error))
        except ValueError:
            print(colored("Invalid IP address, please try again!",error))


    scan_type = input("Insert ScanType: ")

    #Run function:
    auto_nmap(target_ip,scan_type)

if __name__ == "__main__":
    main()

