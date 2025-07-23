
# How to Add a New Payload to the Platform

This guide explains how to create and integrate a new payload package into the CS-EXTC2-HUB. Following these steps ensures your payload is compatible with the hub's generation, compilation, and management features.

## Directory and File Structure

For the hub to discover and use your payload, you must place it inside the `payloads/` directory. The internal structure of your payload folder is critical.

**Required Source Directory Structure (`payloads/`):**

Your new payload must be in its own folder within the `payloads` directory. The name of this folder becomes the payload's identifier in the UI.


```
CS-EXTC2-HUB
    └──payloads/
        └── your\_payload\_name/
            ├── about.md
            ├── CMakeLists.txt.j2
            ├── config.json
            ├── controller.py.j2
            ├── your_payload_name.c.j2
            └── requirements.txt

````
**Crucial Naming Convention:** 

The C source file **must** be named identically to its parent folder (e.g., a payload in `payloads/icmp_x86/` must have its C source file named `icmp_x86.c.j2`). The compilation script in `src/hub/compile.py` relies on this convention to find the source file.

---

## Required Files Explained

Each file in your payload's directory serves a specific purpose.

### 1. `config.json`
This file drives the UI on the "Generate" page and provides the variables for your templates.

* **Function:** When a user selects your payload, `protocolhub.py` reads this file to dynamically build the options form. The `description` field is used for UI labels, and the `value` field provides the default setting for the input box.
* **Structure:** Each setting must be an object containing `description` and `value` keys.
* **Required Keys:**
    * `payload_name`: The name for the compiled executable. This is used in `CMakeLists.txt.j2`.
    * `cs_teamserver_ip`: The IP of the Cobalt Strike Team Server.
    * `cs_teamserver_port`: The port for the External C2 listener.
    * `pipename`: The named pipe for the beacon connection.

You can add as many keys as you need for your implementation. Just make sure they fit the format. 

* **Example:**
    ```json
    {
      "payload_name": {
        "description": "Package name after compilation. No spaces.",
        "value": "my_tcp_payload"
      },
      "cs_teamserver_ip": {
        "description": "IP Address of the teamserver.",
        "value": "192.168.1.100"
      },
      "cs_teamserver_port": {
        "description": "Port of the teamserver's External C2 listener.",
        "value": 2222
      },
      "pipename": {
        "description": "Named pipe to connect your beacon to.",
        "value": "tcp_pipe"
      },
      "callback_port": {
        "description": "The port the controller will listen on and the client will connect to.",
        "value": 8080
      }
    }
    ```

### 2. `about.md`
This Markdown file provides a description of your payload.

* **Function:** The content of this file is displayed on the left-hand side of the "Generate" page when your payload is selected. It should explain what the payload does, its protocol, and any unique features. The `protocolhub.py` script loads and renders this file in the UI.

### 3. `requirements.txt`
This file lists the Python dependencies for your controller.

* **Function:** This file is for user reference. The hub **does not** automatically install these packages. The user is responsible for installing these dependencies in the environment where the controller will run.

### 4. `<your_payload_name>.c.j2`
This is the source code for your client-side implant. It's a Jinja2 template.

* **Function:** The `compile.py` script processes this file, replacing Jinja2 variables (like `{{ cs_teamserver_ip }}`) with the values provided by the user in the "Generate" UI. The final, rendered C code is then compiled by CMake.
* **Templating Example:**
    ```c
    // Value from config.json is inserted here
    #define SLEEP_TIME {{ sleep_time }}
    ```

### 5. `controller.py.j2`
This is the source code for your server-side controller. It's also a Jinja2 template.

* **Function:** This script acts as the C2 server for your implant. Like the client source, `compile.py` renders this template with user-provided options. The resulting `controller.py` file can be started and stopped from the "Controllers" tab in the UI.
* **Templating Example:**
    ```python
    TEAMSERVER_IP = "{{ cs_teamserver_ip }}"
    TEAMSERVER_PORT = {{ cs_teamserver_port }}
    ```

### 6. `CMakeLists.txt.j2`
This is the build script for CMake.

* **Function:** It instructs CMake how to compile your C client. It is also a Jinja2 template, allowing you to use variables from your `config.json` to define the project name and other build settings.
* **Crucial Correction:** The `add_executable` command must use the C file corresponding to your payload name.
  * **Template Example:**
      ```cmake
      cmake_minimum_required(VERSION 3.15)
      # The project name is pulled from the config.json
      project({{ payload_name }} C)

      # Set compiler for 32-bit Windows
      set(CMAKE_SYSTEM_NAME Windows)
      set(CMAKE_SYSTEM_PROCESSOR x86)
      set(CMAKE_C_COMPILER    i686-w64-mingw32-gcc)
      set(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32)

      set(CMAKE_C_STANDARD 11)
      set(CMAKE_C_STANDARD_REQUIRED ON)
    
      # This MUST match the name of your C source file
      add_executable({{ payload_name }}
          payload.c # This MUST match the .c file in your payload folder. Ex, icmp_x86.c 
      )             #Note, you'll only see a payload.c.j2 in your payload folder, but the payload.c version
                    # will get generated. TLDR: Take the filename of the payload.c.j2, remove .j2, and put that here.
                    # ex, payload.c.j2 (filename) -> payload.c (goes here)
    
      # Link against WinSock2 for networking
      # OPTIONAL - included just in case you're using sockets
      #target_link_libraries({{ payload_name }} PRIVATE
      #    ws2_32
      #)

      # Place the final .exe in the root of the build folder
      get_filename_component(PARENT_DIR "${CMAKE_BINARY_DIR}" PATH)
      set_target_properties({{ payload_name }} PROPERTIES 
          RUNTIME_OUTPUT_DIRECTORY "${PARENT_DIR}"
      )
      ```

---

## The End-to-End Workflow

Understanding the process from generation to execution clarifies how the files work together.


1.  **Generation (Generate Tab)**
    * The UI scans the `payloads/` directory and populates the payload selector.
    * When you select a payload, `protocolhub.py` reads its `config.json` and `about.md` to build the interface.
    * You fill in your desired options and click **Generate Package**.


2.  **Compilation**
    * The `Compile` class in `compile.py` creates a new directory with a unique ID (UUID) inside `packages/`.
    * It copies your source files from `payloads/<your_payload_name>/` into this new UUID directory.
    * It renders the `.j2` templates, injecting your options into the C code, Python controller, and `CMakeLists.txt`.
    * It runs `cmake` to compile your C code into a Windows executable (`.exe`).
    * Finally, it zips the compiled `.exe`, the rendered `controller.py`, and other source files into a package located at `static/packages/<uuid>/<payload_name>.zip`.


3.  **Controller Management (Controllers Tab)**
    * This page, managed by `controllerhub.py`, scans the `packages/` directory to find all generated controllers.
    * It uses a database (`db.py`) and the `psutil` library to check if a controller's process ID (PID) is currently running and displays its status.
    * You can **Start**, **Stop**, and **Delete** controllers from here.
        * **Start**: Executes the `controller.py` script using a subprocess and records its PID in the database.
        * **Stop**: Kills the process by its PID and removes it from the database.
        * **Delete**: Stops the controller (if running), then permanently deletes the entire UUID package directory.


4.  **Deployment (Packages Tab)**
    * This page, managed by `filebrowser.py`, lists the final `.zip` packages from `static/packages/`.
    * You can download your package from here to deploy the client executable to a target.
    * These packages *also* contain everything you need to run the controller in a standalone fashion, rather than having them run from the host. Note, you lose all management options by doing this, and the Controller will not show up in the Web UI.
