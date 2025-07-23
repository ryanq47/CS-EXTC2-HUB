# CS-EXTC2-HUB

A WebGui Management tool for CS-EXTC2-* (Cobalt Strike External C2) Protocols. Simplifies the compilation & running of controllers, and payloads. 

Current Implemented Protocols:
 - [CS-EXTC2-ICMP (x86)](https://github.com/ryanq47/CS-EXTC2-ICMP)


If you run into any bugs, PLEASE submit an issue!

NOTE!!! This tool can only be run on linux operating systems, due to the compilation feature. 

---

# Features:
 - Few Click compilation of Payloads

 - Hosted Controllers
   - A controller is generated for each payload, run controller with one click. 

 - Payload & Controller management: 
   - Controllers: Configure, Start, Stop, Create, Delete, Stats 
   - Payloads: Configure, Compile, Download, Delete
 - Extensibility: 
   - Add your own (existing or new) EXT-C2 Clients & Controllers


# Images:

#### Generate A Package
<img width="1621" height="1094" alt="image" src="https://github.com/user-attachments/assets/02133d8a-aa51-41f5-a522-cb91c14ceb87" />

#### Generated Packages

<img width="1617" height="1101" alt="image" src="https://github.com/user-attachments/assets/41ba9f34-3754-43e4-b0c0-4878c6de4238" />

#### Package Contents:

<img width="1121" height="367" alt="image" src="https://github.com/user-attachments/assets/ff8510a6-f93d-4476-9099-55b1ccbc36db" />

#### Controllers & Controller Stats:
<img width="1610" height="575" alt="image" src="https://github.com/user-attachments/assets/7d44fe87-51aa-4e77-a13d-de4f42fae738" />

<img width="1614" height="1096" alt="image" src="https://github.com/user-attachments/assets/667a0fe7-a0c8-4f77-a0b6-b3821af6e985" />


# Setup:

1. **Install dependencies:**

    Note, you may need a `venv` here. 

   ```bash
   pip install -r requirements.txt
   ```

   You'll also need `cmake` and `mingw`
   ```bash
   sudo apt-get install gcc-mingw-w64 cmake
   ```


3. **Start the tool**

   ```bash
   python3 main.py
   ```

4. **Navigate to the WebPage**

   URL: `http://<your_ip>:9000`

   The `EXTC2-HUB` tab will guide you with further setup for the External C2 Bridge.


# Adding your own EXT-C2 setups:

You can (somewhat) easily integrate your existing External C2 payloads into this hub. The process is designed to be non-destructive and **will not break your code's core logic**. The required format acts as a simple wrapper around your existing client and controller. (provided the controller is written in python)

To make your payload compatible, you'll need to make minor adjustments. This primarily involves replacing hardcoded configuration values—such as IP addresses, ports, or sleep times—with template variables like `{{ cs_teamserver_ip }}`. This is the key step that allows your payload to be configured through the platform's web interface.

For a complete guide on the required file structure and how to add these template variables, please refer to the **`Adding Your Own Payloads.md`** documentation.

Again, please create an issue if you have any bugs, or questions!
