# CS-EXTC2-HUB

A WebGui Management tool for CS-EXTC2-* Protocols. Simplifies the compilation & running of controllers, and payloads. 

Current Implemented Protocols:
 - [CS-EXTC2-ICMP (x86)](https://github.com/ryanq47/CS-EXTC2-HUB)


---

# Features:
 - Few Click compilation of Payloads

 - Hosted Controllers
   - A controller is generated for each payload, run controller with one click. 

 - Payload & Controller management: 
   - Controllers: Configure, Start, Stop, Create, Delete, Stats 
   - Payloads: Configure, Compile, Download, Delete


# Setup:

1. **Install dependencies:**

    Note, you may need a `venv` here. 

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the tool**

   ```bash
   python3 main.py
   ```

3. **Navigate to the WebPage**

   URL: `http://<your_ip>:9000`
