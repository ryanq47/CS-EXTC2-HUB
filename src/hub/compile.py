import uuid
import shutil
from jinja2 import Template
import zipfile
from pathlib import Path
import structlog
from nicegui import ui
import json
import subprocess

logger = structlog.get_logger(__name__)

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
        self.temp_payload_path = Path("packages") / str(self.uuid)
        self.payload_options_dict = payload_options_dict
        # create packages dir
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
            user_entered_payload_name = self.payload_options_dict.get("payload_name").get("value",
                                                                                          "default_payload_name")
            output_file_path = Path("static") / "packages" / str(self.uuid) / f"{user_entered_payload_name}.zip"
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            output_file_path.touch(exist_ok=True)
            self.zip_files(processed_files, output_file_path)



        except Exception as e:
            logger.info(e)
            ui.notify(e)

    def setup(self):
        '''
        Sets up the compile env
        '''

        # copy data back to json

        # get files from payload template path
        for file in self.payload_path.iterdir():
            logger.info(file)
            if file.is_file():
                # copy into new packages path
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
        # intead of `key: {desc:... value:...}`. This allows for proper unpacking
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
        # intead of `key: {desc:... value:...}`. This allows for proper unpacking
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
        # intead of `key: {desc:... value:...}`. This allows for proper unpacking
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
            logger.info(f"Data written to {config_path}")

    def compile(self):
        # create build dir
        (Path(self.temp_payload_path) / "build").mkdir(exist_ok=True)
        temp_build_path = Path(self.temp_payload_path) / "build"
        # ui.notification(temp_build_path)

        ui.notification(f"Starting build for {self.payload_name}", position="top-right", color="green")

        cmake_config = subprocess.run(
            ["cmake", "-S", self.temp_payload_path, "-B", temp_build_path],
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info(cmake_config)

        cmake_build = subprocess.run(
            ["cmake", "--build", temp_build_path],
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info(cmake_build)

    def zip_files(self, file_paths, output_zip_path):
        """
        Create a zip file from a list of file paths using pathlib.

        Args:
            file_paths (list of str or Path): List of file paths to include in the zip.
            output_zip_path (str or Path): Output zip file path.
        """
        logger.info(f"Zipping files: {file_paths}")
        output_zip_path = Path(output_zip_path)

        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                file_path = Path(file_path)
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)
                else:
                    logger.info(f"Warning: {file_path} does not exist or is not a file.")

    def get_filtered_files(self, directory, extensions=('.exe', '.py', '.dll', '.c', '.h', '.md', '.txt'), recursive=False):
        """
        Get all files in the directory with specific extensions.

        Args:
            directory (str or Path): The directory to search in.
            extensions (tuple): File extensions to include (e.g. ('.py', '.exe')).
            recursive (bool): Whether to search recursively.

        Returns:
            List[Path]: List of matching file paths.

        Purpose for each extension
            .txt: CMakeLists.txt
            .md: about.md
            .c/.h: sourcewhatever.c/.h
            .py: controller.py
            .exe: compiled payload
        """
        logger.info(directory)
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a valid directory")

        if recursive:
            files = [f for f in directory.rglob('*') if f.suffix.lower() in extensions and f.is_file()]
        else:
            files = [f for f in directory.glob('*') if f.suffix.lower() in extensions and f.is_file()]

        logger.info(files)
        return files