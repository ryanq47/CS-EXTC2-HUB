from nicegui import ui, app
from pathlib import Path
from src.hub.protocolhub import ProtocolHub
from src.hub.filebrowser import FileBrowser
from src.hub.controllerhub import ControllerBrowser, ControllerBase
from src.hub.extc2 import ExtC2Overview
from src.hub.db import get_all_running_controllers, delete_controller
import os 
import subprocess
import shutil
import structlog


logger = structlog.get_logger(__name__)


def main():
    set_needed_perms()
    restart_controllers()
    #Add static files & make sure it exists
    logger.info("Serving static dir")
    # make needed directories BEFORE everything else gets called, otherwise path not found/dir not exist errors may happen
    Path("static").mkdir(parents=True, exist_ok=True)
    Path("static/packages").mkdir(parents=True, exist_ok=True)
    #Path("static/packages").mkdir(parents=True, exist_ok=True)
    app.add_static_files('/static', 'static')

    logger.info("Running")
    ui.run(host="0.0.0.0", port=9000, reload=False, dark=True, title="CS-EXTC2-HUB")

def set_needed_perms():
    logger.info("=" * 50)
    logger.info("ICMP packet crafting requires the Python interpreter to have CAP_NET_RAW permission.")

    # Get the path to the current Python interpreter
    default_python_path = shutil.which("python3")
    resolved_path = os.path.realpath(default_python_path)
    
    logger.info(f"Default Python interpreter: {resolved_path}")
    
    # Check current capabilities
    try:
        result = subprocess.run(['getcap', resolved_path], capture_output=True, text=True, check=False)
        if 'cap_net_raw=ep' in result.stdout:
            logger.info(f"CAP_NET_RAW is already set on {resolved_path}. No action needed.")
            logger.info("=" * 50)
            return

    except FileNotFoundError:
        logger.info("'getcap' not found")
        exit()
        return
    
    custom = input("Would you like to use a different Python interpreter? (y/N): ").strip().lower()

    if custom == 'y':
        custom_path = input("Enter full path to the Python interpreter: ").strip()
        if not os.path.exists(custom_path):
            logger.info("Error: Path does not exist.")
            return
        resolved_path = os.path.realpath(custom_path)

    logger.info(f"\nThe following command will be executed:\n")
    logger.info(f"sudo setcap cap_net_raw+ep {resolved_path}")
    logger.info("You may be prompted for your sudo password...\n")

    confirm = input("\nDo you want to proceed? (Y/n): ").strip().lower()
    if confirm == 'n':
        logger.info("Operation cancelled by user.")
        return

    try:
        subprocess.run(['sudo', 'setcap', 'cap_net_raw+ep', resolved_path], check=True)
        logger.info("CAP_NET_RAW permission set successfully.")
    except subprocess.CalledProcessError:
        logger.info("Failed to set permission. You might need sudo privileges. The ICMP controller will need to be run manually, instead of through the web interface")
    logger.info("=" * 50)

def restart_controllers():
    '''
    Restarts controllers listed in db
    
    '''
    running_controllers = get_all_running_controllers()

    for controller in running_controllers:
        package_path = Path("temp") / controller.get("uuid")

        # check if controller exists first, if not, pass
        if not package_path.exists():
            logger.info(f"[!] Cannot restart controller {controller.get('uuid')}, it does not exist. Removing from db")
            delete_controller(controller.get("uuid"))
            return

        # remove stale entry
        #delete_controller(controller.get("uuid"))
        logger.info(f"[+] Starting previously running controller '{controller.get('uuid')}'")
        c = ControllerBase(package_path=package_path)
        c.start_controller()

    

#@ui.page('/')
def header():
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

    # make scroll bar for overflow go bye bye. Works with h-96px in routing section of code.
    ui.add_body_html('''
    <style>
    html, body {
        overflow: hidden;
    }
    </style>
    ''')

    with ui.header().classes("bg-black"):
        with ui.element().classes("flex justify-center items-center gap-4 w-full"):
            ui.button("Controllers", on_click=lambda: ui.navigate.to("/controllers")).props("flat").classes("text-white")
            ui.button("EXTC2-HUB", on_click=lambda: ui.navigate.to("/")).props("flat").classes("text-white")
            ui.button("Generate", on_click=lambda: ui.navigate.to("/packages/generate")).props("flat").classes("text-white")
            ui.button("Packages", on_click=lambda: ui.navigate.to("/packages")).props("flat").classes("text-white")

@ui.page('/')
def extc2():
    header()
    with ui.column().classes("w-full h-[calc(100vh-96px)]"):
        e2o = ExtC2Overview()
        e2o.render()


@ui.page('/controllers')
def cb():
    header()
    with ui.column().classes("w-full h-[calc(100vh-96px)]"):
        c = ControllerBrowser()
        c.render()

@ui.page('/packages/generate')
def gp():
    header()
    with ui.column().classes("w-full h-[calc(100vh-96px)] "):
        p = ProtocolHub()
        p.render()


@ui.page('/packages')
def fb():
    header()

    with ui.column().classes("w-full h-[calc(100vh-96px)] "):
        fb = FileBrowser("static/packages")
        fb.render()


