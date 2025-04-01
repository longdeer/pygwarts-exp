from typing									import Dict
from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.filch.marauders_map			import MaraudersMap
from pygwarts.filch.linkindor				import GP_ARP_REQ_LOG








class ARPRequestInspector(Transmutable):

	"""
		Utility object, that implements pygwarts ARP request (MAC added) processing and obtaining "state"
		according to "filchmap" mapping. Returns a dictionary with discovered state integer, that
		describes "filchmap" inspection result, along with such result. If request parsing failed or valid
		"filchmap" is absent, returns None.
	"""

	filchmap :MaraudersMap

	def __call__(self, request :str) -> Dict[str,int|str] :

		try:	dstip, srcip, srcmac = GP_ARP_REQ_LOG.search(request).group("dst", "src", "mac")
		except:	return
		else:

			state  = srcip in self.filchmap.ip4
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

			return	{

				"state":				state,
				"source ip4":			srcip,
				"target ip4":			dstip,
				"source MAC":			srcmac,
				"source ip4 to MAC":	mapped_mac,
				"source ip4 to name":	mapped_name,
				"source MAC to ip4":	maced_ip,
				"source MAC to name":	maced_name,
				"target ip4 to MAC":	mapped_dst_mac,
				"target ip4 to name":	mapped_dst_name,
			}







