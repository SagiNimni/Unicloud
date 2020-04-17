from getmac import get_mac_address as gma
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'WindowsManagement\\diskScripts')
CONFIG_DIR = os.path.join(ROOT_DIR, 'configuration')
MEGA_BASH_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'MEGAcmd')
MAC_ADDRESS = gma()
