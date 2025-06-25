from nicegui import ui, app
from src.hub.protocolhub import ProtocolHub

def main():
    print("Running")
    app = ui.run(host="0.0.0.0", port=9000, reload=True, dark=True)

@ui.page('/')
def index():
    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        p = ProtocolHub()
        p.render()

