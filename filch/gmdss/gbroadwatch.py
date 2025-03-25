from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import DIRTtimer
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.filch.marauders_map			import MaraudersMap
from pygwarts.filch.linkindor				import EUI48_format
from pygwarts.filch.linkindor				import P_ARP_REQ
from pygwarts.filch.linkindor.sniffing		import ARPSniffer
from scapy.all								import sniff
from scapy.all								import Ether
from scapy.all								import ARP








if	__name__ == "__main__":
	if	(kill := (point := TimeTurner()).diff(subtrahend=TimeTurner(timepoint="2300"))) <0:

		root = "/srv/lcontainer/filch"

		@DIRTtimer(T=-kill)
		class Filch(ARPSniffer):

			class loggy(LibraryContrib):

				handler		= f"{root}/broadwatch/{point.Ym_aspath}/gbroadwatch{point.dmY_asjoin}.loggy"
				init_name	= "filch"

			class filchmap(MaraudersMap):	pass
			def trap(self, FRAME :Ether):

				if	(MAC := EUI48_format(FRAME.src)) is not None:
					match FRAME[ARP].op:

						case 1:	self.loggy.info(f"{P_ARP_REQ.search(FRAME.summary()).group()} ({MAC})")
						case 2:	self.loggy.debug(f"{MAC} answer")
						case _:	self.loggy.debug(FRAME.summary())








		filch = Filch()
		filch.filchmap.CSV(

			f"{root}/broadmap.csv",
			";",
			IP4=0,
			MAC=1,
			NAME=2,
			DESC=3
		)
		filch(sniff, filter="arp", prn=filch.trap)







