from getmac import get_mac_address as gma
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'WindowsManagement\\diskScripts')
CONFIG_DIR = os.path.join(ROOT_DIR, 'configuration')
DRIVES_LIST_DIR = os.path.join(ROOT_DIR, 'GUI\\mappedDrives.ini')
MEGA_BASH_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'MEGAcmd')
MAC_ADDRESS = gma()

# TODO service and changes support between devices that are connected to same account
# TODO encryption between The Unicloud database and user
# TODO requirements for sign up password
# TODO Android support
# TODO web support(HTML and HTTP)
# TODO Disconnect from Unicloud account
# TODO setup.py installer
