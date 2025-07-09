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
                "value": "blank",
                "description": "blank"
            }
        }
        self.currently_selected_payload = None
        self.option_inputs = {}  # to track input fields
        self.option_container = None  # container for payload options

        # Hold a reference to the markdown UI element
        self.about_markdown = None

    # @ui.refreshable
    def render(self):
        with ui.card().classes('w-full h-full'):
            with ui.splitter(limits=[50, 50]).classes("w-full h-full") as splitter:
                with splitter.before:
                    # p-4 for padding cuz w-full wipes padding
                    with ui.column().classes("w-full h-full p-4"):
                        self.left_column()
                    # ui.label("left")
                with splitter.after:
                    with ui.scroll_area().classes("h-full"):
                        self.option_container = ui.column().classes("h-full p-4")
                        self.payload_options()

    def left_column(self):
        # with ui.element().classes('p-4 w-full h-full'):
        options = self._get_payload_names()
        ui.label("Payload Selector").classes("text-xl")
        ui.separator()
        selector = ui.select(value="icmp_x86", on_change=lambda x: self.update_options(selector.value),
                             label="Payloads", options=options).classes("w-96").props("filled square")

        with ui.scroll_area().classes("h-3/5"):
            # Create the markdown element and store our reference to it.
            self.about_markdown = ui.markdown()

        # buttons at bottom
        with ui.row().classes("absolute bottom-8 justify-center space-x-4"):  # [ ] center + [x] pin to bottom
            # ui.button("Generate Payload")#.classes('flex-1 p-0')
            # ui.button("Generate Controller")#.classes('flex-1 p-0') # mayeb later have a run controller option
            ui.button("Generate Package", on_click=lambda: self._on_click_generate_action())  # .classes('flex-1 p-0')

            self.start_controller_checkbox = ui.checkbox("Start Controller", value=False)
            with self.start_controller_checkbox:
                ui.tooltip("Automatically start a controller on this host, for this package on generation")

        # update options at first load
        self.update_options(selector.value)

    def update_options(self, payload_name):
        self.currently_selected_payload = payload_name

        # get proper options here
        new_about_text = self._get_payload_about()
        if self.about_markdown:
            self.about_markdown.set_content(new_about_text)

        self.payload_options_dict = self._get_payload_options()

        # self.payload_options.refresh()
        self.payload_options()

    def _get_payload_names(self) -> list:
        '''
        Return list of payloads
        '''
        p = Path("payloads")
        list_of_payloads = []
        for payload_name in p.iterdir():
            if payload_name.is_dir():
                # comes out to 'payloads/<NAME>, need to strip payloads/
                list_of_payloads.append(str(payload_name).replace('payloads/', ''))
        return list_of_payloads

    def _get_payload_options(self) -> dict:
        config_file = Path("payloads") / self.currently_selected_payload / "config.json"

        # ui.notification(config_file)

        with open(config_file, "r") as config_options:
            # logger.info(config_options.read())
            return json.load(config_options)

    def _get_payload_about(self) -> str:
        '''
        Reads about.md from payload

        '''
        if not self.currently_selected_payload:
            return ""

        about_file = Path("payloads") / self.currently_selected_payload / "about.md"

        with open(about_file, "r") as about:
            # logger.info(config_options.read())
            return about.read()

    def _on_click_generate_action(self):
        '''
        Called when the "generate" option is selected

        '''
        # start comp:
        compile_class = Compile(payload_name=self.currently_selected_payload,
                                payload_options_dict=self.payload_options_dict)
        compile_class.run()

        package_path = compile_class.temp_payload_path

        if self.start_controller_checkbox.value:
            # logger.info("start controller")
            ui.notify("Placeholder starting controller", position="top-right", color="green")
            c = ControllerBase(package_path=package_path)
            c.start_controller()

    def payload_options(self):
        if not self.option_container:
            return

        self.option_container.clear()
        self.option_inputs = {}

        with self.option_container:
            with ui.row().classes("justify-between w-full"):
                ui.label("Payload Options").classes("text-xl")
                # reloads the original options from the json file
                ui.button(icon="refresh", on_click=lambda: self.update_options(self.currently_selected_payload))

            ui.separator()

            with ui.grid().classes("w-full"):
                for key, value in self.payload_options_dict.items():
                    description = value.get("description", "")
                    val = value.get("value", "")

                    with ui.column():
                        ui.label(key).classes("text-bold")
                        ui.separator()
                        ui.label(description)
                        input_field = ui.input(
                            label=key,
                            value=val,
                            on_change=lambda v, k=key: self.payload_options_dict[k].__setitem__("value", v.value)
                        ).props("filled square").classes("w-96")

                        self.option_inputs[key] = input_field

