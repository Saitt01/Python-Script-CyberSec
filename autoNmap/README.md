### Auto Nmap ###

**Auto Nmap** is a Python script that automates different types of Nmap scans, saving the results into custom-named files.

## Features

- **Quick Scan**: A fast scan targeting the most common ports for quick insights.
- **Full Scan**: A comprehensive scan that identifies open ports, services, versions, and OS details.
- **Stealth Scan**: A stealthy scan using decoy IP addresses to evade detection.
- **OS Scan**: Focused on detecting the target's operating system by analyzing packet responses.

## Requirements

To run this script, you need:

- Python 3.x
- The following Python libraries:
  - `os`
  - `pyfiglet`
  - `termcolor`
  - `ipaddress`
  - `sys`
- **Nmap** installed on your system (you can install it with `sudo apt install nmap` on Linux-based systems).

## Installation

1. Clone the repository:

   git clone https://github.com/Saitt01/Python-Script-CyberSec.git


2. Navigate to the project directory:

    cd auto-nmap

3. Install the required dependencies:

    pip install -r requirements.txt

4. Make sure Nmap is installed on your system.

## Usage

1. Run the script:

    python auto_nmap.py

2. Enter the target IP address and choose the desired scan type:

    1: Quick Scan
    2: Full Scan
    3: Stealth Scan
    4: OS Scan

3. Choose a file name to save the scan results.

## Contributing

If you want to contribute to this project, feel free to make a pull request or open an issue!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.