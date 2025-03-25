from typing									import Any
from typing									import List
from typing									import Dict
from typing									import Tuple
from typing									import Callable
from sys									import exc_info
from time									import time
from asyncore								import loop
from traceback								import format_exception
from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.filch.marauders_map			import MaraudersMap
from pygwarts.filch.apppuf.snmp				import SNMPtrap
from pysnmp.entity							import config
from pysnmp.entity.engine					import SnmpEngine
from pysnmp.entity.rfc3413					import ntfrcv
from pysnmp.carrier.asyncore.dgram			import udp
from pysnmp.carrier.asyncore.dispatch		import AsyncoreDispatcher as ScapyDispatcher
from pysnmp.smi								import builder
from pysnmp.smi								import view
from pysnmp.smi.rfc1902						import ObjectType
from pysnmp.smi.rfc1902						import ObjectIdentity
from pysnmp.proto.rfc1902					import ObjectName
from pysnmp.proto.rfc1902					import OctetString
from pysnmp.error							import PySnmpError








class Filch(SNMPtrap):
	class loggy(LibraryContrib):

		init_name	= "filch"
		init_level	= 10
		force_info	= "*filchmap*",

	def __init__(self):
		super().__init__()

		class AsyncoreDispatcher(ScapyDispatcher):
			def runDispatcher(self, kill_timer :int):

				start = time()

				while self.jobsArePending() or self.transportsAreWorking():
					tick = time()

					if		kill_timer <tick - start : break
					try:	loop(self.getTimerResolution(), use_poll=True, map=self.__sockMap, count=1)
					except	KeyboardInterrupt : raise
					except:	raise PySnmpError("poll error: %s"%";".join(format_exception(*exc_info())))

					self.handleTimerTick(tick)

		self.dispatcher = AsyncoreDispatcher
		self.builder	= builder.MibBuilder()
		self.viewer		= view.MibViewController(self.builder)
		self.handlers	= list()




	def trap(self, listen_ip :str, listen_port :int, listen_time :int, community :str, community_i :str):

		ENGINE = SnmpEngine()
		ENGINE.registerTransportDispatcher(self.dispatcher())
		self.loggy.debug(f"Registered dispatcher {ENGINE.transportDispatcher}")

		config.addTransport(

			ENGINE,
			udp.domainName + ( 1, ),
			udp.UdpTransport().openServerMode(( listen_ip,listen_port ))
		)
		self.loggy.debug(f"UDP transport established for {listen_ip}:{listen_port}")

		config.addV1System(ENGINE, community_i, community)
		nr = ntfrcv.NotificationReceiver(ENGINE, self.callback)
		self.loggy.debug(f"Registered receiver {nr}")

		try:

			self.loggy.debug("Starting dispatcher")
			ENGINE.transportDispatcher.jobStarted(1)
			ENGINE.transportDispatcher.runDispatcher(listen_time)

		finally:

			self.loggy.debug("Closing dispatcher")
			ENGINE.transportDispatcher.closeDispatcher()


	def get_modules(self, sources :List[str], modules :List[str]):

		self.builder.addMibSources(*( builder.DirMibSource(S) for S in sources ))
		self.builder.loadModules(*modules)

		module_name	= self.viewer.getFirstModuleName()

		while True:

			if		module_name : self.loggy.info(f"Loaded module {module_name}")
			try:	module_name = self.viewer.getNextModuleName(module_name)
			except:	break


	def callback(
					self,
					engine				:SnmpEngine,
					state_reference		:int,
					context_engine_id	:OctetString,
					context_name		:OctetString,
					bind_variables		:List[Tuple[ObjectName,Any]],
					cbCtx				:Any,
				)-> Dict[str,List[str]]	:

		context = engine.observer.getExecutionContext("rfc3412.receiveMessage:request")
		SRC = context["transportAddress"][0]
		self.loggy.debug(f"Callback on {SRC} trap")

		for name, value in bind_variables:

			rfcobj = ObjectType(ObjectIdentity(name), value).resolveWithMib(self.viewer)
			NMOD, NSYM, NIND = rfcobj[0].getMibSymbol()

			try:	NIND = NIND[0]
			except:	pass

			try:	VMOD, VSYM, VIND = rfcobj[1].getMibSymbol()
			except:	VMOD, VSYM, VIND = str(), str(rfcobj[1]), str()

			current = (

				str(SRC),
				str(NMOD), str(NSYM), str(NIND),
				str(VMOD), str(VSYM),
				str(VIND) if VIND else str()
			)

			self.loggy.debug(f"Trap summary: {current}")
			self.Handler(current)




	class filchmap(MaraudersMap): pass
	class Handler(Transmutable):

			dsx1LoopbackStatus = {

				"2":	"Near end payload loopback",
				"4":	"Near end line loopback",
				"8":	"Near end other loopback",
				"16":	"Near end inward loopback",
				"32":	"Far end payload loopback",
				"64":	"Far end line loopback",
			}
			dsx1LineStatus = {

				"1":		"No alarm present",
				"2":		"Far end LOF (a.k.a., Yellow Alarm)",
				"4":		"Near end sending LOF Indication",
				"8":		"Far end sending AIS",
				"16":		"Near end sending AIS",
				"32":		"Near end LOF (a.k.a., Red Alarm)",
				"64":		"Near end Loss Of Signal",
				"128":		"Near end is looped",
				"256":		"E1 TS16 AIS",
				"512":		"Far End Sending TS16 LOMF",
				"1024":		"Near End Sending TS16 LOMF",
				"2048":		"Near End detects a test code",
				"4096":		"any line status not defined here",
				"8192":		"Near End in Unavailable Signal State",
				"16384":	"Carrier Equipment Out of Service",
				"32768":	"DS2 Payload AIS",
				"65536":	"DS2 Performance Threshold Exceeded",
			}

		def name(self, addr :str) -> str :

			try:
				if	(host_name := self.filchmap.ip4map_name(addr)) is not None:
					return host_name
			except:	return addr
			else:	return addr

		def __call__(self, chunk :Tuple[str,str,str,str,str,str,str]):

			match chunk:

				case ( src, "SNMPv2-MIB", "sysUpTime", *_ ):					return
				case ( src, "SNMPv2-MIB", "snmpTrapOID", *_ ):					return
				case ( src, "SNMPv2-MIB", "snmpTrapEnterprise", *_):			return
				case ( src, "SNMP-COMMUNITY-MIB", "snmpTrapAddress", *_ ):		return
				case ( src, "SNMP-COMMUNITY-MIB", "snmpTrapCommunity", *_ ):	return
				case ( src, "DS1-MIB", "dsx1LoopbackStatus", P, _, S, _ ):

					if	S != "1":

						self.loggy.info(
							f"{self.name(src)} port {P} loopback status: {self.dsx1LoopbackStatus.get(S)}"
						)

				case ( src, "DS1-MIB", "dsx1LineStatus", P, _, S, _ ):

					self.loggy.info(
						f"{self.name(src)} port {P} line status: {self.dsx1LineStatus.get(S)}"
					)

				case ( src, MIB, *details ):

					self.loggy.info(f"{self.name(src)} {MIB}: {details}")








if	__name__ == "__main__":

	filch = Filch()
	filch.filchmap.CSV(

		"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/broadmap.csv",
		";",
		IP4=0,
		MAC=1,
		NAME=2,
		DESC=3
	)
	filch.get_modules(

		[ "~/.pysnmp/mibs" ],
		[ "SNMPv2-MIB", "IF-MIB", "SNMP-COMMUNITY-MIB", "XPPC-MIB", "POLYGON-MIB", "POLYCOM740-MIB" ]
	)

	filch("127.0.0.18", 54321, filch.trap, listen_time=100, community="trap", community_i="area")







