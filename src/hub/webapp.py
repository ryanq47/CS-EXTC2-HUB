from nicegui import ui, app
from pathlib import Path
from src.hub.protocolhub import ProtocolHub, FileBrowser
from src.hub.connectorhub import ConnectorBrowser

def main():
    #Add static files & make sure it exists
    print("Serving static dir")
    # make needed directories BEFORE everything else gets called, otherwise path not found/dir not exist errors may happen
    Path("static").mkdir(parents=True, exist_ok=True)
    Path("static/packages").mkdir(parents=True, exist_ok=True)
    #Path("static/packages").mkdir(parents=True, exist_ok=True)
    app.add_static_files('/static', 'static')

    print("Running")
    ui.run(host="0.0.0.0", port=9000, reload=False, dark=True)

@ui.page('/')
def index():
    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        # p = ProtocolHub()
        # p.render()

        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Connectors')
            two = ui.tab('CS-EXTC2-HUB')
            three = ui.tab('Generate Package')
            four = ui.tab('Files')

        ui.separator()

        with ui.tab_panels(tabs, value=two).classes('w-full'):
            with ui.tab_panel(one):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    c = ConnectorBrowser()
                    c.render()
                
            with ui.tab_panel(two):
                #ui.label("CS-EXTC2-HUB")
                ui.label("Main Page")
                ui.label("explanation of extc2 here?")

            with ui.tab_panel(three):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    p = ProtocolHub()
                    p.render()

            with ui.tab_panel(four):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    fb = FileBrowser("static/packages")
                    fb.render()



