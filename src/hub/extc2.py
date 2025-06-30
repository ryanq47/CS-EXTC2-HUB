from nicegui import ui, app

class ExtC2Overview:
    def __init__(self):
        ...


    def render(self):
        #align_items="center"
        with ui.card(align_items="center").classes("w-full h-full"):
            with ui.scroll_area().classes("w-full h-full no-shadow"):

                ui.label("CS External C2...")

                #ui.label("imagehere")
                with ui.column().classes("w-full p-0 justify-center items-center"):
                    ui.image("static/pics/extc2.png").props("fit=scale-down").classes("w-[300px]")

                ui.label("Some Desc Blah Blah This tool makes the controllers & the clients")

                #################################
                # Definitions
                #################################
                ui.label("Definitions: ").classes("text-xl")
                ui.separator()
                ui.markdown('**Package**: Consists of a Third-Party-Controller (in python), and a Third-Party-Client, in c. Navigate to "GENERATE PACKAGE" to generate a package.')


                #################################
                # Setup
                #################################
                ui.label("Setup (Cobalt Strike Side): ").classes("text-xl")
                ui.separator()
                ui.label("Setup guide here")

                ui.label("Maybe caroseul this whole thing?")
                # with ui.column().classes("w-full p-0 justify-center items-center"):
                #     ui.label("1. Start an External C2 Listener in Cobalt Strike")
                #     ui.image("static/pics/create_listener.png").props("fit=scale-down").classes("w-[500px]")#.classes("w-96") #.props("fit=scale-down")
                #     ui.label("2. Once it's started, you're good to go on the CS side.")
                #     ui.image("static/pics/started_listener.png").props("fit=scale-down").classes("w-[500px]")#.classes("w-96")#

                #     ui.label("3. Go to the Generate Package tab, fill in values for the package & hit generate. Click 'start controller' to automatically start a controller with the specified settings")


                #     ui.label("4. Unzip downloaded package, and deploy .EXE to target. EXE should download the payload, and execute it.")

                with ui.carousel(animated=True, arrows=True, navigation=True).props('height=550px').classes("w-full"):
                    with ui.carousel_slide().classes('p-4 items-center justify-center'):
                        ui.label("1. Start an External C2 Listener in Cobalt Strike")
                        ui.image("static/pics/create_listener.png").props("fit=scale-down").classes("w-[500px]")

                    with ui.carousel_slide().classes('p-4 items-center justify-center'):
                        ui.label("2. Once it's started, you're good to go on the CS side.")
                        ui.image("static/pics/started_listener.png").props("fit=scale-down").classes("w-[1500]")

                    with ui.carousel_slide().classes('p-4 items-center justify-center'):
                        ui.label("3. Go to the Generate Package tab, fill in values for the package & hit generate. Click 'start controller' to automatically start a controller with the specified settings")
                        ui.image("static/pics/generate_package.png").props("fit=scale-down").classes("w-[700px]")

                    with ui.carousel_slide().classes('p-4 items-center justify-center'):
                        ui.markdown("4. Make *sure* the controller is running, either via the CONTROLLERS tab, or running locally on some machine. The controllers need to be up before executing the payload.")
                        ui.image("static/pics/running_controller.png").props("fit=scale-down").classes("w-[1500px]")

                    with ui.carousel_slide().classes('p-4 items-center justify-center'):
                        ui.label("5. Unzip downloaded package from the PACKAGES tab, and deploy .EXE to target. EXE should download the payload, and execute it.")
                        ui.image("static/pics/screenshot_payload.png").props("fit=scale-down").classes("w-[700px]")
                        

                # with ui.carousel(animated=True, arrows=True, navigation=True).classes("w-full h-full"):#.props('height=180px'):
                #     with ui.carousel_slide():#.classes('p-0 h-24'):
                #         ui.image("static/pics/create_listener.png").props("fit=scale-down")
                #     with ui.carousel_slide():#.classes('p-0 h-24'):
                #         ui.image("static/pics/started_listener.png").props("fit=scale-down")


                #################################
                # Ext Resources
                #################################
                ui.label("Resources: ").classes("text-xl")
                ui.separator()

                with ui.row():
                    ui.link("ExtC2 Page:", target="https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/listener-infrastructure_external-c2.htm", new_tab=True)
                    ui.label("Official External C2 Documentation from Fortra")

                with ui.row():
                    ui.link("ExtC2 Spec:", target="https://hstechdocs.helpsystems.com/kbfiles/cobaltstrike/attachments/externalc2spec.pdf", new_tab=True)
                    ui.label("Official External C2 Spec")
