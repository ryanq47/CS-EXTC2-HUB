from nicegui import ui, app
from pathlib import Path
import json
import subprocess 
from src.hub.controllerhub import ControllerBase
from src.hub.compile import Compile
import structlog

logger = structlog.get_logger(__name__)

class ProtocolHub:
    def __init__(self):
        pass

        self.payload_options_dict = {
            "someoption1": {
                "value":"blank",
                "description":"blank"
            }
        }
        self.currently_selected_payload = None

    #@ui.refreshable
    def render(self):
        with ui.card().classes('w-full h-full'):
            with ui.splitter(limits=[50,50]).classes("w-full h-full") as splitter:
                with splitter.before:
                        #p-4 for padding cuz w-full wipes padding
                        with ui.column().classes("w-full h-full p-4"):
                            self.payload_selector()
                        #ui.label("left")
                with splitter.after:
                    with ui.scroll_area().classes("h-full"):
                        self.payload_options()

    def payload_selector(self):
        #with ui.element().classes('p-4 w-full h-full'):
        options = self._get_payload_names()
        ui.label("Payload Selector").classes("text-xl")
        ui.separator()
        selector = ui.select(value="icmp_x86", on_change=lambda x: self.update_options(selector.value), label="Payloads", options=options).classes("w-96").props("filled square")
        #update options at first load
        self.update_options(selector.value)

        #buttons at bottom
        with ui.row().classes("absolute bottom-8 justify-center space-x-4"): # [ ] center + [x] pin to bottom
            #ui.button("Generate Payload")#.classes('flex-1 p-0')
            #ui.button("Generate Controller")#.classes('flex-1 p-0') # mayeb later have a run controller option
            ui.button("Generate Package", on_click=lambda:self._on_click_generate_action())#.classes('flex-1 p-0')
            
            self.start_controller_checkbox = ui.checkbox("Start Controller", value=False)
            with self.start_controller_checkbox:
                ui.tooltip("Automatically start a controller on this host, for this package on generation")

    def update_options(self, payload_name):
        self.currently_selected_payload = payload_name
        # get proper options here

        self.payload_options_dict = self._get_payload_options()

        self.payload_options.refresh()

    def _get_payload_names(self):
        '''
        Return list of payloads
        '''
        p = Path("payloads")
        list_of_payloads = []
        for payload_name in p.iterdir():
            if payload_name.is_dir():
                #comes out to 'payloads/<NAME>, need to strip payloads/
                list_of_payloads.append(str(payload_name).replace('payloads/',''))
        return list_of_payloads

    def _get_payload_options(self):
        config_file = Path("payloads") / self.currently_selected_payload / "config.json"

        #ui.notification(config_file)

        with open(config_file, "r") as config_options:
            #logger.info(config_options.read())
            return json.loads(config_options.read())

    def _on_click_generate_action(self):
        '''
        Called when the "generate" option is selected
        
        '''
        # start comp:
        compile_class = Compile(payload_name=self.currently_selected_payload, payload_options_dict=self.payload_options_dict)
        compile_class.run()

        package_path = compile_class.temp_payload_path


        if self.start_controller_checkbox.value:
            #logger.info("start controller")
            ui.notify("Placeholder starting controller", position="top-right", color="green")
            c = ControllerBase(package_path=package_path)
            c.start_controller()



    @ui.refreshable
    def payload_options(self):
        with ui.row().classes("justify-between w-full"):
            ui.label("Payload Options").classes("text-xl")
            ui.button(icon="refresh", on_click=lambda: self.update_options(self.currently_selected_payload))
        ui.separator()
        with ui.grid().classes("w-full"):
            # Iterate through the payload options dictionary and create inputs for each option
            #logger.info(self.payload_options_dict)
            for key, value in self.payload_options_dict.items():
                #logger.info(key)
                #logger.info(value) #{'description': 'Maximum payload size for Cobalt Strike (512 KB)', 'value': 524288}
                
                description = self.payload_options_dict.get(key).get("description")
                value = self.payload_options_dict.get(key).get("value")

                with ui.column():
                    # with ui.tooltip():
                    #     ui.label(description).classes("text-md")
                    ui.label(key).classes("text-bold")
                    ui.separator()
                    ui.label(description)
                    # tldr this updates the self.payload_options_dict so the correct data gets passed to the controller & payload. self.payload_optiosn_dict re-loads from file on refresh.
                    # maybe add in a reload button specifically for this.
                    # have to use .__setitem__ dunder cuz lambda's can't do dict[key] afaik
                    ui.input(label=key, value=value, on_change=lambda v, k=key: self.payload_options_dict[k].__setitem__("value", v.value)).props("filled square").classes("w-96")


