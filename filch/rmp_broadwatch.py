from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import DIRTtimer
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.filch.marauders_map			import MaraudersMap
from pygwarts.filch.linkindor				import EUI48_format
from pygwarts.filch.linkindor				import P_ARP_REQ
from pygwarts.filch.linkindor.sniffing		import ARPSniffer
from irma_local								import TelegramTechHoist
from filch_local							import ARPRequestInspector
from scapy.all								import sniff
from scapy.all								import Ether
from scapy.all								import ARP








if	__name__ == "__main__":
	if	(kill := (point := TimeTurner()).diff(subtrahend=TimeTurner(timepoint="2300"))) <0:

		root = "/srv/lcontainer/filch"

		@DIRTtimer(T=-kill)
		class Broadwatch(ARPSniffer):

			@TelegramTechHoist
			class loggy(LibraryContrib):

				handler		= f"{root}/broadwatch/{point.Ym_aspath}/broadwatch{point.dmY_asjoin}.loggy"
				init_name	= "filch"
				watchdog	= "Broadwatch.Inspector",

			class filchmap(MaraudersMap): pass
			class Inspector(ARPRequestInspector):

				def __call__(self, request :str):

					if	(result := super().__call__(request)) is not None:

						state			= result["state"]
						srcip			= result["source ip4"] 
						dstip			= result["target ip4"] 
						srcmac			= result["source MAC"]
						mapped_name		= result["source ip4 to name"]
						maced_name		= result["source MAC to name"]
						mapped_dst_name	= result["target ip4 to name"]

						match state:

							case 1533:	return
							case 2557:	return

							case 998:	self.loggy.info(f"{maced_name} ip4 lookup")
							case 1145:	self.loggy.info(f"{mapped_name} requested unknown {dstip}")
							case 1536:	self.loggy.info(f"unknown {srcmac} requested unknown {dstip} from unknown {srcip}")
							case 1538:	self.loggy.info(f"unknown {srcmac} lookup for unknown {dstip}")
							case 1561:	self.loggy.info(f"unknown {srcmac} requested unknown {dstip} from {mapped_name} ip4")
							case 1632:	self.loggy.info(f"{maced_name} reqeusted unknown {dstip} from unknown {srcip}")
							case 1634:	self.loggy.info(f"{maced_name} lookup for unknown {dstip}")
							case 1657:	self.loggy.info(f"{maced_name} requested unknown {dstip} from {mapped_name} ip4")
							case 1924:	self.loggy.info(f"unknown {srcmac} requested {mapped_dst_name} from unknown {srcip}")
							case 1926:	self.loggy.info(f"unknown {srcmac} lookup for {mapped_dst_name} ip4")
							case 1949:	self.loggy.info(f"unknown {srcmac} requested {mapped_dst_name} from {mapped_name} ip4")
							case 2020:	self.loggy.info(f"{maced_name} reqeusted {mapped_dst_name} from unknown {srcip}")
							case 2022:	self.loggy.info(f"{maced_name} lookup for {mapped_dst_name} ip4")
							case 2045:	self.loggy.info(f"{maced_name} requested {mapped_dst_name} from {mapped_name} ip4")
							case 3584:	self.loggy.info(f"unknown {srcmac} gratuitous request from unknown {dstip}")
							case 3680:	self.loggy.info(f"unknown {dstip} gratuitous request from {maced_name} mac")
							case 4093:	self.loggy.info(f"{maced_name} gratuitous request from {mapped_name} ip4")

							case _:		self.loggy.info(f"unknown request state {state} for {dstip} request from {srcip}")


			def trap(self, FRAME :Ether):

				if	(MAC := EUI48_format(FRAME.src)) is not None:
					match FRAME[ARP].op:

						case 1:
							if	isinstance(current := P_ARP_REQ.search(FRAME.summary()).group(), str):

								current += f" ({MAC})"
								self.loggy.info(current)
								self.Inspector(current)
						case 2:	self.loggy.debug(f"{MAC} answer")
						case _:	self.loggy.debug(FRAME.summary())








		filch = Broadwatch()
		filch.filchmap.CSV(

			f"{root}/broadmap.csv",
			";",
			IP4=0,
			MAC=1,
			NAME=2,
			DESC=3
		)
		filch(sniff, filter="arp", prn=filch.trap)







