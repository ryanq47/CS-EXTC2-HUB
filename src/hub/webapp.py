from nicegui import ui, app
from src.hub.protocolhub import ProtocolHub

def main():
    print("Running")
    app = ui.run(host="0.0.0.0", port=9000, reload=True, dark=True)

@ui.page('/')
def index():
    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        # p = ProtocolHub()
        # p.render()

        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('Connectors')
            two = ui.tab('CS-EXTC2-HUB')
            three = ui.tab('Payloads')

        ui.separator()

        with ui.tab_panels(tabs, value=two).classes('w-full'):
            with ui.tab_panel(one):
                ui.label("Connectors")
                ui.label("SomeConnector - Status - IP - start | stop, etc, etc")

            with ui.tab_panel(two):
                #ui.label("CS-EXTC2-HUB")
                ui.label("Main Page")
                ui.label("explanation of extc2 here?")

            with ui.tab_panel(three):
                with ui.column().classes("w-full h-screen overflow-hidden"):
                    p = ProtocolHub()
                    p.render()




