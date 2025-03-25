from pygwarts.magical.time_turner		import TimeTurner
from operator							import getitem
from ipaddress							import ip_network
from pygwarts.irma.contrib				import LibraryContrib
from pygwarts.filch.linkindor.discovery	import HostDiscovery
from scapy.all							import srp
from scapy.all							import Ether
from scapy.all							import ARP








root	= "/srv/lcontainer/filch"
point	= TimeTurner()








class Filch(HostDiscovery):
	class loggy(LibraryContrib):

		handler		= f"{root}/discovery/{point.Ym_aspath}/gdiscovery{point.dmY_asjoin}.loggy"
		init_name	= "filch"

	def discoverer(self, addr :str, **kwargs) -> str | None :

		R = srp(Ether(dst="ff:ff:ff:ff:ff:ff") /ARP(pdst=addr), **kwargs)
		if len(R) and len(R[0]): return getattr(getattr(getitem(getitem(R,0),0),"answer"),"src")








if	__name__ == "__main__":

	filch = Filch()

	for ip4 in list(ip_network("192.168.160.0/22"))[1:-1]:
		filch(str(ip4), filch.discoverer, retry=0, timeout=1, verbose=0)







