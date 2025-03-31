from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import DIRTtimer
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.filch.marauders_map			import MaraudersMap
from pygwarts.filch.linkindor				import EUI48_format
from pygwarts.filch.linkindor				import P_ARP_REQ
from pygwarts.filch.linkindor				import GP_ARP_REQ_LOG
from pygwarts.filch.linkindor.sniffing		import ARPSniffer
from scapy.all								import sniff
from scapy.all								import Ether
from scapy.all								import ARP








if	__name__ == "__main__":
	if	(kill := (point := TimeTurner()).diff(subtrahend=TimeTurner(timepoint="2300"))) <0:

		root = "/srv/lcontainer/filch"

		@DIRTtimer(T=-kill)
		class Broadwatch(ARPSniffer):

			class loggy(LibraryContrib):

				handler		= f"{root}/broadwatch/{point.Ym_aspath}/gbroadwatch{point.dmY_asjoin}.loggy"
				init_name	= "filch"
				watchdog	= "Broadwatch.RequestInspector",

			class filchmap(MaraudersMap): pass
			class RequestInspector(Transmutable):
				def __call__(self, request :str):

					dstip,srcip,srcmac = GP_ARP_REQ_LOG.search(request).group("dst", "src", "mac")
					state = 0

					state ^= srcip in self.filchmap.ip4
					state ^= (srcip == "0.0.0.0") <<1
					state ^= (dstip in self.filchmap.ip4) <<2
					state ^= bool(mapped_mac := self.filchmap.ip4map_mac(srcip)) <<3
					state ^= bool(mapped_name := self.filchmap.ip4map_name(srcip)) <<4
					state ^= bool(maced_ip := self.filchmap.macmap_ip4(srcmac)) <<5
					state ^= bool(maced_name := self.filchmap.macmap_name(srcmac)) <<6
					state ^= bool(mapped_dst_mac := self.filchmap.ip4map_mac(dstip)) <<7
					state ^= bool(mapped_dst_name := self.filchmap.ip4map_name(dstip)) <<8
					state ^= bool(srcmac != mapped_mac) <<9
					state ^= bool(dstip != maced_ip) <<10
					state ^= bool(dstip == srcip) <<11

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
								self.RequestInspector(current)
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







