from nicegui import ui, app
from pathlib import Path
from src.hub.protocolhub import ProtocolHub, FileBrowser
from src.hub.controllerhub import ControllerBrowser, ControllerBase
from src.hub.db import get_all_running_controllers, delete_controller
import os 
import subprocess
import shutil
import logging

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG, WARNING, ERROR, CRITICAL as needed
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    set_needed_perms()
    restart_controllers()
    #Add static files & make sure it exists
    logging.info("Serving static dir")
    # make needed directories BEFORE everything else gets called, otherwise path not found/dir not exist errors may happen
    Path("static").mkdir(parents=True, exist_ok=True)
    Path("static/packages").mkdir(parents=True, exist_ok=True)
    #Path("static/packages").mkdir(parents=True, exist_ok=True)
    app.add_static_files('/static', 'static')

    logging.info("Running")
    ui.run(host="0.0.0.0", port=9000, reload=False, dark=True, title="CS-EXTC2-HUB")

def set_needed_perms():
    logging.info("=" * 50)
    logging.info("ICMP packet crafting requires the Python interpreter to have CAP_NET_RAW permission.")

    # Get the path to the current Python interpreter
    default_python_path = shutil.which("python3")
    resolved_path = os.path.realpath(default_python_path)
    
    logging.info(f"Default Python interpreter: {resolved_path}")
    
    # Check current capabilities
    try:
        result = subprocess.run(['getcap', resolved_path], capture_output=True, text=True, check=False)
        if 'cap_net_raw=ep' in result.stdout:
            logging.info(f"CAP_NET_RAW is already set on {resolved_path}. No action needed.")
            logging.info("=" * 50)
            return

    except FileNotFoundError:
        logging.info("'getcap' not found")
        exit()
        return
    
    custom = input("Would you like to use a different Python interpreter? (y/N): ").strip().lower()

    if custom == 'y':
        custom_path = input("Enter full path to the Python interpreter: ").strip()
        if not os.path.exists(custom_path):
            logging.info("Error: Path does not exist.")
            return
        resolved_path = os.path.realpath(custom_path)

    logging.info(f"\nThe following command will be executed:\n")
    logging.info(f"sudo setcap cap_net_raw+ep {resolved_path}")
    logging.info("You may be prompted for your sudo password...\n")

    confirm = input("\nDo you want to proceed? (Y/n): ").strip().lower()
    if confirm == 'n':
        logging.info("Operation cancelled by user.")
        return

    try:
        subprocess.run(['sudo', 'setcap', 'cap_net_raw+ep', resolved_path], check=True)
        logging.info("CAP_NET_RAW permission set successfully.")
    except subprocess.CalledProcessError:
        logging.info("Failed to set permission. You might need sudo privileges. The ICMP controller will need to be run manually, instead of through the web interface")
    logging.info("=" * 50)

def restart_controllers():
    '''
    Restarts controllers listed in db
    
    '''
    running_controllers = get_all_running_controllers()

    for controller in running_controllers:
        package_path = Path("temp") / controller.get("uuid")

        # check if controller exists first, if not, pass
        if not package_path.exists():
            logging.info(f"[!] Cannot restart controller {controller.get("uuid")}, it does not exist. Removing from db")
            delete_controller(controller.get("uuid"))
            return

        # remove stale entry
        #delete_controller(controller.get("uuid"))
        logging.info(f"[+] Starting previously running controller '{controller.get("uuid")}'")
        c = ControllerBase(package_path=package_path)
        c.start_controller()

    

@ui.page('/')
def index():
    ui.add_head_html(r'''
    <style>
    @font-face {
        font-family: "Audiowide";
        src: url('/static/quantico.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }

    /* Apply globally (optional) */
    body {
        font-family: "Audiowide", sans-serif;
        /* font-size: 18px; /* Set size here */
        /*font-weight: bold;*/
    }
                     
    head {
        font-family: "Audiowide", sans-serif;
        font-size: 18px; /* Set size here */
        font-weight: bold;
    }
    </style>

    ''')

    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        # p = ProtocolHub()
        # p.render()

        with ui.tabs().classes('w-full').classes("bold") as tabs:
            #one = ui.tab('Controllers').classes("font-[Audiowide]")#.style('font-family: Audiowide;')
            one = ui.tab('Controllers').style('font-family: Audiowide;').classes("text-[17px] bold")#.style('font-family: Audiowide;')
            
            two = ui.tab('CS-EXTC2-HUB').style('font-family: Audiowide;').classes("text-xl")
            three = ui.tab('Generate Package').style('font-family: Audiowide;')
            four = ui.tab('Packages').style('font-family: Audiowide;')

        ui.separator()

        with ui.tab_panels(tabs, value=two).classes('w-full'):
            with ui.tab_panel(one):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    c = ControllerBrowser()
                    c.render()
                
            with ui.tab_panel(two):
                #ui.label("CS-EXTC2-HUB")
                ui.label("Main Page")
                ui.label("explanation of extc2 here?")

            with ui.tab_panel(three):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    p = ProtocolHub()
                    p.render()

            with ui.tab_panel(four):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    fb = FileBrowser("static/packages")
                    fb.render()



