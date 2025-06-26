from pathlib import Path
from nicegui import ui, app
from src.hub.db import Base, add_or_update_agent
import json
'''
Notes, display each folder in static/temp (maybe rename to app?)
and the status of the connector. Each payload will hav ONE connector listed in 
the connector tab, in a stopped state.

'''


class ConnectorBrowser:
    def __init__(self):
        self.list_of_files = []

    @ui.refreshable
    def render(self):
        self._get_controllers()
        self.render_connector_table()
        #print(self.list_of_files)
        #self.render_files_table()

    def _get_controllers(self):
        '''
        Recursively gets list of files under temp
        '''
        base_path = Path("temp")
        #self.list_of_files = []  # Ensure it's reset

        # payload that this connnector is for:
        #self.get_filtered_files()

        for file_path in base_path.rglob('*'):
            if file_path.is_file() and file_path.name == "controller.py":
                # Store relative path from 'static/packages'
                relative_path = file_path.relative_to(base_path)
                self.list_of_files.append(str(relative_path))

        return self.list_of_files


    def render_connector_table(self):
        with ui.row().classes("w-full justify-between p-4"):
            ui.label("Connector Name")
            ui.label("Connector Name")
            ui.label("Connector Name")
            ui.label("Connector Name")

            # ui.label("File Path")
            # ui.label("Time Stamp")
            # ui.button(icon="refresh")

            with ui.dropdown_button('Actions', auto_close=True):
                ui.item('Refresh', on_click=lambda: ui.notify('You clicked item 1'))
                ui.item('Start All', on_click=lambda: ui.notify('You clicked item 2'))   
                ui.item('Stop All', on_click=lambda: ui.notify('You clicked item 2'))   

            ui.separator()

        with ui.scroll_area().classes("w-full h-full"):
            print(self.list_of_files)
            for file_path in self.list_of_files:
                base_path = (Path("temp") / file_path).parent
                config_path = str(base_path / "config.json")
                print(config_path)
                         
                #json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
                # getting error about json read
                with open(config_path, "r") as f:
                    #print(f.read())
                    config = json.load(f)

                name = config.get("payload_name").get("value", "Not Found")
                ts_ip = config.get("cs_teamserver_ip").get("value", "Not Found")
                ts_port = config.get("cs_teamserver_port").get("value", "Not Found")
                #callback_server = config.get("icmp_callback_server").get("value")
                payload_type = config.get("type").get("value", "Not Found")

                # to get uuid, just get parent folder

                file_path = Path("temp") / file_path

                # render row

                with ui.row().classes("w-full h-16 justify-between items-center"):
                    ui.label(name)
                    ui.label("UUID_HERE")
                    #ui.label(ts_ip)
                    #ui.label(ts_port)
                    ui.label(payload_type)
                    # all rest of stats will be in stats for nerds popup

                    #ui.label(created)
                    # Fix: capture current value as default argument
                    with ui.dropdown_button('Actions', auto_close=True):
                        ui.item('Start', on_click=lambda: ui.notify('You clicked item 1'))
                        ui.item('Stop', on_click=lambda: ui.notify('You clicked item 2'))  

                        # popup with more details
                        ui.item('Stats for nerds', on_click=lambda: ui.notify('You clicked item 2'))                    # with ui.row():

                    ui.separator()

                # with ui.row().classes("w-full h-16 justify-between items-center"):
                #     ui.label("connector_name")
                #     #ui.label(str(file_path))
                #     #ui.label(created)
                #     # Fix: capture current value as default argument
                #     with ui.row():
                #         ui.button('Stop').props("color=red")
                #         ui.button('Start')
                #     ui.separator()


import importlib
import sys
import threading  
class ConnectorBase:
    def __init__(self):
        ...

    def run_py_script_in_thread(script_path):
        #import module as module.name
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        # load it into loaded mods
        sys.modules["module.name"] = module
        # and execute it
        spec.loader.exec_module(module)

        if hasattr(module, 'go'):
            thread = threading.Thread(target=module.go)
            thread.start()
            #module.go()  # Run the go function in the script
        else:
            print(f"Error: 'go' function not found in {script_path}")




    def stop_connector(self):
        '''
        
        Stops connector
        '''

    