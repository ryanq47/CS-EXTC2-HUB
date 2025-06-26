import datetime
from pathlib import Path
from nicegui import ui, app
from src.hub.db import Base, add_or_update_agent

# add_or_update_agent(
#     uuid_str="123e4567-e89b-12d3-a456-426614174000",
#     name="Agent007",
#     ip="192.168.1.100",
#     port=8080,
#     status="active",
#     teamserver_ip="10.0.0.2",
#     teamserver_port=4444
# )
#delete_agent(uuid)


class ConnectorBrowser:
    def __init__(self):
        ...
    @ui.refreshable
    def render(self):
        self.render_connector_table()
        #print(self.list_of_files)
        #self.render_files_table()

    
    def render_connector_table(self):
        with ui.row().classes("w-full justify-between p-4"):
            ui.label("Connector Name")
            # ui.label("File Path")
            # ui.label("Time Stamp")
            ui.button(icon="refresh")
            ui.separator()

        with ui.scroll_area().classes("w-full h-full"):
            for i in range(1,5):
                # # get web path
                # web_path = f"static/packages/{file_path}"

                # # get timestamp
                # file_path = Path("static") / "packages"/ file_path
                # stat = file_path.stat()

                # # Access timestamps
                # created = datetime.datetime.fromtimestamp(stat.st_ctime)

                # # render row
                # with ui.row().classes("w-full h-16 justify-between items-center"):
                #     ui.label(file_path.name)
                #     ui.label(str(file_path))
                #     ui.label(created)
                #     # Fix: capture current value as default argument
                #     with ui.row():
                #         ui.button('Delete', on_click=lambda folder=file_path.parent: self._delete_folder(folder)).props("color=red")
                #         ui.button('Download', on_click=lambda wp=web_path: ui.download.from_url(wp))
                #     ui.separator()

                with ui.row().classes("w-full h-16 justify-between items-center"):
                    ui.label("connector_name")
                    #ui.label(str(file_path))
                    #ui.label(created)
                    # Fix: capture current value as default argument
                    with ui.row():
                        ui.button('Stop').props("color=red")
                        ui.button('Start')
                    ui.separator()

    