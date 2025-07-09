from pathlib import Path
from nicegui import ui, app
from src.hub.db import Base, add_running_controller, get_all_running_controllers, get_controller_by_uuid, delete_controller
import json
import structlog
logger = structlog.get_logger(__name__)
'''
Notes, display each folder in static/temp (maybe rename to app?)
and the status of the controller. Each payload will hav ONE controller listed in 
the controller tab, in a stopped state.

'''


class ControllerBrowser:
    def __init__(self):
        self.list_of_files = []
        self.stats_for_nerds_dialog = ui.dialog()


    @ui.refreshable
    def render(self):
        self._get_controllers()
        self.render_controller_table()


    def _get_controllers(self):
        '''
        Recursively gets list of files under temp
        '''
        base_path = Path("temp")
        self.list_of_files = []  # Ensure it's reset each call, otherwise it stacks

        # payload that this connnector is for:
        #self.get_filtered_files()

        for file_path in base_path.rglob('*'):
            if file_path.is_file() and file_path.name == "controller.py":
                # Store relative path from 'static/packages'
                relative_path = file_path.relative_to(base_path)
                self.list_of_files.append(str(relative_path))

        return self.list_of_files

    def is_running(self, uuid) -> bool:
        '''
        Checks if a controller is running, according to db

        returns True if so, False if not

        could also edit to check PID...
        '''

        # get data from db each time:
        data = get_all_running_controllers()

        for running_controller in data:
            if running_controller.get("uuid") == uuid:
                return True
            
        return False

    def render_controller_table(self):
        with ui.row().classes("w-full justify-between p-4"):
            ui.label("Controller Name")
            ui.label("Controller UUID")
            ui.label("Controller Online [according to db]")

            with ui.dropdown_button('Actions', auto_close=True):
                ui.item('Refresh', on_click=lambda: self.render.refresh())
                # ui.item('Start All', on_click=lambda: ui.notify('You clicked item 2'))   
                # ui.item('Stop All', on_click=lambda: ui.notify('You clicked item 2'))   

            ui.separator()

        with ui.scroll_area().classes("w-full h-full"):
            logger.info(self.list_of_files)
            for file_path in self.list_of_files:
                try:
                    package_path = (Path("temp") / file_path).parent
                    config_path = str(package_path / "config.json")
                    logger.info(config_path)
                    uuid = package_path.name
                    #json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
                    # getting error about json read
                    with open(config_path, "r") as f:
                        #logger.info(f.read())
                        config = json.load(f)

                    name = config.get("payload_name").get("value", "Not Found")
                    ts_ip = config.get("cs_teamserver_ip").get("value", "Not Found")
                    ts_port = config.get("cs_teamserver_port").get("value", "Not Found")
                    #callback_server = config.get("icmp_callback_server").get("value")
                    payload_type = config.get("type").get("value", "Not Found")

                    # to get uuid, just get parent folder


                    # render row

                    with ui.row().classes("w-full h-16 justify-between items-center"):
                        ui.label(name)
                        ui.label(uuid)

                        ui.label(str(self.is_running(uuid)))
                        # all rest of stats will be in stats for nerds popup

                        #ui.label(created)
                        # Fix: capture current value as default argument
                        with ui.dropdown_button('Actions', auto_close=True):
                            ui.item('Start', on_click=lambda pp=package_path: self._start_controller(package_path=pp))
                            ui.item('Stop', on_click=lambda pp=package_path: self._stop_controller(package_path=pp))

                            # popup with more details
                            ui.item('Stats for nerds', on_click=lambda config_data=config, uuid=uuid: self.render_stats_for_nerds(config_data, uuid))                    # with ui.row():
                            #ui.item('Delete', on_click=lambda: ui.notify("not Implemented"))
                            ui.item('Delete', on_click=lambda pp=package_path: self._delete_controller(package_path=pp))

                        ui.separator()
                except Exception as e:
                    logger.error("Error with loading ...", file_path=file_path, error=e)
                    continue
    
    def render_stats_for_nerds(self, config_data, uuid):
        '''
        Dialog popupf ro stats for nerds option in contorller screen
        
        '''
        self.stats_for_nerds_dialog.clear()
        data = get_controller_by_uuid(uuid)
        with self.stats_for_nerds_dialog as dialog, ui.card().classes("w-full h-full"):
            ui.label("Config Values").classes("text-xl")
            ui.separator()

            # basic show values
            # for key,subkey in config_data.items():
            #     ui.label(f"{key} : {subkey.get("value")}")

            # table stuff
            rows = [{"Key": key, "Value": subkey.get("value", "")} for key, subkey in config_data.items()]

            ui.table(
                columns=[
                    {"name": "Key", "label": "Config Key", "field": "Key", "align": "left"},
                    {"name": "Value", "label": "Value", "field": "Value", "align": "right"},
                ],
                rows=rows,
            ).classes("w-full no-shadow")

            ui.label("Misc stats").classes("text-xl ")
            ui.separator()
            if data:

                rows = [
                    {"Label": "UUID", "Value": uuid},
                    {"Label": "Started at", "Value": data.get("started_at", "N/A")},
                    {"Label": "PID", "Value": data.get("pid", "N/A")},
                ]

                # Create the table
                ui.table(
                    columns=[
                        {"name": "Label", "label": "Label", "field": "Label", "align": "left"},
                        {"name": "Value", "label": "Value", "field": "Value", "align": "right"},
                    ],
                    rows=rows,
                ).classes("w-full no-shadow")

            else:
                ui.label("Controller not running, no running data")

            with ui.row().classes("w-full justify-between"):
                package_path = Path("temp") / uuid
                ui.button("Start Controller", on_click=lambda: self._start_controller(package_path=package_path)).classes("w-full")
                ui.button("Stop Controller", on_click=lambda: self._stop_controller(package_path=package_path)).classes("w-full")

        dialog.open()

    def _start_controller(self, package_path, refresh_class=None):
        '''
        Calls start controller & refreshes element

        refresh calss; class/element to call .refresh on
        '''
        ControllerBase(package_path=package_path).start_controller()
        self.render.refresh()


    def _stop_controller(self, package_path, refresh_class=None):
        '''
        Calls stop controller & refreshes element

        refresh calss; class/element to call .refresh on

        '''
        ControllerBase(package_path=package_path).stop_controller()
        self.render.refresh()

    def _delete_controller(self, package_path, refresh_class=None):
        '''
        Calls delete controller in ControllerBase class

        '''
        ControllerBase(package_path=package_path).delete_controller()
        self.render.refresh()

import subprocess
import shutil
import os
import signal
class ControllerBase:
    def __init__(self, package_path):
        self.package_path = Path(package_path)
        self.controller_path = self.package_path / "controller.py"
        self.uuid = package_path.name # path is temp/uuid, .name just gets uuid

    def check_if_controller_exists(self) -> bool:
        '''
        Checks if controller script file exists.
        Returns True if it exists, False otherwise.
        '''
        return self.controller_path.exists()

    def delete_controller(self):
        '''
        Deletes a controller

        '''
        ui.notify("Not Implemented")


    def start_controller(self):
        if not self.check_if_controller_exists():
            logger.info("[!] Controller seemingly does not exist. Removing from DB")
            delete_controller(self.uuid)

        python_path = shutil.which("python3")
        if not python_path:
            logger.info("Could not find 'python3' in PATH.")
            return

        logger.info(f"Found Python interpreter at {python_path}")
        logger.info(f"Starting controller from {self.controller_path}")

        try:
            proc = subprocess.Popen([python_path, str(self.controller_path)])
            logger.info(f"Started controller with PID {proc.pid}")
            ui.notify(f"Started controller with PID {proc.pid}", position="top-right", color="green")
            add_running_controller(self.uuid, pid=proc.pid)  # <-- Add `pid` to DB
        except Exception as e:
            ui.notify(e, position="top-right", color="red")
            logger.info(f"Failed to start controller: {e}")

    def stop_controller(self):
        '''
        
        Stops controller
        '''
        try:

            controller = get_controller_by_uuid(self.uuid)
            ui.notify(controller)
            pid = controller.get("pid")

            os.kill(pid, signal.SIGTERM)
            logger.info(f"Controller with PID {pid} terminated.")
            ui.notify(f"Stopped controller with PID {pid}", position="top-right", color="red")
            delete_controller(self.uuid)
        except ProcessLookupError as pe:
            ui.notify(pe, position="top-right", color="red")
            logger.info(f"Process with PID {pid} not found.")
        except Exception as e:
            ui.notify(e, position="top-right", color="red")
            logger.info(f"Error: {e}")