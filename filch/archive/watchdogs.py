from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import Transmutation
from pygwarts.magical.time_turner.timers				import Sectimer
from pygwarts.filch.houses.linkindor					import GP_ARP_LOG
from pygwarts.filch.houses.apppuf						import GP_SNMP_TRAP_INFO
from pygwarts.filch.houses.apppuf						import GP_SNMP_TRAP_UPTIME








class ARPWatchdog(Transmutation):

	"""
		All (for now) ARP requests handler
	"""

	def mutable_chain(self, layer :Transmutable) -> Transmutable :
		class TimerInSeconds(super().mutable_chain(layer)):


			@property
			def filch(self) : return self.intercept._upper_layer.filch
			def inspect(self, message :str) -> str | super | None :

				"""
					Must implement inspection of log to handle in complex:
					- IP lookup requests;
					- unknown MAC in requests;
					- unknown IP in requesrs;
				"""

				try:

					dst, src, mac = GP_ARP_LOG.fullmatch(message).group("dst", "src", "mac")
					current_lines = list()


					macmatch = self.filch.macmap(mac)
					if macmatch:

						mapped_ip, mapped_host,_ =  macmatch
					else:
						mapped_ip, mapped_host = str(),str()


					# IP lookups for known/unknown/spoofed sources.
					# Spoofing detected by mentioning MAC.
					if src == "0.0.0.0":

						if mapped_ip == dst : current_lines.append(f"ARP: {mapped_host} IP lookup")
						else:

							try:	mapped_dst_host = self.filch.ipmap_host(dst)
							except	KeyError : mapped_dst_host = None


							current_lines.append(

								"ARP: %s lookup from %s MAC"%(

									mapped_dst_host	if mapped_dst_host	else f"unknown {dst}",
									mapped_host		if mapped_host		else f"unknown {mac}"
								)
							)


					else:


						# Known for filch source might be either from known/unknown MAC.
						# Mentioning MAC means unknown, mentioning host means spoofing.
						# Normal known source mapped with right MAC is omitted.
						if src in self.filch and src != mapped_ip:
							current_lines.append(

								"ARP: %s source request from %s MAC"%(

									self.filch.ipmap_host(src),
									mapped_host if mapped_host else f"unknown {mac}"
								)
							)




						# Source is unknown and either MAC known/unknown.
						# Gratuitous requests are ommited.
						elif src not in self.filch:
							current_lines.append(
							
								"ARP: unknown %s source request from %s MAC"%(

									src,
									mapped_host if mapped_host else f"unknown {mac}"
								)
							)




						# Unknown destination for not lookup trigger.
						if dst not in self.filch : current_lines.append(f"ARP: request for unknown {dst}")


					# All current lines (if any) concetenated by the new line and one more new line
					# is added to the end for additional indentation.
					if len(current_lines) : return "%s\n"%"\n".join(current_lines)


				# This is the point, where regex match was not successfull, so execution is passed
				# to invoke next watchdog decorator by accessing super object. It also might be
				# accessed in successfull match case if none of handling logic was activated and
				# "inspect" method simply not returned anywhere.
				#
				# First caught only for AttributeError, because if log line parse will fail,
				# None will be returned before group access, so basicly no unpacking might occur
				# for TypeError to be raised after parsing.
				except	AttributeError : pass
				if hasattr(super(), "inspect") : return super().inspect(message)


		return TimerInSeconds








class UptimeWatchdog(Transmutation):

	"""
		Some (because might be others) SNMP (v1) traps from Polykom-740 handler
	"""

	def mutable_chain(self, layer :Transmutable) -> Transmutable :
		class TimerInSeconds(super().mutable_chain(layer)):


			@property
			def filch(self) : return self.intercept._upper_layer.filch
			def inspect(self, message :str) -> str or super or None :

				"""
					Must implement inspection of log in complex to hanlde:
					- device uptime less than one day
				"""

				try:

					src,uptime = GP_SNMP_TRAP_UPTIME.fullmatch(message).group("src", "uptime")
					if int(uptime) < 86400:

						if		src in self.filch : sender = self.filch.ipmap_host(src).split("-")[2]
						else:	sender = src


						return f"{sender} uptime is {Sectimer.sectimer(uptime)}\n"


					# Returning at this point, so no further watchdog matching will occur,
					# as uptime check might match typical SNMP watchdog parse, but at this point
					# uptime comparisson was triggered but passed.
					return


				# This is the point, where regex match was not successfull, so execution is passed
				# to invoke next watchdog decorator by accessing super object. It also might be
				# accessed in successfull match case if none of handling logic was activated and
				# "inspect" method simply not returned anywhere.
				#
				# First caught only for AttributeError, because if log line parse will fail,
				# None will be returned before group access, so basicly no unpacking might occur
				# for TypeError to be raised after parsing.
				except	AttributeError : pass
				if hasattr(super(), "inspect") : return super().inspect(message)


		return TimerInSeconds








class TrapWatchdog(Transmutation):

	"""
		Any SNMP trap caught being intercepted
	"""

	def mutable_chain(self, layer :Transmutable) -> Transmutable :
		class TimerInSeconds(super().mutable_chain(layer)):


			@property
			def filch(self) : return self.intercept._upper_layer.filch
			def inspect(self, message :str) -> str or super or None :

				"""
					Must implement inspection of log in complex to hanlde:
					- any trap parsed out being intercepted
				"""

				try:

					src,msg = GP_SNMP_TRAP_INFO.fullmatch(message).group("src", "msg")

					if		src in self.filch : sender = self.filch.ipmap_host(src).split("-")[2]
					else:	sender = src


					return f"{sender} {msg}\n"


				# This is the point, where regex match was not successfull, so execution is passed
				# to invoke next watchdog decorator by accessing super object. It also might be
				# accessed in successfull match case if none of handling logic was activated and
				# "inspect" method simply not returned anywhere.
				#
				# First caught only for AttributeError, because if log line parse will fail,
				# None will be returned before group access, so basicly no unpacking might occur
				# for TypeError to be raised after parsing.
				except	AttributeError : pass
				if hasattr(super(), "inspect") : return super().inspect(message)


		return TimerInSeconds








class PolykomWatchdog(Transmutation):

	"""
		Some (because might be others) SNMP (v1) traps from Polykom-740 handler
	"""

	def mutable_chain(self, layer :Transmutable) -> Transmutable :
		class TimerInSeconds(super().mutable_chain(layer)):


			@property
			def filch(self) : return self.intercept._upper_layer.filch
			def inspect(self, message :str) -> str or super or None :

				"""
					Must implement inspection of log in complex to hanlde:
					- port status changes
				"""

				try:

					src,msg = GP_SNMP_TRAP_INFO.fullmatch(message).group("src", "msg")
					if "status on port " in msg:

						if src in self.filch : sender = self.filch.ipmap_host(src)
						else: sender = src


						return f"{sender} {msg}\n"


				# This is the point, where regex match was not successfull, so execution is passed
				# to invoke next watchdog decorator by accessing super object. It also might be
				# accessed in successfull match case if none of handling logic was activated and
				# "inspect" method simply not returned anywhere.
				#
				# First caught only for AttributeError, because if log line parse will fail,
				# None will be returned before group access, so basicly no unpacking might occur
				# for TypeError to be raised after parsing.
				except	AttributeError : pass
				if hasattr(super(), "inspect") : return super().inspect(message)


		return TimerInSeconds







