from nicegui import ui, app
from pathlib import Path

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
                #ui.link("https://github.com/ryanq47/EXT-C2-HUB")
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
        options = self._get_payload_names()
        ui.label("Payload Selector").classes("text-xl")
        ui.separator()
        selector = ui.select(on_change=lambda x: self.update_options(selector.value), label="Payloads", options=options).classes("w-96").props("filled square")

        #buttons at bottom
        with ui.row().classes("absolute bottom-8"): # [ ] center + [x] pin to bottom
            ui.button("Generate Payload")
            ui.button("Generate Controller") # mayeb later have a run controller option
            ui.button("Generate All")

    def update_options(self, payload_name):
        # get proper options here
        ui.notify("updating options")
        self.payload_options_dict = {
            payload_name:"",
            "someoption8":"",
            "someoption9":"",
            "someoption10":"",
            "someoption11":"",
            "someoption12":"",
            "someoption13":"",

        }
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

    @ui.refreshable
    def payload_options(self):
        ui.label("Payload Options").classes("text-xl")
        ui.separator()
        with ui.grid().classes("w-full"):
            # Iterate through the payload options dictionary and create inputs for each option
            for key, value in self.payload_options_dict.items():
                with ui.column():
                    ui.input(label=key, value=value).props("filled square").classes("w-96")