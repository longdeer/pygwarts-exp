from collections							import defaultdict
from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.utils		import DATETIME_1_P
from pygwarts.magical.patronus				import CAST
from pygwarts.irma.access.handlers.parsers	import GroupParser








class BroadwatchAccessHandler(GroupParser):

	"""
		Handles broadwatch
	"""

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.recap = {

			"mapped_requests":		list(),
			"unmapped_requests":	list(),
			"missmatched_mac":		list(),
			"missmatched_ip":		list(),
			"ip_lookup":			list(),
		}


	@GroupParser.register_counter
	def __call__(self, line :str, register :str) -> bool :

		if	(linked_register := super().__call__(line, register)) is not None :
			if	(target := self.parse(line, "dst", "src", "mac")) is not None :
				if	(len(target) == 3):

					dst,src,mac = target
					self.loggy.debug(f"Considering {dst} request from {src} at {mac}")


					try:	DT = TimeTurner(*DATETIME_1_P.search(line).group("date", "time"))
					except	Exception as E:

						self.loggy.warning(f"Failed to obtain datetime due to {CAST(E)}")
						return




					if	src in self.filchmap:

						mapped_mac, mapped_name,_ = self.filchmap.ipmap(src)

						if	dst in self.filchmap:
							DST = self.filchmap.ipmap_host(dst)


							# The following relies on loggy file to be formatted the way it is
							# defaulted for LibraryContrib class, so any changes in format
							# must be maintained for datetime obtaining in this section.
							if	mac != mapped_mac:

								self.loggy.debug(f"Spoofguard triggered")
								# source {mapped_name} mac missmatching @ DT
								self.recap["missmatched_mac"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=mapped_name,
										source_mapped_mac=mapped_mac,
										source_maced_ip=None,
										source_maced_name=None,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=DST,
										timestamp=DT,
									)
								)


							else:
								self.loggy.debug("Mapped request")
								# self.recap["mapped_requests"][mapped_name][DST] += 1
								self.recap["mapped_requests"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=mapped_name,
										source_mapped_mac=mapped_mac,
										source_maced_ip=None,
										source_maced_name=None,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=DST,
										timestamp=DT,
									)
								)


						else:
							self.loggy.debug("Unmapped destination request")
							# self.recap["unmapped_requests"][mapped_name][dst] += 1
							self.recap["unmapped_requests"].append(

								dict(

									request_source_ip=src,
									request_source_mac=mac,
									source_mapped_name=mapped_name,
									source_mapped_mac=mapped_mac,
									source_maced_ip=None,
									source_maced_name=None,
									request_target_ip=dst,
									target_mapped_ip=None,
									target_mapped_name=None,
									timestamp=DT,
								)
							)




					elif	src == "0.0.0.0":

						if	(record := self.filchmap.macmap(mac)) is not None :

							maced_ip, maced_host_name,_ = record

							if	maced_ip == dst:

								self.loggy.debug("Mapped ip lookup")
								# {maced_host_name} ip lookup @ DT
								self.recap["ip_lookup"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=maced_ip,
										source_maced_name=maced_host_name,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=None,
										timestamp=DT,
									)
								)


							elif	dst in self.filchmap:

								self.loggy.debug("Mapped mac missmatched mapped ip lookup")
								dst_name = self.filchmap.ipmap_host(dst)
								self.recap["ip_lookup"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=None,
										source_maced_name=maced_host_name,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=dst_name,
										timestamp=DT,
									)
								)


							else:
								self.loggy.debug("Mapped mac missmatched unmapped ip lookup")
								self.recap["ip_lookup"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=None,
										source_maced_name=maced_host_name,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=None,
										timestamp=DT,
									)
								)


						elif	dst in self.filchmap:

							dst_mac, dst_name, _ = self.filchmap.ipmap(dst)
							self.loggy.debug("Mapped target lookup from unmapped address")
							# {dst_name} ip lookup from unknown {mac} @ DT
							self.recap["ip_lookup"].append(

								dict(

									request_source_ip=src,
									request_source_mac=mac,
									source_mapped_name=None,
									source_mapped_mac=None,
									source_maced_ip=None,
									source_maced_name=None,
									request_target_ip=dst,
									target_mapped_ip=dst,
									target_mapped_name=dst_name,
									timestamp=DT,
								)
							)


						else:
							self.loggy.debug("Unmapped target lookup from unmapped address")
							# unknown {dst} lookup from unknown {mac} @ DT
							self.recap["ip_lookup"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=None,
										source_maced_name=None,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=None,
										timestamp=DT,
									)
								)




					elif	src is not None:

						if	(record := self.filchmap.macmap(mac)) is not None :

							maced_ip, maced_host_name,_ = record

							if	dst in self.filchmap:

								DST = self.filchmap.ipmap_host(dst)
								self.loggy.debug("Mapped target request from missmatched ip")
								# source {maced_name} ip missmatching @ DT
								self.recap["missmatched_ip"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=None,
										source_maced_name=maced_host_name,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=DST,
										timestamp=DT,
									)
								)

							else:
								self.loggy.debug("Unknown target request from missmatched ip")
								# unknown {dst} request from missmatched {maced_name} ip @ DT
								self.recap["missmatched_ip"].append(

									dict(

										request_source_ip=src,
										request_source_mac=mac,
										source_mapped_name=None,
										source_mapped_mac=None,
										source_maced_ip=None,
										source_maced_name=maced_host_name,
										request_target_ip=dst,
										target_mapped_ip=None,
										target_mapped_name=None,
										timestamp=DT,
									)
								)


						elif	dst in self.filchmap:

							DST = self.filchmap.ipmap_host(dst)
							self.loggy.debug("Mapped target request from unmapped source")
							# self.recap["unmapped_requests"][src][DST] += 1
							self.recap["unmapped_requests"].append(

								dict(

									request_source_ip=src,
									request_source_mac=mac,
									source_mapped_name=None,
									source_mapped_mac=None,
									source_maced_ip=None,
									source_maced_name=None,
									request_target_ip=dst,
									target_mapped_ip=None,
									target_mapped_name=DST,
									timestamp=DT,
								)
							)


						else:
							self.loggy.debug("Unmapped target request from unmapped source")
							# self.recap["unmapped_requests"][src][dst] += 1
							self.recap["unmapped_requests"].append(

								dict(

									request_source_ip=src,
									request_source_mac=mac,
									source_mapped_name=None,
									source_mapped_mac=None,
									source_maced_ip=None,
									source_maced_name=None,
									request_target_ip=dst,
									target_mapped_ip=None,
									target_mapped_name=None,
									timestamp=DT,
								)
							)




					return True


				self.loggy.warning(f"Handler {self} invalid parse result for line \"{line}\"")
















class DiscoverywatchAccessHandler(GroupParser):

	"""
		Hadles all discoverywatch
	"""

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.recap = {

			"known_hosts":		list(),
			"unknown_ip":		list(),
			"unknown_mac":		list(),
			"missmatched_mac":	list(),
			"missmatched_ip":	list(),
		}


	@GroupParser.register_counter
	def __call__(self, line :str, register :str) -> bool :

		if	(linked_register := super().__call__(line, register)) is not None:
			if	(target := self.parse(line, "ip", "mac")) is not None:
				if	(len(target) == 2):


					ip,mac = target
					self.loggy.debug(f"Considering {ip} at {mac} discover")


					if	ip in self.filchmap:

						self.loggy.debug("Discovered ip mapped by filch")
						mapped_mac, host_name, desc = self.filchmap.ipmap(ip)


						if	mac == mapped_mac:

							self.loggy.debug("Discovered mac mapped by filch")
							self.recap["known_hosts"].append(

								dict(

									discovered_ip=ip,
									filch_mapped_mac=mapped_mac,
									filch_mapped_host_name=host_name,
									filch_mapped_description=desc,
									discovered_mac=mac,
									filch_maced_ip=None,
									filch_maced_host_name=None,
									filch_maced_description=None,
								)
							)


						elif(record := self.filchmap.macmap(mac)) is not None :

							maced_ip, maced_host_name, maced_desc = record
							self.loggy.debug("Discovered mac mapped by another host")
							self.recap["missmatched_mac"].append(

								dict(

									discovered_ip=ip,
									filch_mapped_mac=mapped_mac,
									filch_mapped_host_name=host_name,
									filch_mapped_description=desc,
									discovered_mac=mac,
									filch_maced_ip=maced_ip,
									filch_maced_host_name=maced_host_name,
									filch_maced_description=maced_desc,
								)
							)


						else:

							self.loggy.debug("Discovered unknown mac mapped by known ip")
							self.recap["unknown_mac"].append(

								dict(

									discovered_ip=ip,
									filch_mapped_mac=mapped_mac,
									filch_mapped_host_name=host_name,
									filch_mapped_description=desc,
									discovered_mac=mac,
									filch_maced_ip=None,
									filch_maced_host_name=None,
									filch_maced_description=None,
								)
							)




					# Unknowns handle, None check for sure, cause if it somehow None, due to "parse"
					# implementation, it is not enough just mapper presence check.
					elif	ip is not None and ip not in self.filchmap:
						if	(record := self.filchmap.macmap(mac)) is not None :

							# Trying to find parsed MAC to be in mapper, cause it's might be
							# a missmatch or spoofing.
							maced_ip, maced_host_name, maced_desc = record
							self.loggy.debug("Discovered mapped mac with unknown ip")
							self.recap["missmatched_ip"].append(

								dict(

									discovered_ip=ip,
									filch_mapped_mac=None,
									filch_mapped_host_name=None,
									filch_mapped_description=None,
									discovered_mac=mac,
									filch_maced_ip=maced_ip,
									filch_maced_host_name=maced_host_name,
									filch_maced_description=maced_desc,
								)
							)


						else:

							self.loggy.debug("Discovered unkonwn host")
							self.recap["unknown_ip"].append(

								dict(

									discovered_ip=ip,
									filch_mapped_mac=None,
									filch_mapped_host_name=None,
									filch_mapped_description=None,
									discovered_mac=mac,
									filch_maced_ip=None,
									filch_maced_host_name=None,
									filch_maced_description=None,
								)
							)




					return	True


				self.loggy.warning(f"Handler {self} invalid parse result for line \"{line}\"")
















class SNMPWatchAccessHandler(GroupParser):

	"""
		Hanldes snmp records occurrences
	"""

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.recap = defaultdict(lambda : defaultdict(int))


	@GroupParser.register_counter
	def __call__(self, line :str, register :str) -> bool :

		if	(linked_register := super().__call__(line, register)) is not None:
			if	(target := self.parse(line, "src", "msg")) is not None:

				try:

					src,message = target
					if		src in self.filchmap : source = self.filchmap.ipmap_host(src)
					else:	source = src


					self.recap[source][message] += 1
					self.loggy.debug(f"{source} message counted")


					return	True


				except	Exception as E:
					self.loggy.warning(f"{self} failed to count {source} message due to {CAST(E)}")
			else:	self.loggy.warning(f"Invalid {self} parser result")







