from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import DIRTtimer
from pygwarts.tests.filch					import FilchTestCase
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.filch.linkindor				import EUI48_format
from pygwarts.filch.linkindor				import P_ARP_REQ
from pygwarts.filch.linkindor.sniffing		import ARPSniffer
from scapy.all								import sniff
from scapy.all								import Ether
from scapy.all								import ARP








# print(TimeTurner().diff(subtrahend=TimeTurner(timepoint="1712")))
# Initiating sniffing timer to 23 o'clock
if	(kill_timer := TimeTurner().diff(subtrahend=TimeTurner(timepoint="1718"))) <0:

	@DIRTtimer(T=-kill_timer)
	class Filch(ARPSniffer):

		class loggy(LibraryContrib):

			handler		= "arp_watch.loggy"
			# handler		= "file handler path (optional)"
			init_name	= "filch"

		def trap(self, FRAME :Ether):

			if	(MAC := EUI48_format(FRAME.src)) is not None:
				match FRAME[ARP].op:

					case 1:	self.loggy.info(f"{P_ARP_REQ.search(FRAME.summary()).group()} ({MAC})")
					case 2:	self.loggy.debug(f"{MAC} answer")
					case _:	self.loggy.debug(FRAME.summary())








	filch = Filch()
	filch(sniff, filter="arp", prn=filch.trap)
else:
	print("No")







