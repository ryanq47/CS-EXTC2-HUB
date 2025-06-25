from nicegui import ui, app


def main():
    print("Running")
    app = ui.run(host="0.0.0.0", port=9000, reload=True, dark=True)

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

        self.payload_options_dict = {
            "someoption1":"",
            "someoption2":"",
            "someoption3":"",
            "someoption4":"",
            "someoption5":"",
            "someoption6":"",
            "someoption7":"",

        }

    def render(self):
        with ui.card().classes('w-full h-full'):
            # Title Card
            with ui.card(align_items="center").classes("w-full no-shadow"):
                ui.label("CS-EXTC2-HUB").classes('text-xl')
                ui.separator()

            # Content Card - maybe dynamic with options, etc
            #ui.label("Something Something Something")

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
        ui.label("Payload Selector").classes("text-xl")
        ui.separator()
        ui.select(label="Payloads", options=["one","two"]).classes("w-96").props("filled square")

        #buttons at bottom
        with ui.row().classes("absolute bottom-8"): # [ ] center + [x] pin to bottom
            ui.button("Generate Payload")
            ui.button("Generate Controller") # mayeb later have a run controller option
            ui.button("Generate All")


    def payload_options(self):
        ui.label("Payload Options").classes("text-xl")
        ui.separator()
        with ui.grid().classes("w-full"):
            # Iterate through the payload options dictionary and create inputs for each option
            for key, value in self.payload_options_dict.items():
                with ui.column():
                    ui.input(label=key, value=value).props("filled square").classes("w-96")