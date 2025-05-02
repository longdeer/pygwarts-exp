from pygwarts.magical.time_turner		import TimeTurner
from operator							import getitem
from ipaddress							import ip_network
from pygwarts.irma.contrib				import LibraryContrib
from pygwarts.filch.marauders_map		import MaraudersMap
from pygwarts.filch.linkindor			import EUI48_format
from pygwarts.filch.linkindor.arp		import ARPDiscovery
from pygwarts.filch.linkindor.arp		import ARPResponseInspector
from irma_local							import TelegramTechHoist
from scapy.all							import srp
from scapy.all							import Ether
from scapy.all							import ARP








root	= "/srv/lcontainer/filch"
point	= TimeTurner()








class Discoverywatch(ARPDiscovery):

	@TelegramTechHoist
	class loggy(LibraryContrib):

		handler		= f"{root}/discovery/{point.Ym_aspath}/discovery{point.dmY_asjoin}.loggy"
		init_name	= "filch"
		watchdog	= "Discoverywatch.Inspector",

	class filchmap(MaraudersMap): pass
	class Inspector(ARPResponseInspector):

		def __call__(self, ip4 :str, mac :str):

			if	(result := super().__call__(ip4, mac)) is not None:

				state			= result["state"]
				srcip			= result["source ip4"] 
				srcmac			= result["source MAC"]
				mapped_name		= result["source ip4 to name"]
				maced_name		= result["source MAC to name"]

				match state:

					case 63:	return

					case 199:	self.loggy.info(f"unknown {srcmac} responded from {mapped_name} ip4")
					case 216:	self.loggy.info(f"{maced_name} responded from unknown {srcip}")
					case 223:	self.loggy.info(f"{maced_name} responded from {mapped_name} ip4")
					case 224:	self.loggy.info(f"unknown {srcmac} responded from unknown {srcip}")

					case _:		self.loggy.info(f"{srcip} response unknown state {state}")


	def discoverer(self, addr :str, **kwargs) -> str | None :

		R = srp(Ether(dst="ff:ff:ff:ff:ff:ff") /ARP(pdst=addr), **kwargs)

		if len(R) and len(R[0]):

			respone_mac = EUI48_format(getattr(getattr(getitem(getitem(R,0),0),"answer"),"src"))
			self.Inspector(addr, respone_mac)

			return respone_mac








if	__name__ == "__main__":

	filch = Discoverywatch()
	filch.filchmap.CSV(

			f"{root}/discoverymap.csv",
			";",
			IP4=0,
			MAC=1,
			NAME=2,
			DESC=3
		)

	for ip4 in list(ip_network("192.168.160.0/22"))[1:-1]:
		filch(str(ip4), filch.discoverer, retry=0, timeout=1, verbose=0)







