# man-in-the-middle-arp-spoofing
Python code to execute man in the middle attack/ARP spoofing/DoS attack.
1. Set up 3 Virtual Machines: Client, Attacker, and Server.
2. Before running the script, check for connectivity between client and server by using the ping command.
3. Now, on the attacker VM, run the script (python <your_script>.py) and enter the 'Desired Interface', 'Victim IP', and 'Server IP'.
4. Check ping between client and server. Ping should fail.
