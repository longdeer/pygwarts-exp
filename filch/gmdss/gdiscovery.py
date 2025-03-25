from operator							import getitem
from ipaddress							import ip_network
from pygwarts.irma.contrib				import LibraryContrib
from pygwarts.filch.linkindor.discovery	import HostDiscovery
from scapy.all							import srp
from scapy.all							import Ether
from scapy.all							import ARP








class Filch(HostDiscovery):
	class loggy(LibraryContrib):

		handler		= "file handler path (optional)"
		init_name	= "filch"

	def discoverer(self, addr :str, **kwargs) -> str | None :

		""" scapy ARP request builder """

		R = srp(Ether(dst="ff:ff:ff:ff:ff:ff") /ARP(pdst=addr), **kwargs)
		if len(R) and len(R[0]): return getattr(getattr(getitem(getitem(R,0),0),"answer"),"src")








filch = Filch()


# scan typical network without 0.0 and 255.255 addresses
# no verbose output, no retries, 1 sec timeout
for ip4 in list(ip_network("192.168.0.0/24"))[1:-1]:
	filch(str(ip4), filch.discoverer, retry=0, timeout=1, verbose=0)







