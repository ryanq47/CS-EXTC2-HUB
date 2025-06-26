from nicegui import ui, app
from pathlib import Path
import json
import subprocess 

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
            ui.button("Generate Payload")#.classes('flex-1 p-0')
            ui.button("Generate Controller")#.classes('flex-1 p-0') # mayeb later have a run controller option
            ui.button("Generate All", on_click=lambda:Compile(payload_name=self.currently_selected_payload, payload_options_dict=self.payload_options_dict).run())#.classes('flex-1 p-0')

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
            #print(config_options.read())
            return json.loads(config_options.read())

    @ui.refreshable
    def payload_options(self):
        ui.label("Payload Options - Refresh to reset").classes("text-xl")
        ui.separator()
        with ui.grid().classes("w-full"):
            # Iterate through the payload options dictionary and create inputs for each option
            #print(self.payload_options_dict)
            for key, value in self.payload_options_dict.items():
                #print(key)
                #print(value) #{'description': 'Maximum payload size for Cobalt Strike (512 KB)', 'value': 524288}
                
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


import uuid
import shutil
from jinja2 import Template
class Compile:
    '''
    
    Compile stuff

    WARNING: file with c payload in it MUST be same name as parent folder.

    Ex: 
        icmp_x86/
        and
        icmp_x86.c
    
    '''
    def __init__(self, payload_name, payload_options_dict):
        self.payload_path = Path("payloads") / payload_name
        self.payload_name = payload_name
        self.uuid = uuid.uuid4()
        self.temp_payload_path = Path("temp") / str(self.uuid)
        self.payload_options_dict = payload_options_dict
        # create temp dir
        self.temp_payload_path.mkdir(parents=True, exist_ok=True)

    def run(self):
        '''
        Runs things
        '''
        self.setup()
        self.compile()


    def setup(self):
        '''
        Sets up the compile env
        '''

        # get files from payload template path
        for file in self.payload_path.iterdir():
            print(file)
            if file.is_file():
                # copy into new temp path
                shutil.copy2(file, self.temp_payload_path / file.name)

        # do template magic with jinjna
        self.render_payload_template()
        self.render_controller_template()

    # note- with the render, could move to one func that scans each file, 
    # then replaces the content, but for now it's simpler to do one render per 
    # file that needs it
    def render_payload_template(self):
        # open template file
        temp_payload_source = self.temp_payload_path / f"{self.payload_name}.c.j2"
        with open(temp_payload_source) as f:
            payload_file = f.read()
        
        template = Template(payload_file)
        # final_payload = template.render(
        #     #options here
        #     test="TESTSUCCESSFUL"
        # )

        # create new dict where it's a 1 to 1 mapping between `key : value``,
        #intead of `key: {desc:... value:...}`. This allows for proper unpacking
        # for the template render
        mapped_dict = {}
        for key, subdict in self.payload_options_dict.items():
            mapped_dict[key] = subdict.get("value")

        final_payload = template.render(
            # unpack dict into keyword args to keep templating dynamic
            **mapped_dict
        )

        # save file as .c
        out_path = Path(self.temp_payload_path / f"{self.payload_name}.c")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_payload)

    def render_controller_template(self):
        # open template file
        temp_payload_source = self.temp_payload_path / "controller.py.j2"
        with open(temp_payload_source) as f:
            payload_file = f.read()
        
        template = Template(payload_file)
        # final_payload = template.render(
        #     #options here
        #     test="TESTSUCCESSFUL"
        # )

        # create new dict where it's a 1 to 1 mapping between `key : value``,
        #intead of `key: {desc:... value:...}`. This allows for proper unpacking
        # for the template render
        mapped_dict = {}
        for key, subdict in self.payload_options_dict.items():
            mapped_dict[key] = subdict.get("value")

        final_payload = template.render(
            # unpack dict into keyword args to keep templating dynamic
            **mapped_dict
        )

        # save file as .py
        out_path = Path(self.temp_payload_path / "controller.py")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_payload)

    def compile(self):
        # create build dir
        (Path(self.temp_payload_path) / "build").mkdir(exist_ok=True)
        temp_build_path = Path(self.temp_payload_path) / "build"
        #ui.notification(temp_build_path)

        ui.notification(f"Starting build for {self.payload_name}", position="top-right", color="green")

        cmake_config = subprocess.run(
            ["cmake", "-S", self.temp_payload_path, "-B", temp_build_path],
            capture_output=True,
            text=True,
            check=True,
        )
        print(cmake_config)

        cmake_build = subprocess.run(
            ["cmake", "--build", temp_build_path],
            capture_output=True,
            text=True,
            check=True,
        )
        print(cmake_build)
