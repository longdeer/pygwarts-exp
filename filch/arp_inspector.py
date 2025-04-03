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
			state ^= (srcmac != mapped_mac) <<9
			state ^= (dstip != maced_ip) <<10
			state ^= (dstip == srcip) <<11

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








class ARPResponseInspector(Transmutable):

	"""
		Utility object, that implements processing of ip4 and MAC addresses, that are taken as a response
		to ARP request. Returns a dictionary with response state integer, that describes "filchmap"
		inspection result, along with such result. If response parsing failed or valid "filchmap"
		is absent, returns None.
	"""

	filchmap :MaraudersMap

	def __call__(self, srcip :str, srcmac :str) -> Dict[str,int|str] :

		try:

			state  = srcip in self.filchmap.ip4
			state ^= bool(mapped_mac := self.filchmap.ip4map_mac(srcip)) <<1
			state ^= bool(mapped_name := self.filchmap.ip4map_name(srcip)) <<2
			state ^= bool(maced_ip := self.filchmap.macmap_ip4(srcmac)) <<3
			state ^= bool(maced_name := self.filchmap.macmap_name(srcmac)) <<4
			state ^= (mapped_name == maced_name) <<5
			state ^= (srcmac != mapped_mac) <<6
			state ^= (srcip != maced_ip) <<7

		except:	return
		else:	return	{

				"state":				state,
				"source ip4":			srcip,
				"source MAC":			srcmac,
				"source ip4 to MAC":	mapped_mac,
				"source ip4 to name":	mapped_name,
				"source MAC to ip4":	maced_ip,
				"source MAC to name":	maced_name,
			}







