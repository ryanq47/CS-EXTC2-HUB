from nicegui import ui, app
from pathlib import Path
import json
import subprocess 
from src.hub.controllerhub import ControllerBase
import logging

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

    @ui.refreshable
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
            #logging.info(config_options.read())
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
            #logging.info("start controller")
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
            #logging.info(self.payload_options_dict)
            for key, value in self.payload_options_dict.items():
                #logging.info(key)
                #logging.info(value) #{'description': 'Maximum payload size for Cobalt Strike (512 KB)', 'value': 524288}
                
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

import datetime
class FileBrowser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.list_of_files = []

    @ui.refreshable
    def render(self):
        self._get_files()
        logging.info(self.list_of_files)
        self.render_files_table()

    
    def render_files_table(self):
        with ui.row().classes("w-full justify-between p-4"):
            ui.label("File Name")
            ui.label("File Path")
            ui.label("Time Stamp")
            ui.button(icon="refresh", on_click=lambda: self.render.refresh())
            ui.separator()

        with ui.scroll_area().classes("w-full h-full"):
            for file_path in self.list_of_files:
                # get web path
                web_path = f"static/packages/{file_path}"

                # get timestamp
                file_path = Path("static") / "packages"/ file_path
                stat = file_path.stat()

                # Access timestamps
                created = datetime.datetime.fromtimestamp(stat.st_ctime)

                # render row
                with ui.row().classes("w-full h-16 justify-between items-center"):
                    ui.label(file_path.name)
                    ui.label(str(file_path))
                    ui.label(created)
                    # Fix: capture current value as default argument
                    with ui.row():
                        ui.button('Delete', on_click=lambda folder=file_path.parent: self._delete_folder(folder)).props("color=red")
                        ui.button('Download', on_click=lambda wp=web_path: ui.download.from_url(wp))
                    ui.separator()

    
    def _delete_folder(self, folder_path):
        folder = Path(folder_path)
        if folder.exists() and folder.is_dir():
            shutil.rmtree(folder)

        self.render.refresh()

    def _get_files(self):
        '''
        Recursively gets list of files under static/packages
        '''
        base_path = Path("static/packages")
        self.list_of_files = []  # Ensure it's reset

        for file_path in base_path.rglob('*'):
            if file_path.is_file():
                # Store relative path from 'static/packages'
                relative_path = file_path.relative_to(base_path)
                self.list_of_files.append(str(relative_path))

        return self.list_of_files
    

import uuid
import shutil
from jinja2 import Template
import zipfile

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
        try:
            self.setup()
            self.compile()

            # get files & zip
            processed_files = self.get_filtered_files(self.temp_payload_path)
            # create path for output zip file
            user_entered_payload_name = self.payload_options_dict.get("payload_name").get("value", "default_payload_name")
            output_file_path = Path("static") / "packages" / str(self.uuid) / f"{user_entered_payload_name}.zip"
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            output_file_path.touch(exist_ok=True)
            self.zip_files(processed_files, output_file_path)



        except Exception as e:
            logging.info(e)
            ui.notify(e)

    def setup(self):
        '''
        Sets up the compile env
        '''

        # copy data back to json

        # get files from payload template path
        for file in self.payload_path.iterdir():
            logging.info(file)
            if file.is_file():
                # copy into new temp path
                shutil.copy2(file, self.temp_payload_path / file.name)

        # do template magic with jinjna
        self.render_payload_template()
        self.render_controller_template()
        self.render_cmake_template()

        # update config file with needed values
        self.update_config_file()

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

    def render_cmake_template(self):
        # open template file
        temp_payload_source = self.temp_payload_path / "CMakeLists.txt.j2"
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
        out_path = Path(self.temp_payload_path / "CMakeLists.txt")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_payload)

    def update_config_file(self):
        '''
        Updates config file to use the self.payload_options_dict to fill values in and save it
        
        The config file is NOT used for jijna templating, instead its used for everything else to 
        reference what said config is. 
        '''
        config_path = self.temp_payload_path / "config.json"
        if config_path.exists() and config_path.is_file():
            config_path.unlink()  # Deletes the file

        with open(config_path, 'w') as json_file:
            json.dump(self.payload_options_dict, json_file, indent=4)  
            logging.info(f"Data written to {config_path}")

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
        logging.info(cmake_config)

        cmake_build = subprocess.run(
            ["cmake", "--build", temp_build_path],
            capture_output=True,
            text=True,
            check=True,
        )
        logging.info(cmake_build)


    def zip_files(self, file_paths, output_zip_path):
        """
        Create a zip file from a list of file paths using pathlib.

        Args:
            file_paths (list of str or Path): List of file paths to include in the zip.
            output_zip_path (str or Path): Output zip file path.
        """
        logging.info(f"Zipping files: {file_paths}")
        output_zip_path = Path(output_zip_path)

        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                file_path = Path(file_path)
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)
                else:
                    logging.info(f"Warning: {file_path} does not exist or is not a file.")

    def get_filtered_files(self, directory, extensions=('.exe', '.py', '.dll'), recursive=False):
        """
        Get all files in the directory with specific extensions.

        Args:
            directory (str or Path): The directory to search in.
            extensions (tuple): File extensions to include (e.g. ('.py', '.exe')).
            recursive (bool): Whether to search recursively.

        Returns:
            List[Path]: List of matching file paths.
        """
        logging.info(directory)
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")

        if recursive:
            files = [f for f in directory.rglob('*') if f.suffix.lower() in extensions and f.is_file()]
        else:
            files = [f for f in directory.glob('*') if f.suffix.lower() in extensions and f.is_file()]

        logging.info(files)
        return files