from nicegui import ui, app


def main():
    print("Running")
    app = ui.run(host="0.0.0.0", port=9000, reload=True)

@ui.page('/')
def index():
    # overflow-hidden allows it to go full wide
    with ui.column().classes("w-full h-screen overflow-hidden"):
        p = ProtocolHub()
        p.render()

# move to file
# from nicegui import ui, app
class ProtocolHub:
    def __init__(self):
        pass

    def render(self):
        with ui.card().classes('w-full h-full'):
            # Title Card
            with ui.card(align_items="center").classes("w-full no-shadow"):
                ui.label("CS-EXTC2-HUB").classes('text-xl')
                ui.separator()

            # Content Card - maybe dynamic with options, etc
            ui.label("Something Something Something")

            with ui.splitter().classes("w-full h-full") as splitter:
                with splitter.before:
                    with ui.scroll_area():
                        self.selector()
                        #ui.label("left")
                with splitter.after:
                    with ui.scroll_area():
                        ui.label("right")
                        ui.label("options go here")
                #self.selector()



    def selector(self):
        #ui.label("Choose a whatever")
        #ui.separator()
        ui.select(label="Project", options=["one","two"]).classes("w-full")