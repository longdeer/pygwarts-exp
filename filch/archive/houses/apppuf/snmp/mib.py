from collections						import defaultdict
from pygwarts.filch.houses.apppuf.snmp	import MIBResolver
from pygwarts.filch.houses.apppuf.snmp	import I_inject








class GMDSSA2MIB(MIBResolver):

	"""
		RMP implementation
	"""

	mib_skip = "snmpTrapEnterprise", "snmpTrapOID", "snmpTrapAddress", "snmpTrapCommunity",


	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.MIB_mapping.update({

			"DS1-MIB": {

				"dsx1LoopbackStatus": {

					"sub": "loopback on port",
					"act": lambda st,I : " set to %s%s"%(

						"off" if st == "1" else "payload" if st == "2" else "inward" if st == "5" else st,
						I_inject(I)
					),
					"log": defaultdict(lambda : "warning", **{ "1": "debug" }),
				},

				"dsx1LineStatus": {

					"sub": "status on port",
					"act": lambda st,I : " changed to %s%s"%(

						"NORMAL" if st == "1" else "AIS" if st == "8" else "LOSS" if st == "64" else st,
						I_inject(I)
					),
					"log": defaultdict(lambda : "warning", **{ "1": "info", "8": "info", "64": "info", }),
				},
			},
		})







