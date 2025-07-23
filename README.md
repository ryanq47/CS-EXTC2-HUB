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


# Images:

#### Generate A Package
<img width="1621" height="1094" alt="image" src="https://github.com/user-attachments/assets/02133d8a-aa51-41f5-a522-cb91c14ceb87" />

#### Generated Packages

<img width="1617" height="1101" alt="image" src="https://github.com/user-attachments/assets/41ba9f34-3754-43e4-b0c0-4878c6de4238" />

#### Package Contents:

<img width="1121" height="367" alt="image" src="https://github.com/user-attachments/assets/ff8510a6-f93d-4476-9099-55b1ccbc36db" />

#### Controllers:
<img width="1610" height="575" alt="image" src="https://github.com/user-attachments/assets/7d44fe87-51aa-4e77-a13d-de4f42fae738" />

<img width="1614" height="1096" alt="image" src="https://github.com/user-attachments/assets/667a0fe7-a0c8-4f77-a0b6-b3821af6e985" />


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
