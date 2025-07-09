import datetime
from pathlib import Path
from nicegui import ui
import shutil
import structlog

logger = structlog.get_logger(__name__)

class FileBrowser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.list_of_files = []

    @ui.refreshable
    def render(self):
        self._get_files()
        logger.info(self.list_of_files)
        self.render_files_table()

    def render_files_table(self):
        with ui.card(align_items="center").classes("w-full p-4 h-8 no-shadow  absolute bottom-8"):
            ui.label(
                "FYI: Deleting a package here WILL NOT delete the associated controller for said package. This is to avoid accidently stopping a running controller.").classes(
                "italic")
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
                file_path = Path("static") / "packages" / file_path
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
                        ui.button('Delete', on_click=lambda folder=file_path.parent: self._delete_folder(folder)).props(
                            "color=red")
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

