from nicegui import ui, app
from pathlib import Path
from src.hub.protocolhub import ProtocolHub, FileBrowser
from src.hub.controllerhub import ControllerBrowser, ControllerBase
from src.hub.db import get_all_running_controllers
import os 
import subprocess
import shutil

def main():
    set_needed_perms()
    restart_controllers()
    #Add static files & make sure it exists
    print("Serving static dir")
    # make needed directories BEFORE everything else gets called, otherwise path not found/dir not exist errors may happen
    Path("static").mkdir(parents=True, exist_ok=True)
    Path("static/packages").mkdir(parents=True, exist_ok=True)
    #Path("static/packages").mkdir(parents=True, exist_ok=True)
    app.add_static_files('/static', 'static')

    print("Running")
    ui.run(host="0.0.0.0", port=9000, reload=False, dark=True)

def set_needed_perms():
    print("=" * 50)
    print("ICMP packet crafting requires the Python interpreter to have CAP_NET_RAW permission.")

    # Get the path to the current Python interpreter
    default_python_path = shutil.which("python3")
    resolved_path = os.path.realpath(default_python_path)
    
    print(f"\nDefault Python interpreter: {resolved_path}")
    
    # Check current capabilities
    try:
        result = subprocess.run(['getcap', resolved_path], capture_output=True, text=True, check=False)
        if 'cap_net_raw=ep' in result.stdout:
            print(f"CAP_NET_RAW is already set on {resolved_path}. No action needed.")
            print("=" * 50)
            return

    except FileNotFoundError:
        print("'getcap' not found")
        exit()
        return
    
    custom = input("Would you like to use a different Python interpreter? (y/N): ").strip().lower()

    if custom == 'y':
        custom_path = input("Enter full path to the Python interpreter: ").strip()
        if not os.path.exists(custom_path):
            print("Error: Path does not exist.")
            return
        resolved_path = os.path.realpath(custom_path)

    print(f"\nThe following command will be executed:\n")
    print(f"sudo setcap cap_net_raw+ep {resolved_path}")
    print("You may be prompted for your sudo password...\n")

    confirm = input("\nDo you want to proceed? (Y/n): ").strip().lower()
    if confirm == 'n':
        print("Operation cancelled by user.")
        return

    try:
        subprocess.run(['sudo', 'setcap', 'cap_net_raw+ep', resolved_path], check=True)
        print("CAP_NET_RAW permission set successfully.")
    except subprocess.CalledProcessError:
        print("Failed to set permission. You might need sudo privileges. The ICMP controller will need to be run manually, instead of through the web interface")
    print("=" * 50)

def restart_controllers():
    '''
    Restarts controllers listed in db
    
    '''
    running_controllers = get_all_running_controllers()

    for controller in running_controllers:
        print(f"Starting previously running controller '{controller}'")
        package_path = Path("temp") / controller
        c = ControllerBase(package_path=package_path)
        c.start_controller()

    

@ui.page('/')
def index():
    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        # p = ProtocolHub()
        # p.render()

        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Controllers')
            two = ui.tab('CS-EXTC2-HUB')
            three = ui.tab('Generate Package')
            four = ui.tab('Files')

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



