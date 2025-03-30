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

		root = "/mnt/container/ArrestedDevelopment/pygwarts/development/filch"
		# root = "/srv/lcontainer/filch"

		@DIRTtimer(T=-kill)
		class Broadwatch(ARPSniffer):

			class loggy(LibraryContrib):

				# handler		= f"{root}/broadwatch/{point.Ym_aspath}/gbroadwatch{point.dmY_asjoin}.loggy"
				init_name	= "filch"
				watchdog	= "Broadwatch.RequestInspector",

			class filchmap(MaraudersMap): pass
			class RequestInspector(Transmutable):
				def __call__(self, request :str):

					# It must be valid request anyway
					dstip,srcip,srcmac = GP_ARP_REQ_LOG.search(request).group("dst", "src", "mac")

					state = 0

					state ^= srcip in self.filchmap.ip4										# 1
					state ^= (srcip == "0.0.0.0") <<1										# 2
					state ^= (dstip in self.filchmap.ip4) <<2								# 4
					state ^= bool(mapped_mac := self.filchmap.ip4map_mac(srcip)) <<3		# 8
					state ^= bool(mapped_name := self.filchmap.ip4map_name(srcip)) <<4		# 16
					state ^= bool(maced_ip := self.filchmap.macmap_ip4(srcmac)) <<5			# 32
					state ^= bool(maced_name := self.filchmap.macmap_name(srcmac)) <<6		# 64
					state ^= bool(mapped_dst_mac := self.filchmap.ip4map_mac(dstip)) <<7	# 128
					state ^= bool(mapped_dst_name := self.filchmap.ip4map_name(dstip)) <<8	# 256
					state ^= bool(srcmac != mapped_mac) <<9									# 512
					state ^= bool(dstip != maced_ip) <<10									# 1024
					state ^= bool(dstip == srcip) <<11										# 2048

					self.loggy.info(f"{state = }")

					match state:

						# case 509:	return	# gratuitous request
						case 2557:	return	# gratuitous request
						case 1533:	return	# full mapped request

						# mapped mac lookup for mapped ip4
						# 2 + 4 + 32 + 64 + 128 + 256 + 512
						case 998:	self.loggy.info(f"{maced_name} ip4 lookup")
						# missed mac lookup for mapped ip4
						# 2 + 4 + 32 + 64 + 128 + 256 + 512 + 1024
						case 2022:	self.loggy.info(f"{maced_name} lookup for {mapped_dst_name} ip4")
						# mapped mac lookup for unknown ip4
						# 2 + 32 + 64 + 512 + 1024
						case 1634:	self.loggy.info(f"{maced_name} lookup for unknown {dstip}")
						# unknown mac lookup for mapped ip4
						# 2 + 4 + 128 + 256 + 512 + 1024
						case 1926:	self.loggy.info(f"unknown {srcmac} lookup for {mapped_dst_name} ip4")
						# unknown mac lookup for unknown ip4
						# 2 + 512 + 1024
						case 1538:	self.loggy.info(f"unknown {srcmac} lookup for unknown {dstip}")

						# mapped request for unknown ip4
						# 1 + 8 + 16 + 32 + 64 + 1024
						case 1145:	self.loggy.info(f"{mapped_name} requested unknown {dstip}")
						# unknown mac and ip request for mapped ip4
						# 128 + 256 + 512 + 1024
						case 1920:	self.loggy.info(f"unknown {srcmac} requested {mapped_dst_name} from unknown {srcip}")
						# unknown mac and ip request for unknown ip4
						# 512 + 1024
						case 1536:	self.loggy.info(f"unknown {srcmac} requested unknown {dstip} from unknown {srcip}")
						# missed ip request for mapped ip4
						# 1 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 1024
						case 2045:	self.loggy.info(f"{maced_name} requested {mapped_dst_name} from {mapped_name} ip4")
						# missed ip request for unknown ip4
						# 1 + 8 + 16 + 32 + 64 + 512 + 1024
						case 1657:	self.loggy.info(f"{maced_name} requested unknown {dstip} from {mapped_name} ip4")
						# unknown ip4 but mapped mac request for mapped ip4
						# 4 + 32 + 64 + 128 + 256 + 512 + 1024
						case 2020:	self.loggy.info(f"{maced_name} reqeusted {mapped_dst_name} from unknown {srcip}")
						# unknown ip4 but mapped mac request for unknown ip4
						# 32 + 64 + 512 + 1024
						case 1632:	self.loggy.info(f"{maced_name} reqeusted unknown {dstip} from unknown {srcip}")
						# unknown mac but mapped ip4 request for mapped ip4
						# 1 + 4 + 8 + 16 + 128 + 256 + 512 + 1024
						case 1949:	self.loggy.info(f"unknown {srcmac} requested {mapped_dst_name} from {mapped_name} ip4")
						# unknown mac but mapped ip4 request for unknown ip4
						# 1 + 8 + 16 + 512 + 1024
						case 1561:	self.loggy.info(f"unknown {srcmac} requested unknown {dstip} from {mapped_name} ip4")

						# # 1 + 4 + 16 + 512
						# case 533:	self.loggy.info(f"request with {mapped_name} mac missmatching")
						# mapped mac but unknown ip4 gratuitous request
						# 32 + 64 + 512 + 1024 + 2048
						case 3680:	self.loggy.info(f"unknown {dstip} gratuitous request from {maced_name} mac")
						# case 3680:	self.loggy.info(f"{maced_name} gratuitous request with unknown {dstip}")
						# unknown mac and ip gratuitous request
						# 512 + 1024 + 2048
						case 3584:	self.loggy.info(f"unknown {srcmac} gratuitous request from unknown {dstip}")

						case _:		self.loggy.info(f"unknown request state {state}")


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







